from Abstract.scene import Scene
from os.path import dirname, join, abspath

class CurveScene(Scene):
    def __init__(self):
        self.name = join(dirname(dirname(abspath(__file__))), 'Scenes_coppelia/scene_LineTracerCurvy.ttt')
        self.starting_position = [-0.7557606101036072, -0.1000010147690773, 0.027543731033802032, 0.5213239192962646, -0.4777219295501709, 0.5213421583175659, 0.4777086675167084]
        self.checkpoint_1 = [0.04487847164273262, 0.7503286600112915, 0.027609875425696373, -0.02743576653301716, -0.707614541053772, -0.027354635298252106, 0.7055358290672302]
        self.checkpoint_2 = [0.993854820728302, 0.12439827620983124, 0.027609501034021378, 0.5031706094741821, 0.49829116463661194, 0.5017000436782837, -0.49681222438812256]
        self.checkpoint_3 = [-0.056360453367233276, -1.0496164560317993, 0.027609627693891525, 0.7081372141838074, -0.0034498991444706917, 0.7060580253601074, 0.0034560090862214565]