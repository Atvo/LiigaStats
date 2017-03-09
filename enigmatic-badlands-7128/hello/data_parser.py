#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from string import digits

from bs4 import BeautifulSoup

from teamStrength import *


def get_page_source(match_id, season = '2015-2016'):
	response = urllib2.urlopen('http://liiga.fi/ottelut/' + season + '/runkosarja/' + str(match_id) + '/seuranta/')
	html = response.read()
	return html

def get_shots_from_source(page_source):
	team_strength_map = create_penalty_map(page_source)
	soup = BeautifulSoup(page_source, 'html.parser', from_encoding='utf-8')
	table_soup = soup.find('div', class_='table')

	home_team = soup.find('div', class_='home').find('img').get_text().strip()
	away_team = soup.find('div', class_='away').find('img').get_text().strip()

	home_goalie_array, away_goalie_array = create_goalie_map(page_source)

	shots = []
	shots_soup = soup.find_all('div', class_='shot')
	for shot in shots_soup:

		tooltip_id = shot['data-tooltipid']
		shooter, time_min, time_sec, outcome, blocker, first_assist, second_assist = get_shot_details(soup, table_soup, tooltip_id)

		style = shot['style']
		x = float(style.split(";")[0].split(":")[1][1:5]) + 2
		y = float(style.split(";")[1].split(":")[1][1:5]) + 1
		team_strength = team_strength_map[60 * int(time_min) + int(time_sec)].get_team_strength()

		if 'away' in shot['class']:
			x = 100 - x
			y = 100 - y
			shooting_team = away_team
			opposing_team = home_team
			if team_strength is "home_pp":
				team_strength = "shorthanded"
			elif team_strength is "away_pp":
				team_strength = "powerplay"
			else:
				team_strength = "even"
			goalie = get_goalie(home_goalie_array, time_min, time_sec)

		else:
			shooting_team = home_team
			opposing_team = away_team
			if team_strength is "home_pp":
				team_strength = "powerplay"
			elif team_strength is "away_pp":
				team_strength = "shorthanded"
			else:
				team_strength = "even"
			goalie = get_goalie(away_goalie_array, time_min, time_sec)

		#print(team_strength)
		shot_dict = {'shooter': shooter, 'x': x, 'y': y, 'time_min': time_min, 'time_sec': time_sec, 'shooting_team': shooting_team, 'opposing_team': opposing_team, 'outcome': outcome, 'blocker': blocker, 'first_assist': first_assist, 'second_assist': second_assist, 'goalie': goalie, 'team_strength': team_strength}
		shots.append(shot_dict)

	return shots

def get_shot_details(soup, table_soup, tooltip_id):
	tooltip = soup.find('div', class_='tooltip-' + tooltip_id).get_text()
	details = tooltip.split("\n")
	shooter = details[1].split(":")[1][1:]
	time_min = details[3].split(":")[1][1:]
	time_sec = details[3].split(":")[2]
	outcome = details[4].strip()
	blocker = None
	scorer = None
	first_assist = None
	second_assist = None

	if outcome == "Maali":
		outcome = "Goal"
		time_str = str(time_min) + ":" + str(time_sec)
		time_elements = table_soup.find_all('td', class_="time", string=time_str)
		# Doesn't find element if the time is fixed to the summary
		for time_element in time_elements:
			next_element = time_element.find_next_sibling()
			prev_element = time_element.find_previous_sibling()

			if next_element.get_text() != "":
				text = next_element.get_text().strip()
				links = next_element.find_all('a')
				if len(links) != 0:
					scorer = links[0].get_text()
					if len(links) > 1:
						first_assist = links[1].get_text()
						if len(links) > 2:
							second_assist = links[2].get_text()
					break

			if prev_element.get_text() != "":
				links = prev_element.find_all('a')
				if len(links) != 0:
					scorer = links[0].get_text()
					if len(links) > 1:
						first_assist = links[1].get_text()
						if len(links) > 2:
							second_assist = links[2].get_text()
					break


	if outcome == "Maalivahti torjui":
		outcome = "Saved"

	if outcome == "Laukaus ohi maalin":
		outcome = "Missed"

	if outcome == u"Kenttäpelaaja blokkasi":
		outcome = "Blocked"
		blocker = details[6].strip().replace("(", "").replace(")", "")

	return shooter, time_min, time_sec, outcome, blocker, first_assist, second_assist

