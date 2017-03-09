
from data_parser import get_shots_from_source, get_page_source, get_all_match_ids
from .models import Greeting, Shot, Match
import configuration as cfg

def add_shot_to_database(shot, season):
	new_shot = Shot()
	new_shot.shooter = shot['shooter']
	new_shot.x = shot['x']
	new_shot.y = shot['y']
	new_shot.x_plotted = int(shot['x'] / 100 * cfg.SQUARE_COUNT_WIDTH)
	new_shot.y_plotted = int(shot['y'] / 100 * cfg.SQUARE_COUNT_LENGTH)
	new_shot.time_min = shot['time_min']
	new_shot.time_sec = shot['time_sec']
	new_shot.shooting_team = shot['shooting_team']
	new_shot.opposing_team = shot['opposing_team']
	new_shot.outcome = shot['outcome']
	if shot['blocker'] != None:
		new_shot.blocker = shot['blocker']
	if shot['first_assist'] != None:
		new_shot.first_assist = shot['first_assist']
	if shot['second_assist'] != None:
		new_shot.second_assist = shot['second_assist']
	new_shot.season = season
	new_shot.goalie = shot['goalie']
	new_shot.team_strength = shot['team_strength']
	new_shot.save()

def add_match_to_database(match_id, season="2015-2016"):
	print("Adding match: " + str(match_id))
	match_query = Match.objects.all().filter(match_id=match_id, season=season)
	print(match_query)
	if len(match_query) == 0:
		page_source = get_page_source(match_id)
		shots = get_shots_from_source(page_source)

		for shot in shots:
			add_shot_to_database(shot, season)

		new_match = Match()
		new_match.match_id = match_id
		new_match.season = season
		new_match.save()

	else:
		print("Match already added to database")

def add_all_matches_from_season_to_database(season):
	match_ids = get_all_match_ids(season)

	for match_id in match_ids:
		add_match_to_database(match_id, season)