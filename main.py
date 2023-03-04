from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.mobiles.line_tracer import LineTracer
from pyrep.objects.vision_sensor import VisionSensor
from agent import Agent
import numpy as np
SCENE_FILE = join(dirname(abspath(__file__)), 'scenes/scene_LineTracerLua.ttt')
#STARTING_POSITION = [-2.9057591 , -2.55000305,  0.02754373,  0.2988348 , -0.64085835,0.29883686,  0.6408549 ] #big
STARTING_POSITION = [-2.45576   ,  1.92499709,  0.02754373,  0.2988348 , -0.64085835, 0.29883686,  0.6408549 ] #klukaty

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
            
        print(reward)

        leftSensorState = leftSensor.capture_rgb()
        rightSensorState = rightensor.capture_rgb()

        lstate = getState(leftSensorState)
        rstate = getState(rightSensorState)

        newState = lstate + rstate
        agent.targetMemory(state, action, reward, newState)

        pr.step()

    pr.stop()
    pr.shutdown()

if __name__ == "__main__":
    main()