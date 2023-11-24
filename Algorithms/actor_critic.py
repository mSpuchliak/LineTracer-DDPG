from pyrep import PyRep
from generic_agent import Agent
from scene_factory import SceneFactory
from line_tracer import LineTracerModel
from line_tracer_helper import LineTracerHelper
import torch as T
from statistics import mean

class ActorCritic():
    def start(self):
        sceneFactory = SceneFactory()
        scene = sceneFactory.create_scene('Curve')
        
        pr = PyRep()
        pr.launch(scene.name, headless=False)
        pr.start()

        agent = Agent(alpha=0.0001, beta=0.001, 
                    input_dims=[517], tau=0.001,
                    batch_size=64, fc1_dims=400, fc2_dims=300, 
                    n_actions=2)

        agent.noise.reset()

        robot_helper = LineTracerHelper(scene)
        robot = LineTracerModel()   

        done = False
        iter_counter = 0

        while not done:
            # STATE
            robot.set_state(iter_counter)

            # ACTION
            action_l, action_r = agent.choose_action(robot.state)

            command2 = [action_l, action_r]

            sigmoid_output = T.sigmoid(T.tensor(action_l))
            scaled_output = 4 * sigmoid_output + 1

            sigmoid_outputr = T.sigmoid(T.tensor(action_r))
            scaled_outputr = 4 * sigmoid_outputr + 1

            command = [scaled_output, scaled_outputr]

            robot.set_joint_target_velocities(command)
            pr.step()

            # NEW STATE
            robot.set_new_state(iter_counter)

            # REWARD

            robot_helper.check_state(robot.correct_rows_count_l_new, robot.correct_rows_count_r_new)

            robot_helper.check_going_backwards(robot.orientation, robot.position)

            robot_helper.check_checkpoints(robot.position)

            robot_helper.check_wrong_way()

            robot_helper.speed_check(command)

            
            
            robot_helper.reward = robot_helper.reward - iter_counter

            #print(command[0],command[1], robot_helper.reward)

            agent.remember(robot.state, command2, robot_helper.reward, robot.new_state)
            agent.learn()

            iter_counter += 0.1

            if(robot_helper.round_done):
                robot.set_pose(scene.starting_position)
                robot_helper.round_done = False
                robot_helper.speed_history.append(mean(robot_helper.lap_speed_history))
                robot_helper.lap_speed_history.clear

                iter_counter = 0
                agent.plot_laps_and_speed(robot_helper.speed_history, robot_helper.laps_history)

        pr.stop()
        pr.shutdown()