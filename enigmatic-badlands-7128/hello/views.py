#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import os

from celery import task, current_task
from celery.result import AsyncResult

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
try:
    from django.utils import simplejson as json
except:
    import json
from django.conf.urls import patterns, url

from django_sortable.helpers import sortable_helper

from database_controller import add_shot_to_database, add_match_to_database, add_all_matches_from_season_to_database

from .models import Greeting, Shot
import configuration as cfg

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def moderate(request):
	return render(request, 'moderate.html')

def add_match(request):
	match_id = request.POST['match_id']
	add_match_to_database(match_id)

	return render(request, 'moderate.html')

def add_all_matches_from_season(request):
	season = request.POST['season']
	# if 'DATABASE_URL' exists, then it's heroku
	if os.environ.has_key('DATABASE_URL'):
		job = add_matches_async.delay((season))
	else:
		print("sync")
		add_all_matches_from_season_to_database(season)

	return render(request, 'moderate.html')

@task()
def add_matches_async(season):
	print("add_matches_async")
	current_task.update_state(state='PROGRESS', meta={'current': 0, 'total': 1})
	add_all_matches_from_season_to_database(season)
	# current_task.update_state(state='SUCCESS', meta={'current': 1, 'total': 1})

@task()
def do_work():
    """ Get some rest, asynchronously, and update the state all the time """
    print("do_work")
    for i in range(100):
        sleep(0.1)
        print(i)
        current_task.update_state(state='PROGRESS',
            meta={'current': i, 'total': 100})

def poll_state(request):
    """ A view to report the progress to the user """
    print("poll_state")
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')


def init_work(request):
    """ A view to start a background job and redirect to the status page """
    print("init_work")
    job = do_work.delay()
    print("work initialized")
    return HttpResponseRedirect(reverse('poll_state') + '?job=' + job.id)


# urlpatterns = patterns('webapp.modules.asynctasks.progress_bar_demo',
#     url(r'^init_work$', init_work),
#     url(r'^poll_state$', poll_state, name="poll_state"),
# )

def shots_page(request):
	context = RequestContext(request)
	context['seasons'] = sorted(Shot.objects.values_list('season', flat=True).distinct())
	context['teams'] = sorted(Shot.objects.values_list('shooting_team', flat=True).distinct())
	context['players'] = sorted(Shot.objects.values_list('shooter', flat=True).distinct())
	#context['outcomes'] = sorted(Shot.objects.values_list('outcome', flat=True).distinct())

	context['goal_checked'] = True
	context['save_checked'] = True
	context['miss_checked'] = True
	context['block_checked'] = True
	context['even_checked'] = True
	context['pp_checked'] = True
	context['sh_checked'] = True
	context['advanced_filters'] = False

	# if advanced_filters:
	# 	context['teams_against'] = sorted(Shot.objects.values_list('opposing_team', flat=True).distinct())
	# 	context['goalies'] = sorted(Shot.objects.values_list('goalie', flat=True).distinct())
	# 	context['first_assisters'] = sorted(Shot.objects.values_list('first_assist', flat=True).distinct())
	# 	context['second_assisters'] = sorted(Shot.objects.values_list('second_assist', flat=True).distinct())
	# 	context['blockers'] = sorted(Shot.objects.values_list('blocker', flat=True).distinct())
	return render(request, 'shots.html', context)

