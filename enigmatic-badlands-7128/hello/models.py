from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Shot(models.Model):
	shooter = models.CharField(max_length=255)
	first_assist = models.CharField(max_length=255, default="Unknown")
	second_assist = models.CharField(max_length=255, default="Unknown")
	season = models.CharField(max_length=255, default='2015-2016')
	x = models.DecimalField(max_digits=3, decimal_places=1)
	y = models.DecimalField(max_digits=3, decimal_places=1)
	x_plotted = models.IntegerField(default=0)
	y_plotted = models.IntegerField(default=0)
	time_min = models.IntegerField()
	time_sec = models.IntegerField()
	shooting_team = models.CharField(max_length=255)
	opposing_team = models.CharField(max_length=255)
	outcome = models.CharField(max_length=255)
	blocker = models.CharField(max_length=255, default="Unknown")
	goalie = models.CharField(max_length=255, default="Empty net")
	team_strength = models.CharField(max_length=255, default="even")
	# ToDo: team_strength

class Match(models.Model):
	match_id = models.IntegerField()
	season = models.CharField(max_length=255)

class Penalty(models.Model):
	player = models.CharField(max_length=255)
	infraction = models.CharField(max_length=255)
	#referee1 = models.CharField(max_length=255)
	#referee2 = models.CharField(max_length=255)
	#team = models.CharField(max_length=255)
	#opposing_team = models.CharField(max_length=255)
	#assigned_player = models.CharField(max_length=255)
	time = models.IntegerField()