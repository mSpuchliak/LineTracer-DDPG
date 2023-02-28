from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.mobiles.line_tracer import LineTracer
from pyrep.objects.vision_sensor import VisionSensor
from agent import Agent

SCENE_FILE = join(dirname(abspath(__file__)), 'scenes/scene_LineTracerLua.ttt')
#STARTING_POSITION = [-0.23075932,  0.82499611,  0.02054373, -0.37992865, -0.59636891, -0.3799291 ,  0.59636581]
STARTING_POSITION = [-1.1307591199874878, 0.5999963283538818, 0.027543731033802032, 0.29883480072021484, -0.6408583521842957, 0.2988368570804596, 0.6408547759056091]
SsTARTING_POSITION = [-0.2307, -0.825, 0.026846]
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
    state = [leftSensorState.flat[0], rightSensorState.flat[0]]
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

    if(leftSensorState.flat[0] == 1 and rightSensorState.flat[0] == 1):
        reward = 10
        wrongWayCounter = 0
    elif(leftSensorState.flat[0] == 1 or rightSensorState.flat[0] == 1):
        reward = 1
        wrongWayCounter = 0
    else:
        reward = -1
        wrongWayCounter += 1
    
    if(wrongWayCounter == 400):
        robot.set_pose(STARTING_POSITION)
        agent.replayMemory()
        wrongWayCounter = 0
        reward = -20

    leftSensorState = leftSensor.capture_rgb()
    rightSensorState = rightensor.capture_rgb()
    newState = [leftSensorState.flat[0], rightSensorState.flat[0]]
    agent.targetMemory(state, action, reward, newState)

    pr.step()

pr.stop()
pr.shutdown()