def update_filters(request):
	context = RequestContext(request)

	season = request.POST['season']
	team = request.POST['team']
	shooter = request.POST['shooter']
	#outcome = request.POST['outcome']
	#advanced_filters = True#request.POST['advanced_filters']
	goal_checked = stringToBoolean(request.POST['goal_checked'])
	save_checked = stringToBoolean(request.POST['save_checked'])
	miss_checked = stringToBoolean(request.POST['miss_checked'])
	block_checked = stringToBoolean(request.POST['block_checked'])
	advanced_filters = stringToBoolean(request.POST['advanced_filters'])
	if advanced_filters:
		team_against = request.POST['team_against']
		goalie = request.POST['goalie']
		first_assist = request.POST['first_assist']
		second_assist = request.POST['second_assist']
		blocker = request.POST['blocker']
		even_checked = stringToBoolean(request.POST['even_checked'])
		print(request.POST['even_checked'])
		pp_checked = stringToBoolean(request.POST['pp_checked'])
		sh_checked = stringToBoolean(request.POST['sh_checked'])
	else:
		even_checked = True
		pp_checked = True
		sh_checked = True

	context['selected_season'] = season
	context['selected_team'] = team
	context['selected_shooter'] = shooter
	#context['selected_outcome'] = outcome
	context['goal_checked'] = goal_checked
	context['save_checked'] = save_checked
	context['miss_checked'] = miss_checked
	context['block_checked'] = block_checked
	context['advanced_filters'] = advanced_filters
	if advanced_filters:
		context['selected_team_against'] = team_against
		context['selected_goalie'] = goalie
		context['selected_first_assister'] = first_assist
		context['selected_second_assister'] = second_assist
		context['selected_blocker'] = blocker
		context['even_checked'] = even_checked
		context['pp_checked'] = pp_checked
		context['sh_checked'] = sh_checked
	else:
		context['even_checked'] = True
		context['pp_checked'] = True
		context['sh_checked'] = True

	shots = Shot.objects.all()
	context['seasons'] = sorted(shots.values_list('season', flat=True).distinct())

	if season != "All":
		shots = shots.filter(season=season)

	new_teams = shots.values_list('shooting_team', flat=True).distinct()
	
	if team != "All":
		shots = shots.filter(shooting_team=team)

	if not goal_checked:
		shots = shots.exclude(outcome="Goal")
	if not save_checked:
		shots = shots.exclude(outcome="Saved")
	if not miss_checked:
		shots = shots.exclude(outcome="Missed")
	if not block_checked:
		shots = shots.exclude(outcome="Blocked")

	new_players = shots.values_list('shooter', flat=True).distinct()

	if advanced_filters:
			
		teams_against = shots.values_list('opposing_team', flat=True).distinct()
		context['teams_against'] = sorted(teams_against)
		if team_against != "All":
			shots = shots.filter(opposing_team=team_against)

		goalies = shots.values_list('goalie', flat=True).distinct()
		context['goalies'] = sorted(goalies)
		if goalie != "All":
			shots = shots.filter(goalie=goalie)

		if first_assist != "All":
			shots = shots.filter(first_assist=first_assist)
		if second_assist != "All":
			shots = shots.filter(second_assist=second_assist)

		if block_checked:
			blockers = shots.values_list('blocker', flat=True).distinct()
			context['blockers'] = sorted(blockers)
		if blocker != "All":
			print("FILTER BY BLOCKER")
			shots = shots.filter(blocker=blocker)

		if goal_checked:
			print("Get assisters")
			first_assisters = shots.values_list('first_assist', flat=True).distinct()
			context['first_assisters'] = sorted(first_assisters)

			second_assisters = shots.values_list('second_assist', flat=True).distinct()
			context['second_assisters'] = sorted(second_assisters)

	context['teams'] = sorted(new_teams)
	context['players'] = sorted(new_players)
	context['outcomes'] = sorted(shots.values_list('outcome', flat=True).distinct())

	print("even_checked")
	print(context['even_checked'])
	return render(request, 'shot_filter_form.html', context)

