class StateAssigner:
    def __init__(self):
        self.state = []
        self.new_state = []
        self.robot_data = None

        self.correct_rows_count_l = 0
        self.correct_rows_count_r = 0
        self.correct_rows_count_l_new = 0
        self.correct_rows_count_r_new = 0

    def build_state(self):
        lstate = self.normalize_state(self.robot_data.left_sensor_state)
        rstate = self.normalize_state(self.robot_data.right_sensor_state)

        return lstate + rstate + [self.robot_data.orientation[0], self.robot_data.orientation[1]] + [self.robot_data.position[0], self.robot_data.position[1]]
    
    # Setting state and count of correct rows for both of sensors
    def create_state(self, robot_data):
        self.robot_data = robot_data
        self.state = self.build_state()

        self.correct_rows_count_l = self.calc_correct_rows(self.robot_data.left_sensor_state)
        self.correct_rows_count_r = self.calc_correct_rows(self.robot_data.right_sensor_state)

        if(self.check_sensor_malfunction()):
            self.state = self.new_state
            self.correct_rows_count_r  = self.correct_rows_count_r_new
            self.correct_rows_count_l = self.correct_rows_count_l_new 
        
        return self.state
    
    # Setting new state and count of correct rows for both of sensors
    def create_new_state(self, robot_data):
        self.robot_data = robot_data
        self.new_state = self.build_state()

        self.correct_rows_count_l_new = self.calc_correct_rows(self.robot_data.left_sensor_state)
        self.correct_rows_count_r_new = self.calc_correct_rows(self.robot_data.right_sensor_state)

        if(self.check_sensor_malfunction_new()):
            self.new_state = self.state
            self.correct_rows_count_r_new  = self.correct_rows_count_r
            self.correct_rows_count_l_new = self.correct_rows_count_l 
        
        robot_data.correct_rows_count_l_new = self.correct_rows_count_l_new
        robot_data.correct_rows_count_r_new = self.correct_rows_count_r_new
        
        return self.new_state

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
        