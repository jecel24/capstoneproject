from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings




def home_view(request):
    notice=models.Notice.objects.all()

    context = {
        'notice': notice
    }

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    
    return render(request, 'event/index.html', context)
    
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'event/adminclick.html')

def playerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'event/playerclick.html')


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'event/adminsignup.html',{'form':form})


def player_signup_view(request):
    form1=forms.PlayerForm()
    form2=forms.PlayerExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.PlayerForm(request.POST)
        form2=forms.PlayerExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_player_group = Group.objects.get_or_create(name='PLAYER')
            my_player_group[0].user_set.add(user)

        return HttpResponseRedirect('playerlogin')
    return render(request,'event/playersignup.html',context=mydict)



def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_player(user):
    return user.groups.filter(name='PLAYER').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_player(request.user):
        accountapproval=models.Player.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('player-dashboard')
        else:
            return render(request,'event/player_wait_for_approval.html')
        

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    
    playercount=models.Player.objects.all().filter(status=True).count()
    pendingplayercount=models.Player.objects.all().filter(status=False).count()
    
    teamcount=models.Team.objects.filter().count()
    pendingteamcount=models.Team.objects.all().filter()
    
    sched=models.Game.objects.filter().count()
    
    notif=models.Notice.objects.filter().count()
    


    notice= models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay(by sumit)
    mydict={
        'playercount':playercount,
        'pendingplayercount':pendingplayercount,
        
        
        'teamcount':teamcount,
        'pendingteamcount': pendingteamcount,
        
        'sched':sched,
        
        'notif':notif,
        

        'notice':notice

    }

    return render(request,'event/admin_dashboard.html',context=mydict)

@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def player_dashboard_view(request):
    playerdata=models.Player.objects.all().filter(user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'notice':notice
    }
    return render(request,'event/player_dashboard.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')

    return render(request,'event/admin_notice.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_player_view(request):
    return render(request,'event/admin_player.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_player_view(request):
    form1=forms.PlayerForm()
    form2=forms.PlayerExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.PlayerForm(request.POST)
        form2=forms.PlayerExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()
            
            my_player_group = Group.objects.get_or_create(name='PLAYER')
            my_player_group[0].user_set.add(user)
            
        return HttpResponseRedirect('admin-player')
    return render(request,'event/admin_add_player.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_player_view(request):
    players=models.Player.objects.all().filter(status=True)
    return render(request,'event/admin_view_player.html',{'players':players})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_player_from_event_view(request,pk):
    player=models.Player.objects.get(id=pk)
    user=models.User.objects.get(id=player.user_id)
    user.delete()
    player.delete()
    return redirect('admin-view-player')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_player_view(request,pk):
    player=models.Player.objects.get(id=pk)
    user=models.User.objects.get(id=player.user_id)
    user.delete()
    player.delete()
    return redirect('admin-approve-player')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_player_view(request,pk):
    player=models.Player.objects.get(id=pk)
    user=models.User.objects.get(id=player.user_id)
    form1=forms.PlayerForm(instance=user)
    form2=forms.PlayerExtraForm(instance=player)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.PlayerForm(request.POST,instance=user)
        form2=forms.PlayerExtraForm(request.POST,instance=player)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-player')
    return render(request,'event/admin_update_player.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_player_view(request):
    players=models.Player.objects.all().filter(status=False)
    return render(request,'event/admin_approve_player.html',{'players':players})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_player_view(request,pk):
    players=models.Player.objects.get(id=pk)
    players.status=True
    players.save()
    return redirect(reverse('admin-approve-player'))




#  Team View

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_team_view(request):
    return render(request,'event/admin_team.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_team_view(request):
    form = forms.TeamForm()
    if request.method == "POST":
        form = forms.TeamForm(request.POST)
        if form.is_valid():
            user=form.save() 
          
           
            return HttpResponseRedirect("admin-team")

    return render(request, 'event/admin_add_team.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_team_view(request):
    teams=models.Team.objects.all()
    return render(request,'event/admin_view_team.html',{'teams':teams})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_team_from_event_view(request, pk):
    team = models.Team.objects.get(pk=pk)
    team.delete()
    return redirect('admin-view-team')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_team_view(request,pk):
    form=forms.TeamForm()
    form.delete()
    return redirect('admin-approve-team')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_team_view(request, pk):
    team=models.Team.objects.get(id=pk)
    form=forms.TeamForm(instance=team) # Initialize the form variable with a default value
    if request.method == 'POST':
        form = forms.TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('admin-view-team')
    return render(request, 'event/admin_edit_team.html', {'form': form})


# Game Sched View

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_sched_view(request):
    return render(request,'event/admin_sched.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_sched_view(request):
    form = forms.GameForm()
    if request.method == "POST":
        form = forms.GameForm(request.POST)
        if form.is_valid():
            form.save() 
          
            return HttpResponseRedirect("admin-sched")

    return render(request, 'event/admin_add_sched.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_sched_view(request):
    games=models.Game.objects.all()
    return render(request,'event/admin_view_sched.html', {'games':games})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_sched_from_event_view(request, pk):
    game = models.Game.objects.get(pk=pk)
    game.delete()
    return redirect('admin-view-sched')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_sched_view(request,pk):
    form=forms.GameForm()
    form.delete()
    return redirect('admin-approve-sched')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_sched_view(request, pk):
    game=models.Game.objects.get(id=pk)
    form=forms.GameForm(instance=game) 
    if request.method == 'POST':
        form = forms.GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('admin-view-sched')
    return render(request, 'event/admin_update_sched.html', {'form': form})


# Score View

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_score_view(request):
    return render(request,'event/admin_score.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_score_view(request):
    form = forms.ScoreForm()
    if request.method == "POST":
        form = forms.ScoreForm(request.POST)
        if form.is_valid():
            form.save() 
          
           
            return HttpResponseRedirect("admin-score")

    return render(request, 'event/admin_add_score.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_score_view(request):
    scores=models.Score.objects.all()
    return render(request,'event/admin_view_score.html',{'scores':scores})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_score_from_event_view(request, pk):
    score = models.Score.objects.get(pk=pk)
    score.delete()
    return redirect('admin-view-score')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_score_view(request,pk):
    form=forms.ScoreForm()
    form.delete()
    return redirect('admin-approve-score')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_score_view(request, pk):
    score=models.Score.objects.get(id=pk)
    form=forms.ScoreForm(instance=score) # Initialize the form variable with a default value
    if request.method == 'POST':
        form = forms.ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            return redirect('admin-view-score')
    return render(request, 'event/admin_update_score.html', {'form': form})
