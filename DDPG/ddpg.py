from Abstract.algorithm import Algorithm
from Utilities.line_tracer import LineTracerModel
from Utilities.state_assigner import StateAssigner
from Utilities.round_settings import RoundSettings
from DDPG.reward_assigner_ddpg import RewardAsignerDDPG
from DDPG.agent import Agent
from DDPG.iteration_counter import IterationCounter

class DDPG(Algorithm):
    def __init__(self, scene):
        super().__init__(scene)
        self.round_settings = RoundSettings()
        self.iteration_counter = IterationCounter()
        self.state_assigner = StateAssigner()
        self.reward_assigner = RewardAsignerDDPG(scene, self.round_settings)
        self.agent = Agent(alpha=0.0001, beta=0.001, input_dims=[517], tau=0.001,
                        batch_size=64, fc1_dims=400, fc2_dims=300, n_actions=2)


    def start(self):
        self.pyrep.launch(self.scene.name, headless=False)
        self.pyrep.start()

        model = LineTracerModel()
        
        #agent.load_model()
        self.agent.noise.reset()        

        while not self.round_settings.done:
            # STATE
            robot_data = model.get_robot_data()
            norm_iteration_counter = self.iteration_counter.get_norm_iteration_counter()
            state = self.state_assigner.create_state(robot_data, norm_iteration_counter)

            # ACTION
            action_l, action_r = self.agent.choose_action(state)

            scaled_action_l, scaled_action_r = self.agent.scale_action(action_l, action_r)

            command = [scaled_action_l, scaled_action_r]

            model.set_joint_target_velocities(command)
            self.pyrep.step()

            # NEW STATE
            robot_data = model.get_robot_data()
            new_state = self.state_assigner.create_new_state(robot_data, norm_iteration_counter)

            # REWARD
            reward = self.reward_assigner.get_reward(robot_data, command, self.iteration_counter)

            # LEARNING
            #print(command[0],command[1], reward)

            self.agent.remember(state, [action_l, action_r], reward, new_state)
            self.agent.learn()

            # Prepearment for next iteration
            self.iteration_counter.update_iteration_counter()

            if(self.round_settings.check_round_done()):
                model.reset_robot_position(self.scene.starting_position)
                self.iteration_counter.reset_iteration_counter()
                self.round_settings.finished_rounds_count += 1
            
            self.round_settings.check_if_model_finished()
                
        self.agent.save_model()
        self.pyrep.stop()
        self.pyrep.shutdown()
