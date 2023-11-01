from pyrep import PyRep
from generic_agent import MADDPGAgent, Agent
from scene_factory import SceneFactory
from line_tracer import LineTracerModel
from line_tracer_helper import LineTracerHelper

class ActorCritic():
    def start(self):
        sceneFactory = SceneFactory()
        scene = sceneFactory.create_scene('Circle')
        
        pr = PyRep()
        pr.launch(scene.name, headless=False)
        pr.start()
        
        # agent = MADDPGAgent(516, 2)
        # agent2 = MADDPGAgent(516, 2)

        agent = Agent(alpha=0.0001, beta=0.001, 
                    input_dims=[516], tau=0.001,
                    batch_size=64, fc1_dims=400, fc2_dims=300, 
                    n_actions=1)

        agent2 = Agent(alpha=0.0001, beta=0.001, 
                    input_dims=[516], tau=0.001,
                    batch_size=64, fc1_dims=400, fc2_dims=300, 
                    n_actions=1)
        
        agent.noise.reset()
        agent2.noise.reset()

        robot_helper = LineTracerHelper(scene)
        robot = LineTracerModel()

        done = False
        while not done:
            # STATE
            robot.set_state()

            # ACTION
            action_l = agent.choose_action(robot.state)
            action_r = agent2.choose_action(robot.state)

            action_l2 = action_l + 2
            action_r2 = action_r + 2

            # setting command to the wheels
            command = [action_r2, action_l2]
            print(command)

            robot.set_joint_target_velocities(command)
            pr.step()

            # NEW STATE
            robot.set_new_state()

            # REWARD
            robot_helper.check_checkpoints(robot.position)

            robot_helper.check_state(robot.correct_rows_count_l_new, robot.correct_rows_count_r_new)

            robot_helper.check_going_backwards(robot.orientation, robot.position)

            robot_helper.check_wrong_way()

            agent.remember(robot.state, action_l, robot_helper.reward, robot.new_state, done)
            agent.learn()

            agent.remember(robot.state, action_r ,robot_helper.reward, robot.new_state, done)
            agent.learn()

            if(robot_helper.round_done):
                robot.set_pose(scene.starting_position)
                agent.check_plot(robot_helper.laps_history)
                robot_helper.round_done = False

        pr.stop()
        pr.shutdown()