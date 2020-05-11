from manimlib.imports import *


class Fractal(MovingCameraScene):
    CONFIG = {
        "leave_progress_bars": True,
        "sound": True,
        "tri_config": {
            "stroke_width": 1,
            # "stroke_color": BLACK
        },
        # "camera_config": {"background_color": WHITE}
    }

    def construct(self):
        self.pseudo_one = 1
        tri = Triangle(**self.tri_config)
        self.camera_frame.scale(0.5)
        self.add(tri)
        tri.vertices = [*tri.get_vertices()]
        tri.vertices.append(tri.get_vertices()[0])

        nth_it = tri
        for _ in range(20):
            temp = VGroup()
            for t in nth_it:
                temp.add(*self.cut_tri(t))

            for red in temp:
                if not self.check_in_frame(red):
                    temp.remove(red)

            nth_it = temp
            # self.play(ShowCreation(nth_it))
            # self.add(nth_it)
            if _ % 1 == 0:
                self.play(self.camera_frame.scale, 0.65, self.camera_frame.move_to, ORIGIN)
                self.pseudo_one *= 0.65
            self.play(*[ShowCreation(i) for i in nth_it])

    def cut_tri(self, tri):
        verts = tri.vertices
        side_lengths = []
        for i in [0, 1, 2]:
            side_lengths.append(round(abs(np.linalg.norm(verts[i] - verts[i + 1])), 3))
        slices = VGroup()
        if all(x == side_lengths[0] for x in side_lengths):
            centroid = np.mean(verts[:-1], axis=0)
            for _ in [0, 1, 2]:
                pts = [centroid, verts[_], verts[_ + 1], centroid]
                cut = VMobject(**self.tri_config).set_points_as_corners(pts)
                cut.vertices = pts
                slices.add(cut)

        elif side_lengths[0] == side_lengths[1] or side_lengths[1] == side_lengths[2] or side_lengths[2] == side_lengths[0]:
            hyp = side_lengths.index(max(side_lengths))
            hyp_pts = [interpolate(*[verts[hyp], verts[hyp + 1]], _) for _ in np.arange(0, 1 + 1 / 3, 1 / 3)]
            for j in range(3):
                if hyp != 2:
                    pts = [verts[hyp + 2], hyp_pts[j], hyp_pts[j + 1], verts[hyp + 2]]
                else:
                    pts = [verts[1], hyp_pts[j], hyp_pts[j + 1], verts[1]]
                cut = VMobject(**self.tri_config).set_points_as_corners(pts)
                cut.vertices = pts
                slices.add(cut)

        return slices

    def check_in_frame(self, tri):
        # self.pseudo_one = self.one*0.65
        edge_x = (self.camera_frame.height / 2 * self.pseudo_one) + self.pseudo_one / 2
        edge_y = (self.camera_frame.width / 2 * self.pseudo_one) + self.pseudo_one / 2
        # print(edge_x, edge_y)
        # edge = frame.get_frame_height()
        center = tri.get_center()
        if center[0] > edge_x or center[0] < -edge_x:
            return False

        elif center[1] > edge_y or center[1] < -edge_y:
            return False
        else:
            return True
