from django.urls import path
from .views import InviteCodeView


urlpatterns = [
    path('invite', InviteCodeView.as_view(), name='invite')
]
