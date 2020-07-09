from django.urls import path

from accounts.views import UserLoginView, UserLogoutView, RegisterUserView, ConfirmRegistrationView, \
    ResendConfirmRegistrationView

app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('confirm-email/<str:user_id>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm_email'),
]
