from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginRegisterPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('delete-inovoice/<str:pk>', views.deleteInovoice, name='delete-inovoice'),
]