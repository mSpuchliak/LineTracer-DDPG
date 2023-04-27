from pyrep.robots.mobiles.mobile_base import MobileBase
from pyrep.objects.vision_sensor import VisionSensor

class LineTracerModel(MobileBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 2, 'LineTracer')

        left_sensor_object = self.get_object('LeftSensor')
        right_sensor_object = self.get_object('RightSensor')
        self.left_sensor = VisionSensor(left_sensor_object.get_handle())
        self.right_sensor = VisionSensor(right_sensor_object.get_handle())
    
        self.state = []
        self.new_state = []

        self.correct_rows_count_l = 0
        self.correct_rows_count_r = 0
        self.correct_rows_count_l_new = 0
        self.correct_rows_count_r_new = 0

        self.left_sensor_state = []
        self.right_sensor_state = []

    def get_state(self):
        self.left_sensor_state = self.left_sensor.capture_rgb()
        self.right_sensor_state = self.right_sensor.capture_rgb()        

        lstate = self.normalize_state(self.left_sensor_state)
        rstate = self.normalize_state(self.right_sensor_state)

        self.orientation = self.get_orientation().tolist()
        self.position = self.get_pose()

        return lstate + rstate + [self.orientation[0], self.orientation[1]] + [self.position[0], self.position[1]]
    
    def set_state(self):
        self.state = self.get_state()

        self.correct_rows_count_l = self.calc_correct_rows(self.left_sensor_state)
        self.correct_rows_count_r = self.calc_correct_rows(self.right_sensor_state)

        if(self.check_sensor_malfunction()):
            self.state = self.new_state
            self.correct_rows_count_r  = self.correct_rows_count_r_new
            self.correct_rows_count_l = self.correct_rows_count_l_new 
    
    def set_new_state(self):
        self.new_state = self.get_state()

        self.correct_rows_count_l_new = self.calc_correct_rows(self.left_sensor_state)
        self.correct_rows_count_r_new = self.calc_correct_rows(self.right_sensor_state)

        if(self.check_sensor_malfunction_new()):
            self.new_state = self.state
            self.correct_rows_count_r_new  = self.correct_rows_count_r
            self.correct_rows_count_l_new = self.correct_rows_count_l 

    def normalize_state(self, sensor_state):
        state = []
        for rows in sensor_state:
            for pixel in rows:
                if(pixel[0] == 1.0):
                    state.append(1)
                else:
                    state.append(0)
        return state

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
    
    def check_sensor_malfunction(self):
        if(self.correct_rows_count_l + self.correct_rows_count_r == 0 and self.correct_rows_count_l_new + self.correct_rows_count_r_new > 15):
            return True
        else:
            return False
    
    def check_sensor_malfunction_new(self):
        if(self.correct_rows_count_l_new + self.correct_rows_count_r_new == 0 and self.correct_rows_count_l + self.correct_rows_count_r > 15):
            return True
        else:
            return False