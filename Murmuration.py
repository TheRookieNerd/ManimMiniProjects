from manimlib.imports import *
# from manimlib.utils.space_ops import angle_between


class Boids(Scene):
    CONFIG = {
        "stay_away": 0.25,
        "local_rad": 3,
        "local_v_weight": 4,  # towards local center
        "common_v_weight": 3.,  # towards leader
        "leader_v_weight": 2,
        "push_v_weight": 2,
        "d": 0
    }

    def construct(self):
        birds = VGroup()
        total_birds = 120
        boundary = Rectangle(height=FRAME_HEIGHT, width=FRAME_WIDTH)
        self.add(boundary)

        boxes = VGroup()
        for _, direction in zip(range(6), [UR, DR, UL, DL, 1.5 * RIGHT, 1.5 * LEFT]):
            box = Rectangle(height=3, width=4).move_to(2.5 * direction)
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
            ]) + box.get_center() for _ in range(int(total_birds / 6))]
            for nbp in nth_bird_positions:
                bird_positions.append(nbp)

        last_bird_of_nth_group = []
        d = 0
        for i in range(len(boxes)):
            d += total_birds / len(boxes)
            last_bird_of_nth_group.append(d)
        print(last_bird_of_nth_group)
        # bird_positions = [np.random.uniform(-FRAME_HEIGHT, 0., size=3) for _ in range(int(total_birds / 2))]
        # bird_positions2 = [np.random.uniform(0, FRAME_HEIGHT, size=3) for _ in range(int(total_birds / 2))]
        # for shit in bird_positions2:
        #     bird_positions.append(shit)
        self.previous_bird_positions = bird_positions
        # self.pseudo_lead_right = RIGHT * 3
        # self.pseudo_lead_left = LEFT * 3

        def check_boundary(mobj):
            if mobj.get_left()[0] < boundary.get_left()[0]:
                mobj.velocity[0] = abs(mobj.velocity[0])

            if mobj.get_right()[0] > boundary.get_right()[0]:
                mobj.velocity[0] = -abs(mobj.velocity[0])

            if mobj.get_bottom()[1] < boundary.get_bottom()[1]:
                mobj.velocity[1] = abs(mobj.velocity[1])

            if mobj.get_top()[1] > boundary.get_top()[1]:
                mobj.velocity[1] = -abs(mobj.velocity[1])

        def update_pseudo_lead(leader, dt):
            leader.shift(leader.velocity * dt)
            check_boundary(leader)

        def get_dist(v1, v2):
            return np.linalg.norm(v1.get_center() - v2.get_center())

        def dist_check(bird):
            for b in birds:
                if b != bird:
                    dist = get_dist(b, bird)
                    if dist < self.stay_away:
                        bird.velocity += - (b.get_center() - bird.get_center()) * ((-self.push_v_weight * 10 * dist / self.stay_away) + self.push_v_weight * 10)

        def update_bird(bird, dt):

            bird_index = 0
            for index, b in enumerate(birds):
                if b is bird:
                    bird_index = index
                    # print(bird_index)
            exists = False
            for i in range(len(boxes)):
                if bird_index < last_bird_of_nth_group[i]:
                    direc = (leaders[i].get_center() - bird.get_center()) / np.linalg.norm(leaders[i].get_center() - bird.get_center())
                    exists = True
                    break

            if not exists:
                direc = (leaders[0].get_center() - bird.get_center()) / np.linalg.norm(leaders[0].get_center() - bird.get_center())

            # if bird.get_center()[1] >= self.pseudo_lead_right[1]:
            #     bird.rotate(-angle_between(bird.get_vertices()[0] - bird.get_center(), direc))
            # else:
            #     bird.rotate(angle_between(bird.get_vertices()[0] - bird.get_center(), direc))

            bird.velocity = self.common_v_weight * direc
            lb_positions = []
            for pbp in self.previous_bird_positions:

                if not np.array_equal(pbp, bird.get_center()):
                    if np.linalg.norm(pbp - bird.get_center()) < self.local_rad:
                        lb_positions.append(pbp)

            local_centroid = np.mean(lb_positions, axis=0)

            local_direc = (local_centroid - bird.get_center()) * self.local_v_weight
            bird.velocity += local_direc

            dist_check(bird)
            check_boundary(bird)

            bird.shift(bird.velocity * dt)

            if bird is last_bird:
                self.previous_bird_positions = [b.get_center() for b in birds]

        last_bird = Dot(np.random.uniform(-3., -1., size=3), radius=0.05, color=RED)

        leaders = VGroup()
        for i in range(len(boxes)):
            leader = Dot(boxes[i].get_center())  # , radius=0.001)
            leader.velocity = rotate_vector(RIGHT, 2 * PI * random.random()) * self.leader_v_weight
            leaders.add(leader)

        for leader in leaders:
            leader.add_updater(update_pseudo_lead)
            self.add(leader)

        for i in range(total_birds):
            bird = Dot(bird_positions[i], radius=0.05, color=RED)
            # bird = Triangle(color=BLUE, fill_opacity=1, fill_color=BLUE).rotate(-PI / 2).scale(0.5).move_to(bird_positions[i])
            birds.add(bird)

        birds.add(last_bird)
        last_bird.add_updater(update_bird)

        for bird in birds:
            bird.velocity = RIGHT
            bird.add_updater(update_bird)
            # self.add(bird)

        self.add(birds)
        self.wait(5)
        # print(self.pseudo_lead_right)
        # print(birds[0].get_center())
        # self.wait()