def get_all_match_ids(season="2015-2016"):
	response = urllib2.urlopen('http://liiga.fi/ottelut/' + season + '/runkosarja/')
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

	match_ids = []

	matches = soup.find_all('a', href=re.compile('/tilastot/'))

	for match in matches:
		href = match['href']
		href_parts = href.split("/")
		if len(href_parts) == 7:
			match_id = href_parts[4]
			match_ids.append(match_id)

	#print(len(match_ids))
	return match_ids

def create_goalie_map(page_source):
	soup = BeautifulSoup(page_source, 'html.parser', from_encoding='utf-8')
	table_soup = soup.find('div', class_='table')
	goalies_anchor = table_soup.find('td', class_='time', string=re.compile('Torjunnat'))
	home_starting_goalie = goalies_anchor.find_previous_sibling().find('a').get_text()
	away_starting_goalie = goalies_anchor.find_next_sibling().find('a').get_text()
	home_backup_goalie = None
	away_backup_goalie = None
	goalies_anchor_parent = goalies_anchor.find_parent()
	backup_goalies_anchor = goalies_anchor_parent.find_next_sibling()

	if backup_goalies_anchor != None:
		home_backup_goalie_soup = backup_goalies_anchor.find('td', class_='home')
		if home_backup_goalie_soup != None:
			home_backup_goalie_soup = home_backup_goalie_soup.find('a')
			if home_backup_goalie_soup != None:
				home_backup_goalie = home_backup_goalie_soup.get_text()
		away_backup_goalie_soup = backup_goalies_anchor.find('td', class_='away')
		if away_backup_goalie_soup != None:
			away_backup_goalie_soup = away_backup_goalie_soup.find('a')
			if away_backup_goalie_soup != None:
				away_backup_goalie = away_backup_goalie_soup.get_text()

	home_goalie_array = [home_starting_goalie]*3900
	away_goalie_array = [away_starting_goalie]*3900

	event_soup = table_soup.find_all('td', class_='time', string=re.compile(r"\d\d:\d\d"))
	for event in event_soup:
		time = event.get_text()
		#print(time)
		home_event_soup = event.find_previous_sibling()
		home_event_text = home_event_soup.get_text()
		away_event_soup = event.find_next_sibling()
		away_event_text = away_event_soup.get_text()

		if 'Maalivahdin vaihto' in home_event_text:
			new_goalie = home_event_soup.find_all('a')[1].get_text()
			home_goalie_array = set_goalie_on_map(new_goalie, time, home_goalie_array)
		
		if 'Maalivahti ulos' in home_event_text:
			new_goalie = "Empty net"
			home_goalie_array = set_goalie_on_map(new_goalie, time, home_goalie_array)
		
		if u'Maalivahti sisään' in home_event_text:
			new_goalie = home_event_soup.find_all('a')[0].get_text()
			home_goalie_array = set_goalie_on_map(new_goalie, time, home_goalie_array)
		
		if 'Maalivahdin vaihto' in away_event_text:
			new_goalie = away_event_soup.find_all('a')[1].get_text()
			away_goalie_array = set_goalie_on_map(new_goalie, time, away_goalie_array)
		
		if 'Maalivahti ulos' in away_event_text:
			new_goalie = "Empty net"
			away_goalie_array = set_goalie_on_map(new_goalie, time, away_goalie_array)
		
		if u'Maalivahti sisään' in away_event_text:
			new_goalie = away_event_soup.find_all('a')[0].get_text()
			away_goalie_array = set_goalie_on_map(new_goalie, time, away_goalie_array)

	return home_goalie_array, away_goalie_array

def set_goalie_on_map(name, time_str, goalie_array):
	minutes = int(time_str.split(":")[0])
	seconds = int(time_str.split(":")[1])
	start_index = minutes * 60 + seconds + 1
	for second in range(start_index, 3900):
		goalie_array[second] = name
	return goalie_array

def get_goalie(map, time_min, time_sec):
	index = int(time_min) * 60 + int(time_sec)
	return map[index]


