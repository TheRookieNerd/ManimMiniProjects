from manimlib.imports import *
#from big_ol_pile_of_manim_imports import *


DEFAULT_SCALAR_FIELD_COLORS = [BLUE_E, GREEN, YELLOW, RED]

class DivergenceAsNewFunction(Scene):
    def construct(self):
        self.add_plane()
        self.show_vector_field_function()
        #self.show_divergence_function()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        self.add(plane)

    def func(self, point):
        x, y = point[:2]
        top_part = np.array([(y - 1.0), -x, 0])
        bottom_part = np.array([-(y + 1.0), x, 0])
        norm = get_norm
        return 1 * op.add(
            top_part / (norm(top_part) * norm(point - UP) + 0.1),
            bottom_part / (norm(bottom_part) * norm(point - DOWN) + 0.1),
            # top_part / (norm(top_part)**2 + 1),
            # bottom_part / (norm(bottom_part)**2 + 1),
        )

    def show_vector_field_function(self):
        func = self.func
        unscaled_vector_field = VectorField(
            func,
            length_func=lambda norm: norm,
            colors=[BLUE_C, YELLOW, RED],
            delta_x=np.inf,
            delta_y=np.inf,
        )
        self.play(ShowCreation(unscaled_vector_field))
        in_dot = Dot(color=PINK)
        in_dot.move_to(3.75 * LEFT + 1.25 * UP)

        def get_input():
            return in_dot.get_center()

        def get_out_vect():
            return unscaled_vector_field.get_vector(get_input())

 

        in_dot.save_state()
        in_dot.move_to(ORIGIN)
        self.play(in_dot.restore)
        self.wait()
        #self.play(*[
            #ReplacementTransform(
                #VGroup(mob.copy().fade(1)),
                #VGroup(out_x, out_y),
            #)
            #for mob in (in_x, in_y)
        #])
        out_vect = get_out_vect()
        #VGroup(out_x, out_y).match_style(out_vect)
        out_vect.save_state()
        out_vect.move_to(rhs)
        out_vect.set_fill(opacity=0)
        self.play(out_vect.restore)
        self.out_vect_update = ContinualUpdate(
            out_vect,
            lambda ov: Transform(ov, get_out_vect()).update(1)
        )
        self.add(self.out_vect_update)
        #self.add(out_x_update, out_y_update)

        #self.add(ContinualUpdate(
            #VGroup(out_x, out_y),
            #lambda m: m.match_style(out_vect)
        #))
        self.wait()

        for vect in DOWN, 2 * RIGHT, UP:
            self.play(
                in_dot.shift, 3 * vect,
                run_time=3
            )
            self.wait()

        self.in_dot = in_dot
        self.out_vect = out_vect
        #self.func_equation = VGroup(func_tex, rhs)
        #self.out_x, self.out_y = out_x, out_y
        #self.in_x, self.in_y = out_x, out_y
        #self.in_x_update = in_x_update
        #self.in_y_update = in_y_update
        #self.out_x_update = out_x_update
        #self.out_y_update = out_y_update


def four_swirls_function(point):
    x, y = point[:2]
    result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
    result *= 0.05
    norm = get_norm(result)
    #if norm == 0:
        #return result
    #result *= 2 * sigmoid(norm) / norm
    return result


def get_rgb_gradient_function(min_value=0, max_value=1,
                              colors=[BLUE, RED],
                              flip_alphas=True,  # Why?
                              ):
    rgbs = np.array(list(map(color_to_rgb, colors)))

    def func(values):
        alphas = inverse_interpolate(min_value, max_value, values)
        alphas = np.clip(alphas, 0, 1)
        # if flip_alphas:
        #     alphas = 1 - alphas
        scaled_alphas = alphas * (len(rgbs) - 1)
        indices = scaled_alphas.astype(int)
        next_indices = np.clip(indices + 1, 0, len(rgbs) - 1)
        inter_alphas = scaled_alphas % 1
        inter_alphas = inter_alphas.repeat(3).reshape((len(indices), 3))
        result = interpolate(rgbs[indices], rgbs[next_indices], inter_alphas)
        return result

    return func

