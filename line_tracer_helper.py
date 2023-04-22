from settings import STARTING_POSITION, CHECKPOINT_1, CHECKPOINT_2, CHECKPOINT_3

class LineTracerHelper:
    def __init__(self) -> None:
        self.reward = 0
        self.wrong_way_counter = 0
        self.num_of_laps = 0
        self.laps_history = []
        self.checkpoint_1_done = False
        self.checkpoint_2_done = False
        self.checkpoint_3_done = False
        self.round_done = False
        self.going_backwards_reward = -10
        self.both_sensor_reward = 80
        self.one_sensor_reward = 1
        self.off_track_reward = -5
        self.completed_round_reward = 400
        self.failed_to_complete_reward = -400
    
    def calc_reward(self, correct_rows_count_l, correct_rows_count_r):

        if(correct_rows_count_l > 8 and correct_rows_count_r > 8):
            self.reward = self.both_sensor_reward
            self.wrong_way_counter = 0

        elif(correct_rows_count_l > 8 or correct_rows_count_r > 8):
            self.reward = self.one_sensor_reward
            self.wrong_way_counter = 0

        else:
            self.reward = self.off_track_reward
            self.wrong_way_counter += 1

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
    
    def check_wrong_way(self):
        if(self.wrong_way_counter == 400):
            self.wrong_way_counter = 0
            self.reward = self.failed_to_complete_reward
            self.checkpoint_1_done = False
            self.checkpoint_2_done = False
            self.checkpoint_3_done = False
            self.laps_history.append(0)
            self.num_of_laps = 0
            
            return True
        else:
            return False

    def check_checkpoints(self, position):
        if(position[0] > CHECKPOINT_1[0]):
            self.checkpoint_1_done = True

        if(position[1] < CHECKPOINT_2[1] and self.checkpoint_1_done):
            self.checkpoint_2_done = True

        if(position[0] < CHECKPOINT_3[0] and self.checkpoint_1_done and self.checkpoint_2_done):
            self.checkpoint_3_done = True

        if(position[1] > STARTING_POSITION[1] and self.checkpoint_1_done and self.checkpoint_2_done and self.checkpoint_3_done):
            self.checkpoint_1_done = False
            self.checkpoint_2_done = False
            self.checkpoint_3_done = False
            self.num_of_laps += 1
            self.laps_history.append(1)
            self.reward = self.completed_round_reward
            self.round_done = True
    
    def check_going_backwards(self, orientation, position):
        if(position[0] < 0 and position[1] < 0):
            if(orientation[0] > 0 or orientation[1] > 0):
                pass
            else:
                self.reward = self.going_backwards_reward
                self.checkpoint_1_done = False
                self.checkpoint_2_done = False
                self.checkpoint_3_done = False
        
        if(position[0] < 0 and position[1] > 0):
            if(orientation[0] > 0 or orientation[1] < 0):
                pass
            else:
                self.reward = self.going_backwards_reward
                self.checkpoint_1_done = False
                self.checkpoint_2_done = False
                self.checkpoint_3_done = False
        
        if(position[0] > 0 and position[1] > 0):
            if(orientation[0] < 0 or orientation[1] < 0):
                pass
            else:
                self.reward = self.going_backwards_reward
                self.checkpoint_1_done = False
                self.checkpoint_2_done = False
                self.checkpoint_3_done = False
        if(position[0] > 0 and position[1] < 0):
            if(orientation[0] < 0 or orientation[1] > 0):
                pass
            else:
                self.reward = self.going_backwards_reward
                self.checkpoint_1_done = False
                self.checkpoint_2_done = False
                self.checkpoint_3_done = False

    def check_sensor_malfunction(self, sum_correct_rows, sum_correct_rows_new):
        if(sum_correct_rows == 0 and sum_correct_rows_new > 15):
            return True
        else:
            return False
