from __future__ import unicode_literals

from django.db import models

# Create your models here.
class League (models.Model):
    name = models.CharField(max_length=3)
    last_modified = models.DateField(null=True)
    verbose_name = models.CharField(max_length=50, null=True)
    def __unicode__(self):
        return unicode(self.name)
    class Meta:
        app_label = 'core'

class Team(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    colour = models.CharField(max_length=6, null=True)
    twitter = models.CharField(max_length=15, null=True)
    kickdex = models.CharField(max_length=5, null=True)
    def __unicode__(self):
        return unicode (self.name)
    class Meta:
        app_label = 'core'


class Match(models.Model):
    league = models.CharField(max_length=256)
    match_date = models.DateTimeField(db_index=True)
    home_team = models.CharField(max_length=256)
    away_team = models.CharField(max_length=256)
    def __unicode__(self):
        return unicode(self.match_date) + " : " + unicode(self.home_team) + " v " + unicode(self.away_team)
    class Meta:
        verbose_name_plural = "Matches"
        app_label = 'core'

class MatchStats(Match):
    match = models.OneToOneField(Match)
    RESULT_CHOICES = (
        ('H', 'Home'),
        ('D', 'Draw'),
        ('A', 'Away'))
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
        app_label ='core'

class Odds(models.Model):
    match = models.ForeignKey(Match)
    bet_name = models.CharField(max_length=256)
    bet_type = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_offer = models.CharField(max_length=256)

    class Meta:
        app_label = 'core'
    """{"bet_name": bet_name,
            "bet_type:": item["@slug"],
            "price": item["bids"]["price"][0]["@decimal"],
            "bid-offer": "bid"})"""