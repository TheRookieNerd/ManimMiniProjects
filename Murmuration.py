from manimlib.imports import *
# from manimlib.utils.space_ops import angle_between


class Boids(Scene):
    CONFIG = {
        "stay_away": 1,
        "local_rad": 1,
        "local_v_weight": 10,  # towards local center
        "common_v_weight": 0.0,  # towards leader
        "leader_v_weight": 0.1,
        "push_v_weight": 2,
        "d": 0
    }

    def construct(self):
        birds = VGroup()
        total_birds = 20
        boundary = Rectangle(height=FRAME_HEIGHT, width=FRAME_WIDTH)
        self.add(boundary)

        boxes = VGroup()
        for _, direction in zip(range(4), [UR, DR, UL, DL]):
            box = Rectangle(height=3, width=3).move_to(2.5 * direction)
            boxes.add(box)
            # self.add(box)
        bird_positions = []
        np.random.seed()
        for box in boxes:
            x0, y0, z0 = np.array([-box.width / 2, -box.height / 2, 0])
            x1, y1, z1 = np.array([box.width / 2, box.height / 2, 0])
            nth_bird_positions = [np.array([
                interpolate(x0, x1, random.random()),
                interpolate(y0, y1, random.random()),
                0
            ]) + box.get_center() for _ in range(int(total_birds / 4))]
            for nbp in nth_bird_positions:
                bird_positions.append(nbp)

        # bird_positions = [np.random.uniform(-FRAME_HEIGHT, 0., size=3) for _ in range(int(total_birds / 2))]
        # bird_positions2 = [np.random.uniform(0, FRAME_HEIGHT, size=3) for _ in range(int(total_birds / 2))]
        # for shit in bird_positions2:
        #     bird_positions.append(shit)
        self.previous_bird_positions = bird_positions
        self.centroid = np.mean(bird_positions, axis=0)

        def check_boundary(mobj):
            if mobj.get_left()[0] < boundary.get_left()[0]:
                mobj.velocity[0] = abs(mobj.velocity[0])

            if mobj.get_right()[0] > boundary.get_right()[0]:
                mobj.velocity[0] = -abs(mobj.velocity[0])

            if mobj.get_bottom()[1] < boundary.get_bottom()[1]:
                mobj.velocity[1] = abs(mobj.velocity[1])

            if mobj.get_top()[1] > boundary.get_top()[1]:
                mobj.velocity[1] = -abs(mobj.velocity[1])

        def update_centroid(center, dt):
            # center.velocity = UP * dt * 2
            self.centroid += center.velocity
            check_boundary(center)
            center.move_to(self.centroid)

        def get_dist(v1, v2):
            return np.linalg.norm(v1.get_center() - v2.get_center())

        def dist_check(bird):
            for b in birds:
                if b != bird:
                    dist = get_dist(b, bird)
                    if dist < self.stay_away:
                        bird.velocity += - (b.get_center() - bird.get_center()) * ((-self.push_v_weight * 10 * dist / self.stay_away) + self.push_v_weight * 10)

        def update_bird(bird, dt):
            s = self.common_v_weight
            direc = (self.centroid - bird.get_center()) / np.linalg.norm(self.centroid - bird.get_center())
            # if bird.get_center()[1] >= self.centroid[1]:
            #     bird.rotate(-angle_between(bird.get_vertices()[0] - bird.get_center(), direc))
            # else:
            #     bird.rotate(angle_between(bird.get_vertices()[0] - bird.get_center(), direc))
            bird.velocity = 1 * s * direc
            lb_positions = []
            # print(bird_positions)
            for pbp in self.previous_bird_positions:
                # print(pbp)
                # print(np.array_equal(pbp, bird.get_center()))
                if not np.array_equal(pbp, bird.get_center()):
                    # print(self.local_rad)
                    if np.linalg.norm(pbp - bird.get_center()) < self.local_rad:
                        # print("Phew")
                        lb_positions.append(pbp)

            # print("Starts")
            # print(lb_positions)
            # print("Ends")
            local_centroid = np.mean(lb_positions, axis=0)
            # print(local_centroid)
            # print()

            local_direc = (local_centroid - bird.get_center()) * self.local_v_weight
            # print(local_direc)
            bird.velocity += local_direc

            dist_check(bird)
            check_boundary(bird)

            bird.shift(bird.velocity * dt)
            # bird.shift(bird.dist_velocity * dt * 0.25)
            if bird is last_bird:
                # print(birds[0].get_center())
                self.previous_bird_positions = [b.get_center() for b in birds]
                # print(self.previous_bird_positions)
            # print("RENEWED")

        last_bird = Dot(np.random.uniform(-3., -1., size=3), radius=0.05, color=RED)

        center = Dot(self.centroid)  # , radius=0.001)
        center.velocity = UR * self.leader_v_weight
        center.add_updater(update_centroid)
        self.add(center)

        for i in range(total_birds):
            bird = Dot(bird_positions[i], radius=0.05, color=RED)
            # bird = Triangle(color=BLUE, fill_opacity=1, fill_color=BLUE).rotate(-PI / 2).scale(0.5).move_to(bird_positions[i])

            birds.add(bird)

        birds.add(last_bird)
        last_bird.add_updater(update_bird)

        for bird in birds:
            s = 2
            direc = (self.centroid - bird.get_center()) / np.linalg.norm(self.centroid - bird.get_center())
            bird.velocity = 1 * s * direc
            bird.add_updater(update_bird)
            # self.add(bird)

        self.add(birds)
        self.wait(10)
        # print(self.centroid)
        # print(birds[0].get_center())
        # self.wait()
