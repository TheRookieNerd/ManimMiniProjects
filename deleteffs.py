from manimlib.animation.transform import ApplyMethod
from manimlib.camera.three_d_camera import ThreeDCamera
from manimlib.constants import DEGREES
from manimlib.constants import PRODUCTION_QUALITY_CAMERA_CONFIG
from manimlib.mobject.coordinate_systems import ThreeDAxes
from manimlib.mobject.geometry import Line
from manimlib.mobject.three_dimensions import Sphere
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VectorizedPoint
from manimlib.scene.scene import Scene
from manimlib.utils.config_ops import digest_config
from manimlib.utils.config_ops import merge_dicts_recursively

class ThreeDTest(ThreeDScene):
    def construct(self):
        sphere=Sphere()
        self.begin_vertical_cmaera_rotation()
        self.wait(5)
