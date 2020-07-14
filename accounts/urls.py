from django.urls import path

from accounts.views import (UserLoginView, UserLogoutView, RegisterUserView, ConfirmRegistrationView,
                            ResendConfirmationEmailView, UserPasswordResetView, UserPasswordResetConfirmView,
                            UserPasswordResetDoneView, UserPasswordChangeView, UserPasswordChangeDoneView)

app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('confirm-email/<user_id>/<token>/', ConfirmRegistrationView.as_view(), name='confirm_email'),
    path('resend-confirm-email/<user_id>/<token>/', ResendConfirmationEmailView.as_view(), name='resend_confirm_email'),

    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
