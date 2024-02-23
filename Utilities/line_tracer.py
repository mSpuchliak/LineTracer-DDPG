from pyrep.robots.mobiles.mobile_base import MobileBase
from pyrep.objects.vision_sensor import VisionSensor
from Models.robot_data import RobotData

class LineTracerModel(MobileBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 2, 'LineTracer')

        left_sensor_object = self.get_object('LeftSensor')
        right_sensor_object = self.get_object('RightSensor')

        self.left_sensor = VisionSensor(left_sensor_object.get_handle())
        self.right_sensor = VisionSensor(right_sensor_object.get_handle())

    # Getting value pixels of sensors
    def get_robot_data(self):
        robotData = RobotData()

        robotData.left_sensor_state = self.left_sensor.capture_rgb()
        robotData.right_sensor_state = self.right_sensor.capture_rgb()  
        robotData.orientation = self.get_orientation().tolist()
        robotData.position = self.get_pose()

        return robotData
    
    def reset_robot_position(self, starting_position):
        self.set_pose(starting_position)



 
