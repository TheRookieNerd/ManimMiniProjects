from big_ol_pile_of_manim_imports import *

#while referring to the dictionary, we have to use self.

class Curve(Scene):
    CONFIG={
    "amp":2.3,
    "t_offset":0,
    "rate":0.05,
    "x_min":4,                                                                                  #xmin and max are to define the bounds of the horizontal graph
    "x_max":9,
    "wait_time":15,
    "color_1":RED,
    "color_2":GREEN,
    }
 
    def construct(self):
        rate_no_updater=self.rate
        def update_curve(c, dt):
            other_mob = FunctionGraph(                                                          #look at FunctoinGraph in functions.py in mobjects
                lambda x: self.amp*np.sin((x - (self.t_offset + self.rate)+rate_no_updater)),   #why +rate_no_updater?
                    x_min=0,x_max=self.x_max
                ).shift(LEFT*self.x_min)                                                        #shift.left is to the center the circle over the left bonud of graph
            c.become(other_mob)
            self.t_offset += self.rate
       
        c = FunctionGraph(
            lambda x: self.amp*np.sin((x- (self.t_offset + self.rate)+rate_no_updater)),
            x_min=0,x_max=self.x_max
            ).shift(LEFT*self.x_min)
 
        point=Dot()
        point.move_to(c.points[0])                                                              #points are arrays holding certain points on a shape. 0 denotes the first point and -1 denotes the last point as in a normal array
        point_center=Dot()
        circle=Circle(radius=self.amp)\
               .shift(RIGHT*point.get_center()[0])                                              # \ is to link the next line
        point_center.move_to(circle.get_center())
 
        la=Line(
            circle.get_center(),
            circle.get_center()+RIGHT*self.amp/2,
            color=self.color_1
            )
        lb=DashedLine(
            circle.get_center(),
            circle.get_center()+RIGHT*self.amp/2,
            color=self.color_2
            ).rotate(PI)                                                                        #why rotate PI
        lc=Line(
            circle.get_center(),
            circle.get_center()+LEFT*self.amp/2,
            color=self.color_1
            )
        ld=DashedLine(
            circle.get_center(),
            circle.get_center()+LEFT*self.amp/2,
            color=self.color_2
            ).rotate(PI)
        def update_la(la,dt):
            a=point.get_center()[1]
            b=la.get_length()
            alpha_la=4*np.arctan((2*b-np.sqrt(4*(b**2)-a**2))/(a+0.00001))                     #.00001 to balance somekind of data change, if removed, error showing can convert float into int           
            beta_la=PI/2-alpha_la/2
            ap=PI-alpha_la/2
            bp=PI/2-beta_la
 
            la.set_angle(bp)
        def update_lc(lc,dt):
            a=point.get_center()[1]                                                            #ask what is a? (i.e.) object or what?
            b=lc.get_length()
            alpha_lc=4*np.arctan((2*b-np.sqrt(4*(b**2)-a**2))/(a+0.00001))
            beta_lc=PI/2-alpha_lc/2
            ap=PI-alpha_lc/2
            bp=PI/2-beta_lc
 
            lc.set_angle(bp+2*beta_lc)
 
 
        self.play(  ShowCreation(c),
                    ShowCreation(point),
                    ShowCreation(circle),
                    ShowCreation(la),
                    ShowCreation(lb),
                    ShowCreation(lc),
                    ShowCreation(ld),
                )
        self.wait()
 
        la.add_updater(update_la)
        lc.add_updater(update_lc)
        point.add_updater(lambda m: m.move_to(c.points[0]))
        lb.add_updater(lambda m: m.put_start_and_end_on(la.points[-1],point.get_center()))
        ld.add_updater(lambda m: m.put_start_and_end_on(lc.points[-1],point.get_center()))
        c.add_updater(update_curve)
        self.add(c,point,la,lb,lc,ld)
 
        self.wait(self.wait_time)
        c.remove_updater(update_curve)
 
        self.wait()