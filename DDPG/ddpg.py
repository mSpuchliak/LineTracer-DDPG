from Abstract.algorithm import Algorithm
from DDPG.agent import Agent
from Utilities.line_tracer import LineTracerModel
from DDPG.reward_assigner_ddpg import RewardAsignerDDPG
from Utilities.state_assigner import StateAssigner
from DDPG.iteration_counter import IterationCounter

class DDPG(Algorithm):
    def start(self):
        self.pyrep.launch(self.scene.name, headless=False)
        self.pyrep.start()

        self.finished_rounds_count = 0 
        self.done = False

        model = LineTracerModel()
        state_assigner = StateAssigner()
        iteration_counter = IterationCounter()
        self.reward_assigner = RewardAsignerDDPG(self.scene)
        
        agent = Agent(alpha=0.0001, beta=0.001, input_dims=[517], tau=0.001,
                        batch_size=64, fc1_dims=400, fc2_dims=300, n_actions=2)
        
        #agent.load_model()
        agent.noise.reset()        

        while not self.done:
            # STATE
            robot_data = model.get_robot_data()
            norm_iteration_counter = iteration_counter.get_norm_iteration_counter()
            state = state_assigner.create_state(robot_data, norm_iteration_counter)

            # ACTION
            action_l, action_r = agent.choose_action(state)

            scaled_action_l, scaled_action_r = agent.scale_action(action_l, action_r)

            command = [scaled_action_l, scaled_action_r]

            model.set_joint_target_velocities(command)
            self.pyrep.step()

            # NEW STATE
            robot_data = model.get_robot_data()
            new_state = state_assigner.create_new_state(robot_data, norm_iteration_counter)

            # REWARD
            reward = self.reward_assigner.get_reward(robot_data, command, iteration_counter)

            # LEARNING
            #print(command[0],command[1], reward)

            agent.remember(state, [action_l, action_r], reward, new_state)
            agent.learn()

            # Prepearment for next iteration
            iteration_counter.update_iteration_counter()

            if(self.reward_assigner.check_round_done()):
                model.reset_robot_position(self.scene.starting_position)
                iteration_counter.reset_iteration_counter()
                self.finished_rounds_count += 1
            
            self.check_if_model_finished()
                
        agent.save_model()
        self.pyrep.stop()
        self.pyrep.shutdown()
    
    def check_if_model_finished(self):
        if (self.finished_rounds_count == 500):
            self.done = True
            self.reward_assigner.save_graph()