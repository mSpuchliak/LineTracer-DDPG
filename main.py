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

    while not done:
        left_sensor_state = left_sensor.capture_rgb()
        right_sensor_state = right_sensor.capture_rgb()        

        lstate = agent.normalize_state(left_sensor_state)
        rstate = agent.normalize_state(right_sensor_state)
        orientation = robot.get_orientation().tolist()
        state = lstate + rstate + orientation
        action = agent.get_action(state)

        command = agent.create_command(action)
        robot.set_joint_target_velocities(command)

        correct_rows_count_l = robot_helper.calc_correct_rows(left_sensor_state)
        correct_rows_count_r = robot_helper.calc_correct_rows(right_sensor_state)

        robot_helper.calc_reward(correct_rows_count_l, correct_rows_count_r)

        robot_helper.check_going_backwards(robot.get_orientation())

        if(robot_helper.check_wrong_way()):
            robot.set_pose(STARTING_POSITION)
            agent.replay_memory()
            agent.check_plot(robot_helper.laps_history)

        left_sensor_state = left_sensor.capture_rgb()
        right_sensor_state = right_sensor.capture_rgb()

        lstate = agent.normalize_state(left_sensor_state)
        rstate = agent.normalize_state(right_sensor_state)
        orientation = robot.get_orientation().tolist()
        
        print(robot_helper.reward, robot.get_orientation())
        
        newState = lstate + rstate + orientation
        agent.target_memory(state, action, robot_helper.reward, newState)

        position = robot.get_pose()
        robot_helper.check_checkpoints(position)

        pr.step()

    pr.stop()
    pr.shutdown()

if __name__ == "__main__":
    main()