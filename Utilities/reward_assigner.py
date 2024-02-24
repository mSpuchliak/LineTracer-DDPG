class RewardAssigner:
    def __init__(self, scene, round_settings):
        self.scene = scene
        self.round_settings = round_settings

        self.wrong_way_counter = 0
        self.speed = 0

        self.checkpoint_1_done = False
        self.checkpoint_2_done = False
        self.checkpoint_3_done = False
        self.checkpoint_4_done = False

        self.going_backwards_reward = -10
        self.both_sensor_reward = 80
        self.one_sensor_reward = 1
        self.off_track_reward = -5
        self.completed_round_reward = 400
        self.failed_to_complete_reward = -400
        self.reward = 0
    
    # Check for the status of the robot, and assigning a reward for the current status.
    def check_state(self, correct_rows_count_l, correct_rows_count_r):
        if(correct_rows_count_l > 8 and correct_rows_count_r > 8):
            self.wrong_way_counter = 0
            self.reward = self.both_sensor_reward

        elif(correct_rows_count_l > 8 or correct_rows_count_r > 8):
            self.wrong_way_counter = 0
            self.reward = self.one_sensor_reward

        else:
            self.wrong_way_counter += 1
            self.reward = self.off_track_reward
            
    # Check for the position of the robot, if the robot does not go too long in the wrong direction.
    def check_wrong_way(self):
        if(self.wrong_way_counter > 400):
            self.wrong_way_counter = 0
            self.reset_checkpoints()
            self.round_settings.add_to_laps_history(0)
            self.round_settings.round_done = True

            self.reward = self.failed_to_complete_reward

    # Check for the position of the robot, to be able to tell when the robot will pass the whole path.
    def check_checkpoints(self, position):
        if(position[0] > self.scene.checkpoint_1[0]):
            self.checkpoint_1_done = True

        if(position[1] < self.scene.checkpoint_2[1] and self.checkpoint_1_done):
            self.checkpoint_2_done = True

        if(position[0] < self.scene.checkpoint_3[0] and self.checkpoint_1_done and self.checkpoint_2_done):
            self.checkpoint_3_done = True

        if(position[1] > self.scene.starting_position[1] and self.checkpoint_1_done and self.checkpoint_2_done and self.checkpoint_3_done):
            self.checkpoint_4_done = True
            self.reset_checkpoints()
            self.round_settings.add_to_laps_history(1)
            self.round_settings.round_done = True
            self.reward = self.completed_round_reward 
    
    # Check the position and rotation of the robot, if it is not going in the opposite direction.
    def check_going_backwards(self, orientation, position):
        if(position[0] < 0 and position[1] < 0):
            if not(orientation[0] > 0 or orientation[1] > 0):
                self.wrong_way_counter += 1
                self.reset_checkpoints()
                self.reward = self.going_backwards_reward
        
        if(position[0] < 0 and position[1] > 0):
            if not(orientation[0] > 0 or orientation[1] < 0):
                self.wrong_way_counter += 1
                self.reset_checkpoints()
                self.reward = self.going_backwards_reward
        
        if(position[0] > 0 and position[1] > 0):
            if not(orientation[0] < 0 or orientation[1] < 0):
                self.wrong_way_counter += 1
                self.reset_checkpoints()
                self.reward = self.going_backwards_reward

        if(position[0] > 0 and position[1] < 0):
            if not(orientation[0] < 0 or orientation[1] > 0):
                self.wrong_way_counter += 1
                self.reset_checkpoints()
                self.reward = self.going_backwards_reward

    # Reset of checkpoints.
    def reset_checkpoints(self):
        self.checkpoint_1_done = False
        self.checkpoint_2_done = False
        self.checkpoint_3_done = False
        self.checkpoint_4_done = False
    
    def speed_check(self, wheels_speed):
        self.speed = wheels_speed[0] + wheels_speed[1]
        self.round_settings.add_to_speed_history(self.speed.item())

        if(self.reward > self.one_sensor_reward):
            if(self.speed < 4):
                self.reward -= 90
            if(4 < self.speed < 5):
                self.reward -= 60
            if(5 < self.speed < 5.5):
                self.reward -= 30
            elif(5.5 <= self.speed < 6.0):
                self.reward -= 10     
            elif(6 <= self.speed < 6.5):
                self.reward += 30
            elif(6.5 <= self.speed < 7.0):
                self.reward += 50
            elif(7 >= self.speed):
                self.reward += 90

    def get_reward(self):
        return self.reward
