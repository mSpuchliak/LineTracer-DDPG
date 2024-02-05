from Abstract.algorithm import Algorithm
from DDPG.agent import Agent
from DDPG.line_tracer import LineTracerModel

class DDPG(Algorithm):
    def start(self):
        self.pyrep.launch(self.scene.name, headless=False)
        self.pyrep.start()

        self.model = LineTracerModel()
        self.model.set_reward_asigner(self.scene)

        self.agent = Agent(alpha=0.0001, beta=0.001, input_dims=[517], tau=0.001,
                        batch_size=64, fc1_dims=400, fc2_dims=300, n_actions=2)
        
        #self.agent.load_model()
        self.agent.noise.reset()        

        while not self.model.done:
            # STATE
            self.model.set_state()

            # ACTION
            action_l, action_r = self.agent.choose_action(self.model.state)

            scaled_action_l, scaled_action_r = self.agent.scale_action(action_l, action_r)

            command = [scaled_action_l, scaled_action_r]

            self.model.set_joint_target_velocities(command)
            self.pyrep.step()

            # NEW STATE
            self.model.set_new_state()

            # REWARD
            reward = self.model.get_reward(command)

            # LEARNING
            #print(command[0],command[1], reward)

            self.agent.remember(self.model.state, [action_l, action_r], reward, self.model.new_state)
            
            self.agent.learn()

            # Prepearment for next iteration
            self.model.prepeare_for_next_iter()
                
        self.agent.save_model()
        self.pyrep.stop()
        self.pyrep.shutdown()