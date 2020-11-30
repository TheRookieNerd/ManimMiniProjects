from manimlib.imports import *


class PyTree(Scene):
    CONFIG = {
        "rect_kwargs": {
            "stroke_width": 0.5,
            "fill_opacity": .75,
            "fill_color": RED,
        }
    }

    def construct(self):
        # get_start_anchors() = get_start_anchors()
        square = Square(**self.rect_kwargs).shift(DOWN * 2)  # .rotate(PI / 4)

        self.add(square)
        squares = VGroup(square)
        rep = 2
        temp = VGroup()
        for _ in range(rep):
            for sq in squares:
                verts = sq.get_start_anchors()
                # for _ in range(rep):
                rect1, rect2 = self.bisect_square(sq)
                self.add(rect1, rect2)
                perp1 = (rotate_vector(-(3 / 4) * (verts[0] - verts[-1]), PI / 2) + sq.get_center())
                perp2 = (rotate_vector(-(3 / 4) * (verts[1] - verts[2]), -PI / 2) + sq.get_center())
                # self.add(*[Dot(l) for l in [perp1, perp2]])
                self.play(
                    rect1.move_to, perp1,
                    rect2.move_to, perp2,
                )
                self.play(
                    rect1.shift, (verts[0] - verts[-1]) / 2,
                    rect2.shift, (verts[1] - verts[2]) / 2,
                )
                trxn1 = self.trisect_rect(rect1)
                trxn2 = self.trisect_rect(rect2)
                self.add(trxn1, trxn2)
                self.remove(rect1, rect2)

                self.previous_angles1 = [0, 0, 0]
                self.previous_angles2 = [0, 0, 0]

                ##############################################
                def update_trxn1_tri1(mob, alpha):
                    # print(alpha)
                    mob.rotate((PI) * alpha - self.previous_angles1[0], about_point=verts[1])
                    self.previous_angles1[0] = (PI) * alpha

                def update_trxn1_tri2(mob, alpha):
                    # print(alpha)
                    mob.rotate((-PI / 2) * alpha - self.previous_angles1[1], about_point=trxn1[1].get_start_anchors()[2])
                    self.previous_angles1[1] = (-PI / 2) * alpha

                def update_trxn1_tri3(mob, alpha):
                    # print(alpha)
                    mob.rotate((-2 * PI) * alpha - self.previous_angles1[2], about_point=trxn1[2].get_start_anchors()[0])
                    self.previous_angles1[2] = (-2 * PI) * alpha

                def update_trxn1_pos_mid_tri(mob):
                    offset = trxn1[1].get_center() - trxn1[1].get_start_anchors()[2]
                    mob.move_to(trxn1[0].get_start_anchors()[0] + offset)

                def update_trxn1_pos_top_tri(mob):
                    offset = trxn1[2].get_center() - trxn1[2].get_start_anchors()[0]
                    mob.move_to(trxn1[1].get_start_anchors()[0] + offset)
                ##############################################

                ##############################################
                def update_trxn2_tri1(mob, alpha):
                    # print(alpha)
                    mob.rotate((-PI) * alpha - self.previous_angles2[0], about_point=verts[0])
                    self.previous_angles2[0] = (-PI) * alpha

                def update_trxn2_tri2(mob, alpha):
                    # print(alpha)
                    mob.rotate((PI / 2) * alpha - self.previous_angles2[1], about_point=trxn2[1].get_start_anchors()[2])
                    self.previous_angles2[1] = (PI / 2) * alpha

                def update_trxn2_tri3(mob, alpha):
                    # print(alpha)
                    mob.rotate((2 * PI) * alpha - self.previous_angles2[2], about_point=trxn2[2].get_start_anchors()[0])
                    self.previous_angles2[2] = (2 * PI) * alpha

                def update_trxn2_pos_mid_tri(mob):
                    offset = trxn2[1].get_center() - trxn2[1].get_start_anchors()[2]
                    mob.move_to(trxn2[0].get_start_anchors()[0] + offset)

                def update_trxn2_pos_top_tri(mob):
                    offset = trxn2[2].get_center() - trxn2[2].get_start_anchors()[0]
                    mob.move_to(trxn2[1].get_start_anchors()[0] + offset)
                ##############################################

                trxn1[1].add_updater(update_trxn1_pos_mid_tri)
                trxn1[2].add_updater(update_trxn1_pos_top_tri)

                trxn2[1].add_updater(update_trxn2_pos_mid_tri)
                trxn2[2].add_updater(update_trxn2_pos_top_tri)

                self.add(trxn1[1:])
                self.add(trxn2[1:])
                self.play(
                    UpdateFromAlphaFunc(trxn1[0], update_trxn1_tri1),
                    UpdateFromAlphaFunc(trxn1[1], update_trxn1_tri2),
                    UpdateFromAlphaFunc(trxn1[2], update_trxn1_tri3),

                    UpdateFromAlphaFunc(trxn2[0], update_trxn2_tri1),
                    UpdateFromAlphaFunc(trxn2[1], update_trxn2_tri2),
                    UpdateFromAlphaFunc(trxn2[2], update_trxn2_tri3),
                    run_time=2
                )
                sq1 = VMobject(**self.rect_kwargs).set_points_as_corners([trxn1[1].get_start_anchors()[1], trxn1[1].get_start_anchors()[0], verts[1], trxn1[0].get_start_anchors()[0], trxn1[1].get_start_anchors()[1]])
                sq2 = sq1.copy().flip().move_to(trxn2[0].get_start_anchors()[1])
                self.add(sq1, sq2)

                # self.play(
                #     AnimationGroup(
                #         *[ShowCreation(Dot(k)) for k in sq1.get_start_anchors()],
                #         lag_ratio=0.5
                #     )
                # )
                # self.play(
                #     AnimationGroup(
                #         *[ShowCreation(Dot(k)) for k in sq2.get_start_anchors()],
                #         lag_ratio=0.5
                #     )
                # )
                self.play(*[FadeOut(j) for j in [trxn1, trxn2]])
                # self.remove(trxn1, trxn2)
                # self.play(Indicate(sq1), Indicate(sq2))
                # self.play(trxn1.shift, RIGHT)
                print("FFFFFFF")
                temp = VGroup(sq1, sq2)
                # temp.add(sqs)

            print(f"Loop {_} over")
            squares = temp
            print(squares)
            temp = VGroup()
            # self.play(trxn1[0].rotate, PI, {"about_point": trxn1[0].get_start_anchors()[2]})
            # self.play(Indicate(trxn1[0]))
            # self.add(*[Dot(i) for i in [perp1, perp2]])
        self.wait()

    def bisect_square(self, sq):
        verts = sq.get_start_anchors()
        print(verts)
        midpts = [midpoint(*verts[_:_ + 2]) for _ in [0, 2]]

        rect1 = VMobject(**self.rect_kwargs)
        rect1.set_points_as_corners([midpts[0], *verts[1:3], midpts[1], midpts[0]])
        rect2 = VMobject(**self.rect_kwargs)
        rect2.set_points_as_corners([verts[0], *midpts, verts[-1], verts[0]])

        rects = VGroup(rect1, rect2)
        return rects

    def trisect_rect(self, rect):
        verts = rect.get_start_anchors()
        midpt = midpoint(*verts[1:3])
        tri1 = VMobject(**self.rect_kwargs).set_points_as_corners([verts[3], verts[2], midpt, verts[3]])
        tri3 = VMobject(**self.rect_kwargs).set_points_as_corners([*verts[0:2], midpt, verts[0]])
        tri2 = VMobject(**self.rect_kwargs).set_points_as_corners([verts[0], midpt, verts[3], verts[0]])
        trxn = VGroup(*[tri1, tri2, tri3])
        if rect.get_center()[0] > 0:
            trxn.flip()
        return trxn

        # bisect square CHECK
        #  trisect rectangles
        # rearrange trisection to form individual squares and repeat

        # for _ in sq.get_start_anchors():
        #     self.play(FadeIn(Dot(_)))

        # self.wait()
        # cut = VMobject(color="RED").set_points_as_corners([sq.get_start_anchors()[0], sq.get_top(), sq.get_bottom(), *sq.get_start_anchors()[-1::-3]])
        # # cut.set_fill(fill_color="RED")
        # self.wait()

        # def update_sq(mob, alpha):
        #     # print(alpha)
        #     sq.shift(UP * 2 * alpha)
        # print(UP * 2 * alpha)
        # self.play(UpdateFromAlphaFunc(sq, update_sq), run_time=2)
        # mp = [midpoint(*verts[1:3]), midpoint(verts[3], verts[0])]
        # tri1 = VMobject(**self.rect_kwargs).set_points_as_corners([*verts[0:2], *mp[:], verts[0]])
        # tri2 = VMobject(**self.rect_kwargs).set_points_as_corners([*mp[:], *verts[2:], mp[0]])

        # self.add(sq)
        # self.play(ShowCreation(tri1))
        # self.play(ShowCreation(tri2))
        """
        offset = rect2.get_center() - rect2.get_start_anchors()[2]
        self.prev1 = 0
        self.prev2 = 0

        def update_rect1(mob, alpha):
            # print(alpha)
            rect1.rotate((PI / 2) * alpha - self.prev1, about_point=rect1.get_start_anchors()[3])
            self.prev1 = (PI / 2) * alpha

        def update_rect2(mob, alpha):
            # print(alpha)
            rect2.rotate((-PI / 2) * alpha - self.prev2, about_point=rect2.get_start_anchors()[2])
            self.prev2 = (-PI / 2) * alpha

        def update_rect2_pos(mob):
            offset = rect2.get_center() - rect2.get_start_anchors()[3]
            mob.move_to(rect1.get_start_anchors()[2] + offset)
            # print(rect1.get_start_anchors()[1])

        rect2.add_updater(update_rect2_pos)  # lambda x: x.move_to(rect1.get_start_anchors()[2]))
        self.add(rect2, rect1)-------
        self.play(
            # rect1.rotate, PI / 2, {"about_point": rect1.get_start_anchors()[2]},
            UpdateFromAlphaFunc(rect1, update_rect1),
            UpdateFromAlphaFunc(rect2, update_rect2),
            run_time=2
        )
        print(rect1.get_start_anchors()[1])
        """
        # self.play(ShowCreation(self.trisect_rect(rect1)))
