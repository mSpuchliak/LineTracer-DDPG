from pyrep.robots.mobiles.mobile_base import MobileBase
from pyrep.objects.vision_sensor import VisionSensor
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape

class LineTracerModel(MobileBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 2, 'LineTracer')

        left_sensor_object = self.get_object('LeftSensor')
        right_sensor_object = self.get_object('RightSensor')
        #proximity_sensor_front_object = self.get_object('ProximitySensorFront')
        #proximity_sensor_left_object = self.get_object('ProximitySensorLeft')
        #proximity_sensor_right_object = self.get_object('ProximitySensorRight')

        # self.proximity_sensor_front = ProximitySensor(proximity_sensor_front_object.get_handle())
        # self.proximity_sensor_left = ProximitySensor(proximity_sensor_left_object.get_handle())
        # self.proximity_sensor_right = ProximitySensor(proximity_sensor_right_object.get_handle())
        self.left_sensor = VisionSensor(left_sensor_object.get_handle())
        self.right_sensor = VisionSensor(right_sensor_object.get_handle())

        #cuboid_obejct = self.get_object('Cuboid')
        #self.cuboid = Shape(cuboid_obejct.get_handle())
       
        self.state = []
        self.new_state = []

        self.correct_rows_count_l = 0
        self.correct_rows_count_r = 0
        self.correct_rows_count_l_new = 0
        self.correct_rows_count_r_new = 0

        self.left_sensor_state = []
        self.right_sensor_state = []

    # Getting value pixels of sensors
    def get_state(self, iter_counter):
        self.left_sensor_state = self.left_sensor.capture_rgb()
        self.right_sensor_state = self.right_sensor.capture_rgb()        

        lstate = self.normalize_state(self.left_sensor_state)
        rstate = self.normalize_state(self.right_sensor_state)

        self.orientation = self.get_orientation().tolist()
        self.position = self.get_pose()

        return lstate + rstate + [self.orientation[0], self.orientation[1]] + [self.position[0], self.position[1]] + [iter_counter]
    
    # Setting state and count of correct rows for both of sensors
    def set_state(self, iter_counter):
        self.state = self.get_state(iter_counter)

        self.correct_rows_count_l = self.calc_correct_rows(self.left_sensor_state)
        self.correct_rows_count_r = self.calc_correct_rows(self.right_sensor_state)

        if(self.check_sensor_malfunction()):
            self.state = self.new_state
            self.correct_rows_count_r  = self.correct_rows_count_r_new
            self.correct_rows_count_l = self.correct_rows_count_l_new 
    
    # Setting new state and count of correct rows for both of sensors
    def set_new_state(self, iter_counter):
        self.new_state = self.get_state(iter_counter)

        self.correct_rows_count_l_new = self.calc_correct_rows(self.left_sensor_state)
        self.correct_rows_count_r_new = self.calc_correct_rows(self.right_sensor_state)

        if(self.check_sensor_malfunction_new()):
            self.new_state = self.state
            self.correct_rows_count_r_new  = self.correct_rows_count_r
            self.correct_rows_count_l_new = self.correct_rows_count_l 

    # Normalization of states.
    def normalize_state(self, sensor_state):
        state = []
        for rows in sensor_state:
            for pixel in rows:
                if(pixel[0] == 1.0):
                    state.append(1)
                else:
                    state.append(0)
        return state

    # Calculation of pixels that returned red color, and returning count of rows that had more red pixels than a certain threshold.
    def calc_correct_rows(self, sensor_state):
        rows_evaluation = []

        for rows in sensor_state:
            row_evaluation = 0
            
            for pixel in rows:
                row_evaluation += pixel[0]
            rows_evaluation.append(row_evaluation)
        
        correct_rows_count = 0
        
        for row in rows_evaluation:
            if(row > 15):
                correct_rows_count += 1

        return correct_rows_count
    
    # Check for malfunction of sensors, for state.
    def check_sensor_malfunction(self):
        if(self.correct_rows_count_l + self.correct_rows_count_r == 0 and self.correct_rows_count_l_new + self.correct_rows_count_r_new > 20):
            return True
        else:
            return False
        
    # Check for malfunction of sensors, for new state.
    def check_sensor_malfunction_new(self):
        if(self.correct_rows_count_l_new + self.correct_rows_count_r_new == 0 and self.correct_rows_count_l + self.correct_rows_count_r > 20):
            return True
        else:
            return False