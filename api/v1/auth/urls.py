from django.urls import path
from .views import SignUpView, LogInView, LogoutView


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LogInView.as_view()),
    path('logout/', LogoutView.as_view()),
]
