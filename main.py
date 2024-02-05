from Factories.algorithm_factory import AlgorithmFactory
from Factories.scene_factory import SceneFactory

def main():
    scene_factory = SceneFactory()
    scene = scene_factory.choose_scene('Wobbly')

    algorithm_factory = AlgorithmFactory(scene)
    algorithm = algorithm_factory.choose_algorithm('DDPG')

    algorithm.start()
    
if __name__ == "__main__":
    main()