def update_table(request):
	context = RequestContext(request)
	print("update_table");
	season = request.POST['season']
	team = request.POST['team']
	shooter = request.POST['shooter']
	#outcome = request.POST['outcome']
	#advanced_filters = True#request.POST['advanced_filters']
	advanced_filters = stringToBoolean(request.POST['advanced_filters'])
	goal_checked = stringToBoolean(request.POST['goal_checked'])
	save_checked = stringToBoolean(request.POST['save_checked'])
	miss_checked = stringToBoolean(request.POST['miss_checked'])
	block_checked = stringToBoolean(request.POST['block_checked'])
	even_checked = stringToBoolean(request.POST['even_checked'])
	pp_checked = stringToBoolean(request.POST['pp_checked'])
	sh_checked = stringToBoolean(request.POST['sh_checked'])

	shots = Shot.objects.all()

	if season != "All":
		shots = shots.filter(season=season)
	if team != "All":
		shots = shots.filter(shooting_team=team)
	if shooter != "All":
		shots = shots.filter(shooter=shooter)
	if not goal_checked:
		shots = shots.exclude(outcome="Goal")
	if not save_checked:
		shots = shots.exclude(outcome="Saved")
	if not miss_checked:
		shots = shots.exclude(outcome="Missed")
	if not block_checked:
		shots = shots.exclude(outcome="Blocked")
	if not even_checked:
		shots = shots.exclude(team_strength="even")
	if not pp_checked:
		shots = shots.exclude(team_strength="powerplay")
	if not sh_checked:
		shots = shots.exclude(team_strength="shorthanded")
	# if outcome != "All":
	# 	shots = shots.filter(outcome=outcome)

	if advanced_filters:
		print("advanced_filters")
		advanced_filters = True
		team_against = request.POST['team_against']
		goalie = request.POST['goalie']
		first_assist = request.POST['first_assist']
		second_assist = request.POST['second_assist']
		blocker = request.POST['blocker']

		print(blocker)

		if team_against != "All":
			shots = shots.filter(opposing_team=team_against)
		if goalie != "All":
			shots = shots.filter(goalie=goalie)
		if first_assist != "All":
			shots = shots.filter(first_assist=first_assist)
		if second_assist != "All":
			shots = shots.filter(second_assist=second_assist)
		if blocker != "All":
			print("FILTER BY BLOCKER")
			shots = shots.filter(blocker=blocker)



	context['amount'] = len(shots)
	player_list = shots.values_list('shooter', flat=True).distinct()
	shots_array = [x[:] for x in [[0]*cfg.SQUARE_COUNT_LENGTH]*cfg.SQUARE_COUNT_WIDTH]
	shots_array2 = []
	players = []
	total_count = 0
	for shooter in player_list:
		player = {}
		player['name'] = shooter
		player['goals'] = 0
		player['saves'] = 0
		player['miss'] = 0
		player['block'] = 0
		shot_list = shots.filter(shooter=shooter)
		player['total'] = len(shot_list)
		for shot in shot_list:
			shots_array[shot.x_plotted][shot.y_plotted] += 1
			shots_array2.append([float(shot.y), float(shot.x), 1])
			total_count += 1
			if shot.outcome == "Goal":
				player['goals'] += 1
			if shot.outcome == "Saved":
				player['saves'] += 1
			if shot.outcome == "Missed":
				player['miss'] += 1
			if shot.outcome == "Blocked":
				player['block'] += 1
		players.append(player)

	shots_array3 = []
	max_value = 0
	for i in range(len(shots_array)):
		for l in range(len(shots_array[i])):
			count = shots_array[i][l]
			if count > max_value:
				max_value = count
			shots_array3.append([l + cfg.SQUARE_EDGE_LENGTH, i + cfg.SQUARE_EDGE_LENGTH, count])
	context['shots_array'] = shots_array3
	context['data_array'] = shots_array
	context['max_value'] = total_count #/ 10 #max_value
	context['players'] = sortable_helper(request, players)
	heatmap_container_width = int(request.POST['heatmap_container_width'])
	context['heatmap_container_width'] = heatmap_container_width
	context['heatmap_container_height'] = int(491 / float(973) * heatmap_container_width)
	#return render(request, 'heatmap.html', context)
	print("even_checked")
	return render(request, 'stats_table.html', context)






def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


def stringToBoolean(string):
	if string == "true":
		return True
	if string == "True":
		return True
	return False