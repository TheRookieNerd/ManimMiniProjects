from manimlib.imports import *


class Twin(Scene):
    CONFIG = {
        "square_kwargs": {
            "stroke_width": 0
        }
    }

    def construct(self):
        # def chop(mobj, hov=True):
        #     if hov:
        #         slice1 = mobj.copy().stretch_about_point(0.5, 1, mobj.get_top())
        #         slice2 = mobj.copy().stretch_about_point(0.5, 1, mobj.get_bottom())
        #     else:
        #         slice1 = mobj.copy().stretch_about_point(0.5, 0, mobj.get_right())
        #         slice2 = mobj.copy().stretch_about_point(0.5, 0, mobj.get_left())
        #     return VGroup(slice1, slice2)

        # sq = Square(fill_color=RED, fill_opacity=1, stroke_width=0.01)
        # self.add(sq)
        # test_mobj = chop(sq)
        # for s, direc in zip(test_mobj, [RIGHT, LEFT]):
        #     self.play(s.shift, (sq.side_length / 4) * direc)
        #     test_mobj = test_mobj[0].add(test_mobj[1])
        # self.add(test_mobj)
        def chop_mobject(mob, voh=True, n=5):
            mobj = mob.copy()
            if voh:
                width = mobj.get_left()[0] - mobj.get_right()[0]
                print(f"width:{width}")
                step = abs(width) / n
                print(f"step:{step}")
            else:
                height = mobj.get_top()[1] - mobj.get_bottom()[1]
                step = abs(height) / n

            precision = 3
            pts = np.arange(0, 1, 1 / 10**precision)
            sliced_mobj = VGroup()
            for i in range(n - 1):
                cut_pts = []
                for pt in pts:
                    test = mobj.point_from_proportion(pt)
                    if round(test[0], precision - 1) == round(mobj.get_left()[0] + step, precision - 1):
                        # print("In")
                        cut_pts.append(test)

                slice1_pts = []
                slice2_pts = []
                # for p in mobj.points:
                for p in [mobj.point_from_proportion(i) for i in np.arange(0, 1, 0.001)]:
                    if p[0] < cut_pts[0][0]:
                        slice1_pts.append(p)
                    else:
                        slice2_pts.append(p)

                slice1_pts = self.order_slice(slice1_pts)
                slice2_pts = self.order_slice(slice2_pts)
                # cut_pts.reverse()
                # slice1_pts.insert(0, cut_pts[1])
                slice1_pts.append(cut_pts[0])
                # slice1_pts.append(cut_pts[0])
                slice1, slice2 = VMobject().set_points_as_corners(slice1_pts), VMobject().set_points_as_corners(slice2_pts)
                sliced_mobj.add(slice1)
                if i == n - 2:
                    sliced_mobj.add(slice2)

                mobj = slice2
            return sliced_mobj
            # return VGroup(*[Dot(i) for i in cut_pts])

        # test_mobj = VMobject().set_points_as_corners([UP, RIGHT, DR, DL, LEFT, ORIGIN, UP])
        # test_mobj = Circle()
        # test_mobj = Triangle()
        test_mobj = Square()
        test_mobj.set_stroke(color=YELLOW)
        # self.add(test_mobj)
        temp = chop_mobject(test_mobj, n=5)
        temp.arrange_submobjects(direction=RIGHT)
        self.add(temp)
        for i in temp:
            self.play(Indicate(i))
        self.wait()

    def order_slice(self, cut_pts):
        def sort_by_column(pts, col=0):
            coords = sorted([(i, j[col]) for i, j in enumerate(pts)], key=lambda x: x[1])
            sorted_coords = []

            for coord in coords:
                sorted_coords.append(pts[coord[0]])
            return sorted_coords

        y_sorted = sort_by_column(cut_pts, col=1)

        y_grouped = []

        def get_repeat_length(y_sorted):
            b = 0
            yn = y_sorted[0]

            for y2 in y_sorted:
                if not np.array_equal(y2, yn):
                    if y2[1] == yn[1]:
                        b += 1
                    else:
                        break
            return b

        a = 0
        while y_sorted != []:
            b = get_repeat_length(y_sorted)
            y_grouped.append(y_sorted[a: b + 1])
            for _ in range(b + 1):
                y_sorted.pop(0)

        for i, y_group in enumerate(y_grouped):
            y_grouped[i] = sort_by_column(y_group, col=0)

        ordered_pts = []
        for sublist in y_grouped:
            sublist = sort_by_column(sublist)
            for item in sublist:
                ordered_pts.append(item)
        return ordered_pts