class VectorField(VGroup):
    CONFIG = {
        "delta_x": 0.5,
        "delta_y": 0.5,
        "x_min": int(np.floor(-FRAME_WIDTH / 2)),
        "x_max": int(np.ceil(FRAME_WIDTH / 2)),
        "y_min": int(np.floor(-FRAME_HEIGHT / 2)),
        "y_max": int(np.ceil(FRAME_HEIGHT / 2)),
        "min_magnitude": 0,
        "max_magnitude": 2,
        "colors": DEFAULT_SCALAR_FIELD_COLORS,
        # Takes in actual norm, spits out displayed norm
        "length_func": lambda norm: 0.5 * sigmoid(norm),
        "stroke_color": BLACK,
        "stroke_width": 0.5,
        "fill_opacity": 1.0,
        "vector_config": {},
    }

    def __init__(self, func, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.func = func
        self.rgb_gradient_function = get_rgb_gradient_function(
            self.min_magnitude,
            self.max_magnitude,
            self.colors,
            flip_alphas=False
        )
        for x in np.arange(self.x_min, self.x_max, self.delta_x):
            for y in np.arange(self.y_min, self.y_max, self.delta_y):
                point = x * RIGHT + y * UP
                self.add(self.get_vector(point))

    def get_vector(self, point, **kwargs):
        output = np.array(self.func(point))
        norm = get_norm(output)
        if norm == 0:
            output *= 0
        else:
            output *= self.length_func(norm) / norm
        vector_config = dict(self.vector_config)
        vector_config.update(kwargs)
        vect = Vector(output, **vector_config)
        vect.shift(point)
        fill_color = rgb_to_color(
            self.rgb_gradient_function(np.array([norm]))[0]
        )
        vect.set_color(fill_color)
        vect.set_fill(opacity=self.fill_opacity)
        vect.set_stroke(
            self.stroke_color,
            self.stroke_width
        )
        return vect


# Continual animations

def get_force_field_func(*point_strength_pairs, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in point_strength_pairs:
            to_center = center - point
            norm = get_norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            elif norm >= radius:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func


def get_charged_particles(color, sign, radius=0.1):
    result = Circle(
        stroke_color=WHITE,
        stroke_width=0.5,
        fill_color=color,
        fill_opacity=0.8,
        radius=radius
    )
    sign = TexMobject(sign)
    sign.set_stroke(WHITE, 1)
    sign.set_width(0.5 * result.get_width())
    sign.move_to(result)
    result.add(sign)
    return result


def get_proton(radius=0.1):
    return get_charged_particles(RED, "+", radius)


def get_electron(radius=0.05):
    return get_charged_particles(BLUE, "-", radius)


class IntroduceVectorField(Scene):
    CONFIG = {
        "vector_field_config": {
            # "delta_x": 2,
            # "delta_y": 2,
            "delta_x": 0.5,
            "delta_y": 0.5,
        },
        "stream_line_config": {
            "start_points_generator_config": {
                # "delta_x": 1,
                # "delta_y": 1,
                "delta_x": 0.25,
                "delta_y": 0.25,
            },
            "virtual_time": 3,
        },
        "stream_line_animation_config": {
            # "line_anim_class": ShowPassingFlash,
            "line_anim_class": ShowPassingFlash,
        }
    }

    def construct(self):
        self.add_plane()
        self.add_title()
        self.points_to_vectors()
        self.show_fluid_flow()
        self.show_gravitational_force()
        self.show_magnetic_force()
        self.show_fluid_flow()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        plane.remove(plane.coordinate_labels[-1])
        self.add(plane)

    def add_title(self):
        title = TextMobject("Vector field")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle(opacity=1, buff=SMALL_BUFF)
        self.add_foreground_mobjects(title)

    def points_to_vectors(self):
        vector_field = self.vector_field = VectorField(
            four_swirls_function,
            **self.vector_field_config
        )
        dots = VGroup()
        for vector in vector_field:
            dot = Dot(radius=0.05)
            dot.move_to(vector.get_start())
            dot.target = vector
            dots.add(dot)

class ShorteningLongVectors(IntroduceVectorField):
    def construct(self):
        self.add_plane()
        self.add_title()
        self.contrast_adjusted_and_non_adjusted()

    def contrast_adjusted_and_non_adjusted(self):
        func = four_swirls_function
        unadjusted = VectorField(
            func, length_func=lambda n: n, colors=[WHITE],
        )
        adjusted = VectorField(func)
        for v1, v2 in zip(adjusted, unadjusted):   #zip pairs, each component of adjusted to the corresponding component in unadjusted, where adjusted and unadjusted are lists
            v1.save_state()                        #for restoring to original size, you to save a state before,
            v1.target = v2                         #just like declaring a target before movetotarget 

        self.add(adjusted)
        self.wait()

        #makes stuff bigger
        self.play(LaggedStart(
            MoveToTarget, adjusted,
            run_time=3
        ))
        self.wait()

        #restores to normal
        self.play(LaggedStart(
            ApplyMethod, adjusted,
            lambda m: (m.restore,),
            run_time=3
        ))
        self.wait()



#changing field

class ChangingElectricField(Scene):
    CONFIG = {
        "vector_field_config": {}
    }

    def construct(self):
        particles = self.get_particles()
        vector_field = self.get_vector_field()

        def update_vector_field(vector_field):
            new_field = self.get_vector_field()
            Transform(vector_field, new_field).update(1)
            vector_field.func = new_field.func

        def update_particles(particles, dt):
            func = vector_field.func
            for particle in particles:
                force = func(particle.get_center())
                particle.velocity += force * dt
                particle.shift(particle.velocity * dt)

        self.add(
            ContinualUpdate(vector_field, update_vector_field),
            ContinualUpdateFromTimeFunc(particles, update_particles),
        )
        self.wait(5)

    def get_particles(self):
        particles = self.particles = VGroup()
        for n in range(9):
            if n % 2 == 0:
                particle = get_proton(radius=0.2)
                particle.charge = +1
            else:
                particle = get_electron(radius=0.2)
                particle.charge = -1
            particle.velocity = np.random.normal(0, 0.1, 3)
            particles.add(particle)
            particle.shift(np.random.normal(0, 0.2, 3))

        particles.arrange_submobjects_in_grid(buff=LARGE_BUFF)
        return particles

    def get_vector_field(self):
        func = get_force_field_func(*list(zip(
            list(map(Mobject.get_center, self.particles)),
            [p.charge for p in self.particles]
        )))
        self.vector_field = VectorField(func, **self.vector_field_config)
        return self.vector_field


#for zoom in

class DivergenceTinyNudgesView(MovingCameraScene):
    CONFIG = {
        "scale_factor": 0.25,
        "point": ORIGIN,
    }

    def construct(self):
        self.add_vector_field()
        self.zoom_in()
        #self.take_tiny_step()
        #self.show_dot_product()
        #self.show_circle_of_values()
        #self.switch_to_curl_words()
        #self.rotate_difference_vectors()

    def add_vector_field(self):
        plane = self.plane = NumberPlane()

        def func(p):
            x, y = p[:2]
            result = np.array([
                np.sin(x + 0.1),
                np.cos(2 * y),
                0
            ])
            result /= (get_norm(result)**0.5 + 1)
            return result

        vector_field = self.vector_field = VectorField(
            func,
            #length_func=lambda n: 0.5 * sigmoid(n),
            # max_magnitude=1.0,
        )
        self.add(plane)
        self.add(vector_field)

    def zoom_in(self):
        point = self.point
        vector_field = self.vector_field
        sf = self.scale_factor

        vector_field.vector_config.update({
            "rectangular_stem_width": 0.02,
            "tip_length": 0.1,
        })
        vector_field.length_func = lambda n: n
        vector = vector_field.get_vector(point)

        input_dot = Dot(point).scale(sf)
        input_words = TextMobject("$(x_0, y_0)$").scale(sf)
        input_words.next_to(input_dot, DL, SMALL_BUFF * sf)
        output_words = TextMobject("Output").scale(sf)
        output_words.add_background_rectangle(color= BLACK )
        output_words.next_to(vector.get_top(), UP, sf * SMALL_BUFF)
        output_words.match_color(vector)

        self.play(
            self.camera_frame.scale, sf,
            self.camera_frame.move_to,np.array([0,1,0]),
            FadeOut(vector_field),
            FadeIn(vector),
            run_time=2
        )
        self.add_foreground_mobjects(input_dot)
        self.play(
            FadeIn(input_dot, SMALL_BUFF*DL),
            Write(input_words),
        )
        self.play(
            Indicate(vector),
            Write(output_words),
        )
        self.wait()

        self.set_variables_as_attrs(
            point, vector, input_dot,
            input_words, output_words,
        )


class IntroduceVectorField(Scene):
    CONFIG = {
        "vector_field_config": {
            # "delta_x": 2,
            # "delta_y": 2,
            "delta_x": 0.5,
            "delta_y": 0.5,
        },
        "stream_line_config": {
            "start_points_generator_config": {
                # "delta_x": 1,
                # "delta_y": 1,
                "delta_x": 0.25,
                "delta_y": 0.25,
            },
            "virtual_time": 3,
        },
        "stream_line_animation_config": {
            # "line_anim_class": ShowPassingFlash,
            "line_anim_class": ShowPassingFlash,
        }
    }

    def construct(self):
        self.add_plane()
        self.add_title()
        self.points_to_vectors()
        self.show_fluid_flow()
        self.show_gravitational_force()
        self.show_magnetic_force()
        self.show_fluid_flow()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        plane.remove(plane.coordinate_labels[-1])
        self.add(plane)

    def add_title(self):
        title = TextMobject("Vector field")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle(opacity=1, buff=SMALL_BUFF)
        self.add_foreground_mobjects(title)

    def points_to_vectors(self):
        vector_field = self.vector_field = VectorField(
            four_swirls_function,
            **self.vector_field_config
        )
        dots = VGroup()
        for vector in vector_field:
            dot = Dot(radius=0.05)
            dot.move_to(vector.get_start())
            dot.target = vector
            dots.add(dot)

        self.play(LaggedStart(GrowFromCenter, dots))
        self.wait()
        self.play(LaggedStart(MoveToTarget, dots, remover=True))
        self.add(vector_field)
        self.wait()

    def show_fluid_flow(self):
        vector_field = self.vector_field
        stream_lines = StreamLines(
            vector_field.func,
            **self.stream_line_config
        )
        stream_line_animation = StreamLineAnimation(
            stream_lines,
            **self.stream_line_animation_config
        )

        self.add(stream_line_animation)
        self.play(
            vector_field.set_fill, {"opacity": 0.5}
        )
        self.wait(7)
        self.play(
            vector_field.set_fill, {"opacity": 1},
            VFadeOut(stream_line_animation.mobject),
        )
        self.remove(stream_line_animation)

    def show_gravitational_force(self):
        earth = self.earth = ImageMobject("earth")
        moon = self.moon = ImageMobject("moon", height=1)
        earth_center = 3 * RIGHT + 2 * UP
        moon_center = 3 * LEFT + DOWN
        earth.move_to(earth_center)
        moon.move_to(moon_center)

        gravity_func = get_force_field_func((earth_center, -6), (moon_center, -1))
        gravity_field = VectorField(
            gravity_func,
            **self.vector_field_config
        )

        self.add_foreground_mobjects(earth, moon)
        self.play(
            GrowFromCenter(earth),
            GrowFromCenter(moon),
            Transform(self.vector_field, gravity_field),
            run_time=2
        )
        self.vector_field.func = gravity_field.func
        self.wait()

    def show_magnetic_force(self):
        magnetic_func = get_force_field_func(
            (3 * LEFT, -1), (3 * RIGHT, +1)
        )
        magnetic_field = VectorField(
            magnetic_func,
            **self.vector_field_config
        )
        magnet = VGroup(*[
            Rectangle(
                width=3.5,
                height=1,
                stroke_width=0,
                fill_opacity=1,
                fill_color=color
            )
            for color in (BLUE, RED)
        ])
        magnet.arrange_submobjects(RIGHT, buff=0)
        for char, vect in ("S", LEFT), ("N", RIGHT):
            letter = TextMobject(char)
            edge = magnet.get_edge_center(vect)
            letter.next_to(edge, -vect, buff=MED_LARGE_BUFF)
            magnet.add(letter)

        self.add_foreground_mobjects(magnet)
        self.play(
            self.earth.scale, 0,
            self.moon.scale, 0,
            DrawBorderThenFill(magnet),
            Transform(self.vector_field, magnetic_field),
            run_time=2
        )
        self.vector_field.func = magnetic_field.func
        self.remove_foreground_mobjects(self.earth, self.moon)

x=2
class MovingSine(Scene):
    def construct(self):
        x=2
        def update_sin(sin, dt):
            if x>=0 and x<=2:
                New_sin = FunctionGraph(lambda m:x*np.sin(m))   
                x-=.1
            if x<0 and x>=-2:
                New_sin = FunctionGraph(lambda m:x*np.sin(m))   
                x+=.1            
            sin.become(New_sin)

        sin = FunctionGraph(lambda x: np.sin(x))
        sin.add_updater(update_sin)
        self.play(ShowCreation(sin))
        self.wait(3)


class Partials(MovingCameraScene):
    CONFIG={
        "VectorField_kwargs":{
            "delta_x": .5,
            "delta_y": .5,
            "length_func": lambda norm: .45* sigmoid(norm),
            #"opacity": 1.0,          
        },
        "localfield_kwargs":{
            #"xmin":1,
            #"x_max":3,
             #"y_min":0,
            #"y_max":2,
            "opacity": .15,
            "delta_x":.5,
            "delta_y":.5,
            "length_func": lambda norm: .65* sigmoid(norm),
        },
        "grid_kwargs":{},
        "point_charge_loc": np.array([2,0,0]),
        "focus":np.array([2,1,0]),
    }
 
    def construct(self):
        self.plane()
        self.zoominandstuff()
 
    def plane(self):
        grid= NumberPlane(**self.grid_kwargs)
        grid.add_coordinates()
        self.add(grid)
 
    def zoominandstuff(self):
        mainfield = VectorField(function1, **self.VectorField_kwargs)
        localfield = VectorField(function1, **self.localfield_kwargs)
        self.play(ShowCreation(mainfield), run_time=2, )  
        self.play(
            FadeOut(mainfield),
            self.camera_frame.scale, .25,
            self.camera_frame.move_to, self.focus,
            FadeIn(localfield),
            run_time=3
            )
 
        #self.add(localfield)
        demo_dot = Dot(color=WHITE).scale(.4)
        demo_dot.move_to(self.focus+LEFT)
 
        def get_demo_vect():
            return localfield.get_vector(demo_dot.get_center())
 
        demo_vect = get_demo_vect()
        P_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,1,0]),)
        P=MeasureDistance(P_line).add_tips()
        P_label=P.get_text("P")
 
        self.add(demo_vect)
        self.play(
            GrowFromCenter(P),
            #GrowFromCenter(Q),
            Write(P_label),
            #Write(Q_label),
            run_time=1
            )
 
        P_group=VGroup(P,P_label)
 
        def update_P(p_group):
           
            p_line=Line(demo_vect.points[0],np.array([demo_vect.get_end()[0]+.000001,1,0]))
            new_P=MeasureDistance(p_line).add_tips()
            new_P_label=new_P.get_text("P")
            p_group[0].become(new_P)
            p_group[1].become(new_P_label)
 
 
        def update_Q(q_group):
 
            q_line=Line(np.array([demo_vect.get_end()[0],1,0]),demo_vect.get_end()+UP*.000001,)
            new_Q=MeasureDistance(q_line,color=RED).add_tips()
            new_Q_label=new_Q.get_text("Q")
            if q_line.get_length()<0.01:
                new_Q.fade(1)
                new_Q_label.fade(1)
            q_group[0].become(new_Q)
            q_group[1].become(new_Q_label)
 
 
        def update_vector(obj):
            obj.become(get_demo_vect())
 
        #First add demo_vect and then add P_group, because demo_vect appears before.
        demo_vect.add_updater(update_vector)
        P_group.add_updater(update_P)
 
 
        self.add(demo_vect,P_group)
        for vect in self.focus, self.focus+RIGHT:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                rate_func= linear,
                run_time=3)
           
        Q_line=Line(np.array([demo_vect.get_end()[0],1,0]),demo_vect.get_end()+UP*.00001)
        Q=MeasureDistance(Q_line,color=RED).add_tips()
        Q_label=Q.get_text("Q")
 
        Q_group=VGroup(Q,Q_label)
 
        self.play(
            GrowFromCenter(Q),
            Write(Q_label),
            run_time=1
            )
 
        Q_group.add_updater(update_Q)
        self.add(Q_group)
        for vect in self.focus, self.focus+LEFT:
            self.play(
                ApplyMethod(demo_dot.move_to, vect,),
                rate_func= linear,
                run_time=3)
        self.wait()