def create_penalty_map(page_source):
	soup = BeautifulSoup(page_source, 'html.parser', from_encoding='utf-8')
	table_soup = soup.find('div', class_='table')
	team_strength_array = [TeamStrength() for i in range(4200)]
	penalty_array = []

	event_soup = table_soup.find_all('td', class_='time', string=re.compile(r"\d\d:\d\d"))
	for event in event_soup:
		time = event.get_text()
		#print(time)
		time_parts = time.split(":")
		time_idx = int(time_parts[0]) * 60 + int(time_parts[1])
		home_event_soup = event.find_previous_sibling()
		home_event_text = home_event_soup.get_text()
		away_event_soup = event.find_next_sibling()
		away_event_text = away_event_soup.get_text()
		goal_re = re.compile(r"#\d+ .+ \d+-\d+")
		penalty_re = re.compile(r" \d+ min")
		two_min_re = re.compile(r" 2 min")
		five_min_re = re.compile(r" 5 min")
		ten_min_re = re.compile(r" 10 min")
		twenty_min_re = re.compile(r" 20 min")
		player_name_re = re.compile(r"#\d+ .+ \d+ min")
		team_penalty_re = re.compile(r"Joukkuerangaistus \d+ min")
		penalty_text = None
		length = None

		if re.search(goal_re, home_event_text):
			#print("Home Goal")
			penalty_starts = team_strength_array[time_idx].get_away_penalty_starts_after_goal()
			for i in range(time_idx + 1, time_idx + 240):
				team_strength_array[i].home_goal()

			if penalty_starts:
				length = 2
				#print("2 min penalty")

				for i in range(time_idx, time_idx + 120):
					team_strength_array[i].away_penalty(length)

		if re.search(goal_re, away_event_text):
			#print("Away Goal")
			penalty_starts = team_strength_array[time_idx].get_home_penalty_starts_after_goal()
			for i in range(time_idx + 1, time_idx + 240):
				team_strength_array[i].away_goal()
			if penalty_starts:
				
				length = 2
				#print("2 min penalty")

				for i in range(time_idx, time_idx + 120):
					team_strength_array[i].home_penalty(length)


		if re.search(penalty_re, home_event_text):
			#print("Home Penalty")
			team = "Home"
			penalty_text = home_event_text.strip()

		elif re.search(penalty_re, away_event_text):
			#print("Away Penalty")
			team = "Away"
			penalty_text = away_event_text.strip()

		if penalty_text != None:

			##print(re.search(penalty_re, penalty_text).group())
			#print(penalty_text)

			if re.search(team_penalty_re, penalty_text):
				infraction = re.sub(r"Joukkuerangaistus \d+ min", "", penalty_text)
				infraction = infraction.strip()
				player_name = re.search(team_penalty_re, penalty_text).group()

			else:
				infraction = re.sub(r"#\d+ .+ \d+ min", "", penalty_text)
				infraction = infraction.strip()
				player_name = re.search(player_name_re, penalty_text).group()

			player_name = re.sub(r"#\d+ ", "", player_name)
			player_name = re.sub(r" \d+ min", "", player_name)
			#print(player_name)
			if "(" in infraction:
				designee = re.sub(r".+\(", "", infraction)
				designee = re.sub(r"#\d+ ", "", designee)
				designee = designee.replace(")", "")
				#print(designee)
				infraction = re.sub(r"\(.+\)", "", infraction)
			#print(infraction)

			if re.search(two_min_re, penalty_text):

				length = 2

				if [time, player_name, length, infraction] in penalty_array:
					#print("FOUND!!!!!!!!!!!!!!!!!!!!!")
					length = 4
					for i in range(time_idx, time_idx + 120):
						if team == "Home":
							team_strength_array[i].home_penalty(length)
						if team == "Away":
							team_strength_array[i].away_penalty(length)
				
				else:
					length = 2
					#print("2 min penalty")

					for i in range(time_idx, time_idx + 120):
						if team == "Home":
							team_strength_array[i].home_penalty(length)
						if team == "Away":
							team_strength_array[i].away_penalty(length)

			if re.search(five_min_re, penalty_text):
				length = 5
				#print("5 min penalty")

				for i in range(time_idx, time_idx + 300):
					if team == "Home":
						team_strength_array[i].home_penalty(length)
					if team == "Away":
						team_strength_array[i].away_penalty(length)

			if re.search(ten_min_re, penalty_text):
				length = 10
				#print("10 min penalty")

			if re.search(twenty_min_re, penalty_text):
				length = 20
				#print("20 min penalty")

			penalty_array.append([time, player_name, length, infraction])

	# print(team_strength_array[238])
	# print(team_strength_array[239])
	# print(team_strength_array[240])
	return team_strength_array



def test():
	source = get_page_source(8017)
	#shots = get_shots_from_source(source)
	create_penalty_map(source)

#test()
#get_all_match_ids()