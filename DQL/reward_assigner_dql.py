from Utilities.reward_assigner import RewardAssigner

class RewardAsignerDQL(RewardAssigner):
    def get_reward(self, robot_data):
        self.check_state(robot_data.correct_rows_count_l_new, robot_data.correct_rows_count_r_new)

        self.check_going_backwards(robot_data.orientation, robot_data.position)

        self.check_checkpoints(robot_data.position)

        self.check_wrong_way()

        return self.reward
    