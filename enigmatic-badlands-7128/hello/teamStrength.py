class TeamStrength:
	# home_player_count
	# away_player_count
	# home_penalty_starts_after_goal
	# away_penalty_starts_after_goal
	# home_penalty_ends_after_goal
	# away_penalty_ends_after_goal

	def __init__(self):
		self.home_player_count = 5
		self.away_player_count = 5
		self.home_penalty_starts_after_goal = False
		self.away_penalty_starts_after_goal = False
		self.home_penalty_ends_after_goal = False
		self.away_penalty_ends_after_goal = False

	def away_penalty(self, length):
		if self.away_player_count > 3 and (length != 10 and length != 20) and length != 4:
			self.away_player_count -= 1
		if length == 2:
			self.away_penalty_ends_after_goal = True
		if length == 4:
			self.away_penalty_ends_after_goal = True
			self.away_penalty_starts_after_goal = True

	def home_penalty(self, length):
		if self.home_player_count > 3 and (length != 10 and length != 20) and length != 4:
			self.home_player_count -= 1
		if length == 2:
			self.home_penalty_ends_after_goal = True
		if length == 4:
			self.home_penalty_ends_after_goal = True
			self.home_penalty_starts_after_goal = True

	def away_goal(self): #TODO: assert PP goals
		if self.home_player_count < self.away_player_count and self.home_penalty_ends_after_goal:
			self.home_player_count += 1
			self.home_penalty_starts_after_goal = False

	def home_goal(self):
		if self.home_player_count > self.away_player_count and self.away_penalty_ends_after_goal:
			self.away_player_count += 1
			self.away_penalty_starts_after_goal = False

	def get_away_penalty_starts_after_goal(self):
		return self.away_penalty_starts_after_goal

	def get_home_penalty_starts_after_goal(self):
		return self.home_penalty_starts_after_goal

	def is_home_pp(self):
		return self.home_player_count > self.away_player_count

	def is_away_pp(self):
		return self.away_player_count > self.home_player_count

	def get_team_strength(self):
		if self.is_home_pp():
			return "home_pp"
		if self.is_away_pp():
			return "away_pp"
		return "even"

	def __str__(self):
		string = "Team Strength:\n"
		string += "Home Player Count: " + str(self.home_player_count)
		string += "\nAway Player Count: " + str(self.away_player_count)
		string += "\nHome PEAG: " + str(self.home_penalty_ends_after_goal)
		string += "\nAway PEAG: " + str(self.away_penalty_ends_after_goal)
		string += "\nHome PSAG: " + str(self.home_penalty_starts_after_goal)
		string += "\nAway PSAG: " + str(self.away_penalty_starts_after_goal) + "\n"
		return string