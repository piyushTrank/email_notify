from django.urls import path
from App.views import *

urlpatterns = [
    path("",LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("dashboard/",HomeView.as_view(),name="dashboard"),
    path("add-information",AddInformationView.as_view(),name="add-information"),
    path("delete-user/<int:id>/", DeleteUser.as_view(), name="delete-user"),
    path("edit-notify/<int:id>/", EditNotifyView.as_view(), name="edit-notify"),
    path("cron-job/", CronJobAPI.as_view(), name="cron-job"),
    path("email-management/", EmailView.as_view(), name="email-management"),
    path("add-email/", AddEmailView.as_view(), name="add-email"),
    path("edit-email/<int:id>/", EditEmailView.as_view(), name="edit-email"),
    path("delete-email/<int:id>/", DeleteEmailView.as_view(), name="delete-email"),
]


