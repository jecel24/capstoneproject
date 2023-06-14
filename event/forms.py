from django import forms
from django.contrib.auth.models import User
from . import models



class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = ['name']

class PlayerForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class PlayerExtraForm(forms.ModelForm):
    class Meta:
        model=models.Player
        fields=['team','jersey_number','contact','user_email']

class GameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        fields = ['team1', 'team2', 'date', 'time']

class ScoreForm(forms.ModelForm):
    class Meta:
        model = models.Score
        fields = ['player', 'team', 'score']
        

class NoticeForm(forms.ModelForm):
    class Meta:
        model= models.Notice
        fields='__all__'



