from manimlib.imports import *


class PolyToEl(MovingCameraScene):
    def construct(self):
        n = 10
        mat = np.zeros(shape=(n, n))

        for i in range(n):
            mat[i] = [1 / 2 if j == i or j == (i + 1) % n else 0 for j in range(n)]

        lims = FRAME_HEIGHT - 4
        coords = [np.array([random.randrange(-lims, lims), random.randrange(-lims, lims), 0]) for j in range(n)]
        dots = VGroup(*[Dot(_) for _ in coords])
        lines = VGroup(*[Line(coords[i], coords[(i + 1) % n]) for i in range(n)])
        self.add(dots, lines)

        # pseudo_coords = [np.array([i[0], i[1]]) for i in coords]
        pseudo_one = 1
        for _ in range(500):
            if _ != 0:
                if _ % 30 == 0:
                    scale_fac = 0.4
                    pseudo_one *= scale_fac

                    zoom_rect = Square(side_length=1 / scale_fac * FRAME_HEIGHT * pseudo_one)
                    self.play(ShowCreation(zoom_rect))
                    self.play(self.camera_frame.scale, scale_fac,
                              self.camera_frame.move_to, center_of_mass(coords),
                              # dots.scale_in_place, scale_fac,
                              # lines.scale, pseudo_one
                              )
            coords = mat.dot(coords)
            # coords = [np.array([i[0], i[1], 0]) for i in new_pseudo_coords]
            pseudo_coords = [np.array([i[0], i[1]]) for i in coords]

            new_dots_temp = VGroup(*[Dot(_, radius=0.075 * pseudo_one, color=YELLOW) for _ in coords])
            new_lines_temp = VGroup(*[Line(coords[i], coords[(i + 1) % n], color=YELLOW) for i in range(n)])

            self.play(FadeIn(new_dots_temp))
            self.play(FadeIn(new_lines_temp))

            new_dots = VGroup(*[Dot(_, radius=0.075 * pseudo_one) for _ in coords])
            new_lines = VGroup(*[Line(coords[i], coords[(i + 1) % n]) for i in range(n)])
            # self.add(dots, lines)
            # dots.become(new_dots)
            # lines.become(new_lines)

            self.play(
                dots.become, new_dots,
                lines.become, new_lines,
                # ReplacementTransform(dots, new_dots),
                # ReplacementTransform(lines, new_lines),
                FadeOut(new_dots_temp),
                FadeOut(new_lines_temp),
                run_time=1
            )
