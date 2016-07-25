from __future__ import unicode_literals

from django.db import models

# Create your models here.
class League (models.Model):
    name = models.CharField(max_length=3)
    last_modified = models.DateField(null=True)
    verbose_name = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return unicode(self.name)

class Team(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    colour = models.CharField(max_length=6, null=True)
    twitter = models.CharField(max_length=15, null=True)
    kickdex = models.CharField(max_length=5, null=True)
    def __unicode__(self):
        return unicode (self.name)

class Fixture(models.Model):
    league = models.ForeignKey(League)
    match_date = models.DateField(db_index=True)
    home_team = models.ForeignKey(Team, related_name="AsHomeTeam", db_index=True)
    away_team = models.ForeignKey(Team, related_name="AsAwayTeam", db_index=True)
    def __unicode__(self):
        return unicode(self.match_date) + " : " + unicode(self.home_team) + " v " + unicode(self.away_team)
    class Meta:
        verbose_name_plural = "Matches"

class Match(models.Model):

    RESULT_CHOICES = (
        ('H', 'Home'),
        ('D', 'Draw'),
        ('A', 'Away'))
    league = models.ForeignKey(League)
    match_date = models.DateField(db_index=True)
    home_team = models.ForeignKey(Team, related_name="AsHomeTeam", db_index=True)
    away_team = models.ForeignKey(Team, related_name="AsAwayTeam", db_index=True)
    full_time_home_goals = models.PositiveSmallIntegerField(null=True, db_index=True)
    full_time_away_goals = models.PositiveSmallIntegerField(null=True)
    full_time_result = models.CharField(max_length=1, choices=RESULT_CHOICES, null=True)
    half_time_home_goals = models.PositiveSmallIntegerField(null=True)
    half_time_away_goals = models.PositiveSmallIntegerField(null=True)
    half_time_result = models.CharField(max_length=1, choices=RESULT_CHOICES,null=True)
    home_shots = models.PositiveSmallIntegerField(null=True)
    away_shots = models.PositiveSmallIntegerField(null=True)
    home_shots_on_target = models.PositiveSmallIntegerField(null=True)
    away_shots_on_target = models.PositiveSmallIntegerField(null=True)
    home_corners = models.PositiveSmallIntegerField(null=True)
    away_corners = models.PositiveSmallIntegerField(null=True)
    home_yellow = models.PositiveSmallIntegerField(null=True)
    away_yellow = models.PositiveSmallIntegerField(null=True)
    home_red = models.PositiveSmallIntegerField(null=True)
    away_red = models.PositiveSmallIntegerField(null=True)
    def __unicode__(self):
        return unicode(self.match_date) + " : " + unicode(self.home_team) + " v " + unicode(self.away_team)
    class Meta:
        verbose_name_plural = "Matches"
    