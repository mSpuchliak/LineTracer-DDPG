from pyrep import PyRep
from agent import Agent
from scene_factory import SceneFactory
from line_tracer import LineTracerModel
from line_tracer_helper import LineTracerHelper

class DeepQLearining():

    def start(self):
        sceneFactory = SceneFactory()
        scene = sceneFactory.create_scene('Curve')
        
        pr = PyRep()
        pr.launch(scene.name, headless=False)
        pr.start()
        
        agent = Agent()
        robot_helper = LineTracerHelper(scene)  
        robot = LineTracerModel()

        done = False
        while not done:
            # STATE
            robot.set_state()

            # ACTION
            action = agent.get_action(robot.state)
            command = robot_helper.create_command(action)

            # setting command to the wheels
            robot.set_joint_target_velocities(command)
            pr.step()

            # NEW STATE
            robot.set_new_state()

            # REWARD
            robot_helper.check_checkpoints(robot.position)

            robot_helper.check_state(robot.correct_rows_count_l_new, robot.correct_rows_count_r_new)

            robot_helper.check_going_backwards(robot.orientation, robot.position)

            #robot_helper.check_proximity(robot)

            robot_helper.check_wrong_way()

            # CALCULATION OF BELLMAN
            agent.target_memory(robot.state, action, robot_helper.reward, robot.new_state)

            if(robot_helper.round_done):
                robot.set_pose(scene.starting_position)
                agent.replay_memory()
                agent.check_plot(robot_helper.laps_history)
                robot_helper.round_done = False

        pr.stop()
        pr.shutdown()