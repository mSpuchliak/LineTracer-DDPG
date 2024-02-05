from Scenes.circle_scene import CircleScene
from Scenes.curve_scene import CurveScene
from Scenes.wobbly_scene import WobblyScene
from Scenes.elipse_scene import ElipseScene

class SceneFactory():
    def choose_scene(self, scene_name):
        if (scene_name == 'Circle'):
            return CircleScene()
        elif (scene_name == 'Elipse'):
            return ElipseScene()
        elif (scene_name == 'Wobbly'):
            return WobblyScene()
        elif (scene_name == 'Curve'):
            return CurveScene()