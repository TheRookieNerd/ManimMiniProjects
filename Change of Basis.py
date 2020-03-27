from manimlib.imports import *

class ChangeOfBasis(LinearTransformationScene):
	CONFIG = {
		"show_basis_vectors" : False,
		"matrix" : [[1, 1], [-1, 1]],
		"v_coords_T" : [-1,3],
		"i" : [1,1],
		"j" : [-1,1],
		"v_coords_J" : [1,2],
		"v_coord_strings" : ["1", "1"],
		#"leave_ghost_vectors": True,
		"result_coords_string" : """
			=
			\\left[ \\begin{array}{c}
				1(1) + 2(-1) \\\\
				1(1) + 2(1)
			\\end{arary}\\right] 
			= 
			\\left[ \\begin{array}{c}
				-1 \\\\
				3
			\\end{arary}\\right] 
		"""
	}
	def construct(self):
		self.setup()
		#text=TextMobject("How to represent a vector, in Jenny's coordintes")
		#self.add_title(text)
		i_tilde = self.i_tilde=self.add_vector([1, 0], color = X_COLOR)
		j_tilde = self.j_tilde=self.add_vector([0, 1], color = Y_COLOR)
		self.wait(2)
		i_label = self.label_vector(
			i_tilde, "\\hat{\\imath}", 
			color = X_COLOR,
			label_scale_factor = 1
		)
		
		j_label = self.label_vector(
			j_tilde, "\\hat{\\jmath}", 
			color = Y_COLOR,
			label_scale_factor = 1
		)
		self.wait(2)
		self.play(*list(map(FadeOut, [i_label, j_label])))
		self.wait(3)
		self.apply_transposed_matrix(self.matrix)
		self.wait(3)
		i_label = self.label_vector(
			i_tilde, "\\tilde{\\imath}", 
			color = X_COLOR,
			label_scale_factor = 1
		)
		
		j_label = self.label_vector(
			j_tilde, "\\tilde{\\jmath}", 
			color = Y_COLOR,
			label_scale_factor = 1
		)
		self.wait(2)
		self.play(*list(map(FadeOut, [i_label, j_label])))
		self.wait()

		v=self.add_vector(self.v_coords_T)
		v_label = self.label_vector(
			v, "v_{\\jmath}", 
			color = YELLOW,
			label_scale_factor = 1
		)
		self.wait(2)
		self.play(FadeOut(v_label))
		for l,j,k,m in zip([v, i_tilde,j_tilde],[self.v_coords_J, self.i, self.j],[self.v_coords_J[0], self.i[0], self.j[0]],[LEFT, DOWN*2,RIGHT] ):
			coords= Matrix(j).add_background_rectangle()
			coords.scale(VECTOR_LABEL_SCALE_FACTOR)
			coords.next_to(l.get_end(), np.sign(k)*m)
			self.play(Write(coords, run_time = 1))

			if l==v:
				self.wait(2)
				self.show_linear_combination(i_tilde,j_tilde)

			self.wait()
			self.play(FadeOut(coords))

		block=FullScreenRectangle(opacity=.5)
		self.play(Write(block))
		#text=TexMobject("\\left")
		#self.play(Write(text))







	def show_linear_combination(self, base1,base2,clean_up = True):
		[m.save_state() for m in [base1,base2]]
		#i_hat_copy, j_hat_copy = [m.copy().fade(0.3) for m in (base1, base2)]
		self.play(ApplyFunction(
			lambda m : m.scale(self.v_coords_J[0], about_point=m.get_start()),
			base1
		))
		self.play(ApplyMethod(base2.shift, base1.get_end()))
		self.play(ApplyFunction(
			lambda m : m.scale(self.v_coords_J[1], about_point=m.get_start()),
			base2
		))
		
		self.wait(2)
		if clean_up:
			self.play(*[m.restore for m in [base1,base2]])
		
