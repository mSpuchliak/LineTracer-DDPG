from Scenes.circle_scene import CircleScene
from Scenes.curve_scene import CurveScene
from Scenes.human_scene import HumanScene

class SceneFactory():
    def create_scene(self, scene_name):
        if (scene_name == 'Circle'):
            return CircleScene()

        if (scene_name == 'Human'):
            return HumanScene()
        
        if (scene_name == 'Curve'):
            return CurveScene()