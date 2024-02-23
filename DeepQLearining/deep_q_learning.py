from Abstract.algorithm import Algorithm
from DeepQLearining.agent import Agent
from DeepQLearining.line_tracer import LineTracerModel

class DeepQLearining(Algorithm):
    def start(self):        
        self.pyrep.launch(self.scene.name, headless=False)
        self.pyrep.start()

        self.model = LineTracerModel()
        self.model.set_reward_asigner(self.scene)
        
        agent = Agent()
        self.done = False

        while not self.done:
            # STATE
            self.model.set_state()

            # ACTION
            action = agent.get_action(self.model.state)
            command = agent.create_command(action)

            # setting command to the wheels
            self.model.set_joint_target_velocities(command)
            self.pyrep.step()

            # NEW STATE
            self.model.set_new_state()

            # REWARD
            reward = self.model.get_reward()

            # CALCULATION OF BELLMAN
            agent.target_memory(self.model.state, action, reward, self.model.new_state)

            if(self.model.prepeare_for_next_iter()):
                agent.replay_memory()

        self.pyrep.stop()
        self.pyrep.shutdown()