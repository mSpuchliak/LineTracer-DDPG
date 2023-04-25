from pyrep import PyRep
from pyrep.robots.mobiles.line_tracer import LineTracer
from pyrep.objects.vision_sensor import VisionSensor
from agent import Agent
from line_tracer_helper import LineTracerHelper
from settings import SCENE_FILE, STARTING_POSITION

def main():
    pr = PyRep()
    pr.launch(SCENE_FILE, headless=False)
    pr.start()

    agent = Agent()
    robot = LineTracer()
    robot_helper = LineTracerHelper()

    left_sensor_object = robot.get_object('LeftSensor')
    right_sensor_object = robot.get_object('RightSensor')
    left_sensor = VisionSensor(left_sensor_object.get_handle())
    right_sensor = VisionSensor(right_sensor_object.get_handle())

    done = False
    new_state = []
    correct_rows_count_l_new = 0
    correct_rows_count_r_new = 0

    while not done:
        # STATE
        left_sensor_state = left_sensor.capture_rgb()
        right_sensor_state = right_sensor.capture_rgb()        

        lstate = robot_helper.normalize_state(left_sensor_state)
        rstate = robot_helper.normalize_state(right_sensor_state)

        correct_rows_count_l = robot_helper.calc_correct_rows(left_sensor_state)
        correct_rows_count_r = robot_helper.calc_correct_rows(right_sensor_state)

        sum_correct_rows = correct_rows_count_l + correct_rows_count_r
        sum_correct_rows_new = correct_rows_count_l_new + correct_rows_count_r_new
        
        orientation = robot.get_orientation().tolist()
        position = robot.get_pose()

        state = lstate + rstate + [orientation[0], orientation[1]] + [position[0], position[1]]

        if(robot_helper.check_sensor_malfunction(sum_correct_rows, sum_correct_rows_new)):
            state = new_state
            correct_rows_count_l = correct_rows_count_l_new
            correct_rows_count_r = correct_rows_count_r_new

        # ACTION
        action = agent.get_action(state)

        command = robot_helper.create_command(action)
        robot.set_joint_target_velocities(command)
        pr.step()

        # NEW STATE
        left_sensor_state = left_sensor.capture_rgb()
        right_sensor_state = right_sensor.capture_rgb()

        lstate = robot_helper.normalize_state(left_sensor_state)
        rstate = robot_helper.normalize_state(right_sensor_state)

        correct_rows_count_l_new = robot_helper.calc_correct_rows(left_sensor_state)
        correct_rows_count_r_new = robot_helper.calc_correct_rows(right_sensor_state)
        sum_correct_rows_new = correct_rows_count_l_new + correct_rows_count_r_new

        orientation = robot.get_orientation().tolist()
        position = robot.get_pose()

        new_state = lstate + rstate + [orientation[0], orientation[1]] + [position[0], position[1]]

        if(robot_helper.check_sensor_malfunction(sum_correct_rows_new, sum_correct_rows)):
            new_state = state
            correct_rows_count_l_new = correct_rows_count_l
            correct_rows_count_r_new = correct_rows_count_r

        robot_helper.check_checkpoints(position)
        
        # REWARD
        robot_helper.calc_reward(correct_rows_count_l_new, correct_rows_count_r_new)

        robot_helper.check_going_backwards(orientation, position)

        if(robot_helper.check_wrong_way()):
            robot.set_pose(STARTING_POSITION)
            agent.replay_memory() 
            agent.check_plot(robot_helper.laps_history)
        
        # CALCULATION OF BELLMAN
        print(robot_helper.reward, robot.get_orientation(),  position[0], position[1])
        agent.target_memory(state, action, robot_helper.reward, new_state)

        if(robot_helper.round_done):
            robot.set_pose(STARTING_POSITION)
            agent.replay_memory()
            agent.check_plot(robot_helper.laps_history)
            robot_helper.round_done = False

    pr.stop()
    pr.shutdown()

if __name__ == "__main__":
    main()