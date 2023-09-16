from algorithm_factory import AlgorithmFactory

def main():
    algorithm = AlgorithmFactory()
    algorithm.choose_algorithm('ActorCritic')
    
if __name__ == "__main__":
    main()