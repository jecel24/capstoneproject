
from django.contrib import admin
from django.urls import path
from event import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name='home'),
    
    
    path('adminclick', views.adminclick_view),
    path('playerclick', views.playerclick_view),
    
    path('adminsignup', views.admin_signup_view),
    path('playersignup', views.player_signup_view,name='playersignup'),
    
    path('adminlogin', LoginView.as_view(template_name='event/adminlogin.html')),
    path('playerlogin', LoginView.as_view(template_name='event/playerlogin.html')),
    
    
    
    
    
    
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='event/index.html'),name='logout'),

    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-player', views.admin_player_view,name='admin-player'),
    path('admin-add-player', views.admin_add_player_view,name='admin-add-player'),
    path('admin-view-player', views.admin_view_player_view,name='admin-view-player'),
    path('delete-player-from-event/<int:pk>', views.delete_player_from_event_view,name='delete-player-from-event'),
    path('delete-player/<int:pk>', views.delete_player_view,name='delete-player'),
    path('update-player/<int:pk>', views.update_player_view,name='update-player'),
    path('admin-approve-player', views.admin_approve_player_view,name='admin-approve-player'),
    path('approve-player/<int:pk>', views.approve_player_view,name='approve-player'),
    
    path('admin-team', views.admin_team_view,name='admin-team'),
    path('admin-add-team', views.admin_add_team_view,name='admin-add-team'),
    path('admin-view-team', views.admin_view_team_view,name='admin-view-team'),
    path('delete-team-from-event/<int:pk>', views.delete_team_from_event_view,name='delete-team-from-event'),
    path('delete-team/<int:pk>', views.delete_team_view,name='delete-team'),
    path('edit-team/<int:pk>', views.edit_team_view,name='edit-team'),
    
    path('admin-sched', views.admin_sched_view,name='admin-sched'),
    path('admin-add-sched', views.admin_add_sched_view,name='admin-add-sched'),
    path('admin-view-sched', views.admin_view_sched_view,name='admin-view-sched'),
    path('delete-sched-from-event/<int:pk>', views.delete_sched_from_event_view,name='delete-sched-from-event'),
    path('delete-sched/<int:pk>', views.delete_sched_view,name='delete-sched'),
    path('update-sched/<int:pk>', views.update_sched_view,name='update-sched'),
    
    path('admin-score', views.admin_score_view,name='admin-score'),
    path('admin-add-score', views.admin_add_score_view,name='admin-create-score'),
    path('admin-view-score', views.admin_view_score_view,name='admin-view-score'),
    path('delete-score-from-event/<int:pk>', views.delete_score_from_event_view,name='delete-score-from-event'),
    path('delete-score/<int:pk>', views.delete_score_view,name='delete-score'),
    path('update-score/<int:pk>', views.update_score_view,name='update-score'),
    
    path('player-dashboard', views.player_dashboard_view,name='player-dashboard'),
    
    path('admin-notice', views.admin_notice_view,name='admin-notice'),
   
]
    