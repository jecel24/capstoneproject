from django.db import models
from django.contrib.auth.models import User 

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    jersey_number = models.IntegerField()
    contact = models.CharField(max_length=100)
    user_email  = models.EmailField(max_length=70,blank=True,unique=True)
    status=models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Game(models.Model):
    team1 = models.ForeignKey(Team, related_name='team1_games', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_games', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()



class Score(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()


class Standings(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team} - Wins: {self.wins}, Losses: {self.losses}"


class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='event')
    message=models.CharField(max_length=500)
