from settings import STARTING_POSITION, CHECKPOINT_1, CHECKPOINT_2, CHECKPOINT_3, CHECKPOINT_4

class LineTracerHelper:
    def __init__(self) -> None:
        self.reward = 0
        self.wrong_way_counter = 0
        self.num_of_laps = 0
        self.laps_history = []
        self.checkpoint_1_done = False
        self.checkpoint_2_done = False
        self.checkpoint_3_done = False
    
    def calc_reward(self, correct_rows_count_l, correct_rows_count_r):
        if(correct_rows_count_l > 8 and correct_rows_count_r > 8):
            self.reward = 80
            self.wrong_way_counter = 0
        elif(correct_rows_count_l > 8 or correct_rows_count_r > 8):
            self.reward = 1
            self.wrong_way_counter = 0
        else:
            self.reward = -1
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
            self.reward = -800
            self.checkpoint_1_done = False
            self.checkpoint_2_done = False
            self.checkpoint_3_done = False
            self.laps_history.append(self.num_of_laps)
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
        if(position[1] > CHECKPOINT_4[1] and self.checkpoint_1_done and self.checkpoint_2_done and self.checkpoint_3_done):
            self.checkpoint_1_done = False
            self.checkpoint_2_done = False
            self.checkpoint_3_done = False
            self.num_of_laps += 1


