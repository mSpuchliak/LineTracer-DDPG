from Abstract.algorithm import Algorithm
from DeepQLearining.agent import Agent
from DeepQLearining.reward_assigner_dql import RewardAsignerDQL
from Utilities.line_tracer import LineTracerModel
from Utilities.round_settings import RoundSettings
from Utilities.state_assigner import StateAssigner

class DeepQLearining(Algorithm):
    def __init__(self, scene):
        super().__init__(scene)
        self.round_settings = RoundSettings()
        self.state_assigner = StateAssigner()
        self.reward_asigner = RewardAsignerDQL(self.scene, self.round_settings)  
        self.agent = Agent(input_dims=516, n_actions=3, hidden_dims=2500,
                     batch_size=15,mem_size=100000)
        
    def start(self):        
        self.pyrep.launch(self.scene.name, headless=False)
        self.pyrep.start()

        model = LineTracerModel()

        while not self.round_settings.done:
            # STATE
            robot_data = model.get_robot_data()
            state = self.state_assigner.create_state(robot_data)

            # ACTION
            action = self.agent.get_action(state)
            command = self.agent.create_command(action)

            # setting command to the wheels
            model.set_joint_target_velocities(command)
            self.pyrep.step()

            # NEW STATE
            robot_data = model.get_robot_data()
            new_state = self.state_assigner.create_new_state(robot_data)

            # REWARD
            reward = self.reward_asigner.get_reward(robot_data)

            # CALCULATION OF BELLMAN
            self.agent.target_memory(state, action, reward, new_state)

            if(self.round_settings .check_round_done_dql()):
                self.agent.replay_memory()
                model.reset_robot_position(self.scene.starting_position)

        self.pyrep.stop()
        self.pyrep.shutdown()