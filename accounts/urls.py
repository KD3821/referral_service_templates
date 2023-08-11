from django.urls import path
from .views import VerifyView, HomeView, LoginView


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('code', VerifyView.as_view(), name='code'),
    path('home', HomeView.as_view(), name='home'),
    path('home/<str:phone>', HomeView.as_view(), name='user_home')
]
