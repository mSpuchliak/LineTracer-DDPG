from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.mobiles.line_tracer import LineTracer
from pyrep.objects.vision_sensor import VisionSensor
from agent import Agent
import numpy as np

SCENE_FILE = join(dirname(abspath(__file__)), 'scenes/scene_LineTracerLua.ttt')
#STARTING_POSITION = [-2.9057591 , -2.55000305,  0.02754373,  0.2988348 , -0.64085835,0.29883686,  0.6408549 ] #big
STARTING_POSITION = [-2.45576   ,  1.92499709,  0.02754373,  0.2988348 , -0.64085835, 0.29883686,  0.6408549 ] #klukaty
CHECKPOINT_1 = [-2.030761,    2.22499752,  0.02754373,  0.12278704 -0.6963675,   0.12278818, 0.69636106]
CHECKPOINT_2 = [-1.10576117,  1.8,  0.02754373, -0.43045604, -0.56099224, -0.43046466, 0.56097722]
CHECKPOINT_3 = [-1.43076015,  1.44999731,  0.02754373 -0.6743784,  -0.21263161, -0.67438203, 0.21263009]
CHECKPOINT_4 = [-2.43076134,  1.29999828,  0.02754373,  0.56097728, -0.43046471,  0.5609923, 0.43045613]

def calcColor(SensorState):
    colorList = []
    for rightStates in SensorState:
        number = 0
        for rightState in rightStates:
            number += rightState[0]
        colorList.append(number)
    
    correctRow = 0
    for row in colorList:
        if(row > 15):
            correctRow += 1
    return correctRow

def getState(sensorState):
    state = []
    for row in sensorState:
        for col in row:
            if(col[0] == 1.0):
                state.append(1)
            else:
                state.append(0)
    return state

def main():
    pr = PyRep()
    pr.launch(SCENE_FILE, headless=False)
    pr.start()

    agent = Agent()
    robot = LineTracer()

    leftSensorObject = robot.get_object('LeftSensor')
    rightSensorObject = robot.get_object('RightSensor')
    leftSensor = VisionSensor(leftSensorObject.get_handle())
    rightensor = VisionSensor(rightSensorObject.get_handle())

    done = False
    reward = 0
    wrongWayCounter = 0

    checkpoint_1_done = False
    checkpoint_2_done = False
    checkpoint_3_done = False
    checkpoint_4_done = False
    num_of_laps = 0
    laps_history = []

    while not done:
        leftSensorState = leftSensor.capture_rgb()
        rightSensorState = rightensor.capture_rgb()        

        lstate = getState(leftSensorState)
        rstate = getState(rightSensorState)

        state = lstate + rstate
        action = agent.getAction(state)

        if action == 0:
            commnad = [1, 0]
        elif action == 1:
            commnad = [0, 1]
        elif action == 2:
            commnad = [1, 1]
        else:
            print("Wrong input of a action.")

        robot.set_joint_target_velocities(commnad)

        colorValLeft = calcColor(leftSensorState)
        colorValRight = calcColor(rightSensorState)

        if(colorValLeft > 8 and colorValRight > 8):
            reward = 80
            wrongWayCounter = 0
        elif(colorValLeft > 8 or colorValRight > 8):
            reward = 1
            wrongWayCounter = 0
        else:
            reward = -1
            wrongWayCounter += 1
        
        if(wrongWayCounter == 400):
            robot.set_pose(STARTING_POSITION)
            agent.replayMemory()
            wrongWayCounter = 0
            reward = -800
            checkpoint_1_done = False
            checkpoint_2_done = False
            checkpoint_3_done = False
            checkpoint_4_done = False
            
            laps_history.append(num_of_laps)
            agent.check_plot(laps_history)
            num_of_laps = 0


        leftSensorState = leftSensor.capture_rgb()
        rightSensorState = rightensor.capture_rgb()

        lstate = getState(leftSensorState)
        rstate = getState(rightSensorState)

        newState = lstate + rstate
        agent.targetMemory(state, action, reward, newState)

        position = robot.get_pose()

        if(position[0] > CHECKPOINT_1[0]):
            checkpoint_1_done = True
        if(position[1] < CHECKPOINT_2[1] and checkpoint_1_done):
            checkpoint_2_done = True
        if(position[0] < CHECKPOINT_3[0] and checkpoint_1_done and checkpoint_2_done):
            checkpoint_3_done = True
        if(position[1] > CHECKPOINT_4[1] and checkpoint_1_done and checkpoint_2_done and checkpoint_3_done):
            checkpoint_1_done = False
            checkpoint_2_done = False
            checkpoint_3_done = False
            checkpoint_4_done = False
            num_of_laps += 1

        pr.step()

    pr.stop()
    pr.shutdown()

if __name__ == "__main__":
    main()