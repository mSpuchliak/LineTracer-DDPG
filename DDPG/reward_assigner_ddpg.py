from Utilities.reward_asigner import RewardAsigner

class RewardAsignerDDPG(RewardAsigner):
    def get_reward(self, robot_data, command, iteration_counter):
        self.check_state(robot_data.correct_rows_count_l_new, robot_data.correct_rows_count_r_new)

        self.check_going_backwards(robot_data.orientation, robot_data.position)

        self.check_checkpoints(robot_data.position)

        self.check_wrong_way()

        self.speed_check(command)

        self.reward -= iteration_counter.value

        return self.reward