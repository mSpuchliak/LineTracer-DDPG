from pyrep import PyRep
from generic_agent import GenericAgent, MADDPGAgent
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
        
        agent = MADDPGAgent(516, 2)
        agent2 = MADDPGAgent(516, 2)

        robot_helper = LineTracerHelper(scene)
        robot = LineTracerModel()

        done = False
        while not done:
            # STATE
            robot.set_state()

            # ACTION
            #action = agent.select_action(robot.state)

            action_l = agent.select_action(robot.state)
            action_r = agent2.select_action(robot.state)

            action_l = action_l + 2
            action_r = action_r + 2

            #command = robot_helper.create_command(action)

            # setting command to the wheels
            #robot.set_joint_target_velocities(command)
            command = [action_r, action_l]
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

            # CALCULATION OF BELLMAN
            agent.update(robot.state, action_l, robot_helper.reward, robot.new_state)
            agent2.update(robot.state, action_r, robot_helper.reward, robot.new_state)

            if(robot_helper.round_done):
                robot.set_pose(scene.starting_position)
                #agent.check_plot(robot_helper.laps_history)
                robot_helper.round_done = False

        pr.stop()
        pr.shutdown()