class LineTracerHelper:
    def __init__(self, scene):
        self.reward = 0
        self.scene = scene
        self.wrong_way_counter = 0
        self.speed = 0

        self.laps_history = []
        self.speed_history = []
        self.lap_speed_history = []

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
        
    
    # Creating a command to be executed by the robot according to the action.
    def create_command(self, action):
        if action == 0:
            command = [1, 0]

        elif action == 1:
            command = [0, 1]

        elif action == 2:
            command = [1, 1]

        else:
            command = [0, 0]

        return command
    
    # Check for the status of the robot, and assigning a reward for the current status.
    def check_state(self, correct_rows_count_l, correct_rows_count_r):

        if(correct_rows_count_l > 8 and correct_rows_count_r > 8):
            self.reward = self.both_sensor_reward
            self.wrong_way_counter = 0

        elif(correct_rows_count_l > 8 or correct_rows_count_r > 8):
            self.reward = self.one_sensor_reward
            self.wrong_way_counter = 0

        else:
            self.reward = self.off_track_reward
            self.wrong_way_counter += 1
    
    # Check for the position of the robot, if the robot does not go too long in the wrong direction.
    def check_wrong_way(self):
        if(self.wrong_way_counter > 400):
            self.wrong_way_counter = 0
            self.reward = self.failed_to_complete_reward
            self.reset_checkpoints()
            self.laps_history.append(0)
            self.round_done = True

    # Check for the position of the robot, to be able to tell when the robot will pass the whole path.
    def check_checkpoints(self, position):
        if(position[0] > self.scene.checkpoint_1[0]):
            self.checkpoint_1_done = True

        if(position[1] < self.scene.checkpoint_2[1] and self.checkpoint_1_done):
            self.checkpoint_2_done = True

        if(position[0] < self.scene.checkpoint_3[0] and self.checkpoint_1_done and self.checkpoint_2_done):
            self.checkpoint_3_done = True

        if(position[1] > self.scene.starting_position[1] and self.checkpoint_1_done and self.checkpoint_2_done and self.checkpoint_3_done):
            self.reset_checkpoints()
            self.laps_history.append(1)
            self.reward = self.completed_round_reward 
            self.round_done = True
    
    # Check the position and rotation of the robot, if it is not going in the opposite direction.
    def check_going_backwards(self, orientation, position):
        if(position[0] < 0 and position[1] < 0):
            if not(orientation[0] > 0 or orientation[1] > 0):
                self.reward = self.going_backwards_reward
                self.wrong_way_counter += 1
                self.reset_checkpoints()
        
        if(position[0] < 0 and position[1] > 0):
            if not(orientation[0] > 0 or orientation[1] < 0):
                self.reward = self.going_backwards_reward
                self.wrong_way_counter += 1
                self.reset_checkpoints()
        
        if(position[0] > 0 and position[1] > 0):
            if not(orientation[0] < 0 or orientation[1] < 0):
                self.reward = self.going_backwards_reward
                self.wrong_way_counter += 1
                self.reset_checkpoints()

        if(position[0] > 0 and position[1] < 0):
            if not(orientation[0] < 0 or orientation[1] > 0):
                self.reward = self.going_backwards_reward
                self.wrong_way_counter += 1
                self.reset_checkpoints()
    
    # Reset of checkpoints.
    def reset_checkpoints(self):
        self.checkpoint_1_done = False
        self.checkpoint_2_done = False
        self.checkpoint_3_done = False

    def check_proximity(self, robot_model):
        p_front = robot_model.proximity_sensor_front.read()
        p_left = robot_model.proximity_sensor_left.read()
        p_right = robot_model.proximity_sensor_right.read()

        if(p_front < 1.5 or p_right < 1.5 or p_left < 1.5):
            self.reward -= 10
            print("Too close to walker" + str(p_front) + "|" + str(p_left) + "|" + str(p_right))

        else:
            print("Good distance")

    def speed_bonus(self):
        return
        if(self.speed > 6.5 and self.speed < 7):
            self.reward += 15

        elif(self.speed > 7 and self.speed < 8):
            self.reward += 50

        elif(self.speed > 8):
            self.reward += 70

    def speed_check(self, wheels_speed):

        self.speed = wheels_speed[0] + wheels_speed[1]
        self.lap_speed_history.append(self.speed.item())

        if(self.reward != self.both_sensor_reward):
            return
        
        self.speed_bonus()

            
