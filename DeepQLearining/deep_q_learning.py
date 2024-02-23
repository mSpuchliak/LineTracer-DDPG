from Abstract.algorithm import Algorithm
from DeepQLearining.agent import Agent
from DeepQLearining.line_tracer import LineTracerModel
from DeepQLearining.reward_assigner_dql import RewardAsignerDQL
from Utilities.state_assigner import StateAssigner

class DeepQLearining(Algorithm):
    def start(self):        
        self.pyrep.launch(self.scene.name, headless=False)
        self.pyrep.start()

        self.model = LineTracerModel()

        state_assginer = StateAssigner()
        self.reward_asigner = RewardAsignerDQL(self.scene)  
        
        agent = Agent(input_dims=516, n_actions=3, hidden_dims=2500,
                     batch_size=15,mem_size=100000)
        self.done = False

        while not self.done:
            # STATE
            robot_data = self.model.get_robot_data()
            state = state_assginer.create_state(robot_data)

            # ACTION
            action = agent.get_action(state)
            command = agent.create_command(action)

            # setting command to the wheels
            self.model.set_joint_target_velocities(command)
            self.pyrep.step()

            # NEW STATE
            robot_data = self.model.get_robot_data()
            new_state = state_assginer.create_new_state(robot_data)

            # REWARD
            reward = self.reward_asigner.get_reward(robot_data)

            # CALCULATION OF BELLMAN
            agent.target_memory(state, action, reward, new_state)

            if(self.reward_asigner.check_round_done_dql()):
                agent.replay_memory()
                self.model.reset_robot_position(self.scene.starting_position)

        self.pyrep.stop()
        self.pyrep.shutdown()