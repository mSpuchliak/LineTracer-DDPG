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

        self.reward = 0
        

        self.correct_rows_count_l = 0
        self.correct_rows_count_r = 0
        self.correct_rows_count_l_new = 0
        self.correct_rows_count_r_new = 0

        self.left_sensor_state = []
        self.right_sensor_state = []

        self.iteration_counter = 0
        self.iteration_incrementer = 0.1
        self.iteration_counter_max = 100

        

    def prepeare_for_next_iter(self):
        
        
        # Reseting position and ploting if robot has ended it's round
        if(self.reward_asigner.check_round_done()):
            self.set_pose(self.scene.starting_position)
            self.iteration_counter = 0
            self.finished_rounds_count += 1
        
        self.check_if_model_finished()
    
    
            