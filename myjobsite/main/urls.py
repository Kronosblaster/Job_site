from django.urls import path
from . import views
from main import views as myapp_views

urlpatterns = [
    path('register/', myapp_views.register,name='register'),    
    path('register/save', myapp_views.register_user),
    path('register/login', myapp_views.login),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('dashboard/newJob', views.job_create,name="new job"),
    path('dashboard/addJob', views.add_job,name="addjob"), #This points to a function that adds a job to the database
    path('dashboard/logout', views.logout_request,name="logout"),
    path('dashboard/getJobData/',views.getJobData),
    path('dashboard/getJobDataAll/',views.getJobDataAll),
    path('dashboard/myjobs/',views.my_jobs,name="myjobs"),
    path('dashboard/alljobs/',views.all_jobs,name="alljobs"),
    path('dashboard/myjobs/view/',views.view,name="view"),
    path('dashboard/myjobs/giveup',views.giveup,name="giveup"),
    path('dashboard/myjobs/remove',views.remove,name="remove"),
    path('dashboard/myjobs/done',views.done,name="done"),
    path('dashboard/myjobs/edit',views.edit,name="edit"),
    path('dashboard/myjobs/edit_job',views.edit_job,name="edit_job")
]