from django.db import models


class League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)
    number_of_teams = models.IntegerField()
    current_champion = models.CharField(max_length=50, null=True)
    most_championships = models.CharField(max_length=50, null=True)
    most_appearances = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'League'
    
    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    championships_won = models.IntegerField()
    coach = models.CharField(max_length=100, null=False)
    number_of_players = models.IntegerField()
    league = models.ForeignKey(League, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Team'
        
    def __str__(self):
        return self.name


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    age = models.IntegerField()
    position = models.CharField(max_length=30, null=False)
    appearances = models.IntegerField()
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Player'
        
    def __str__(self):
        return self.name

