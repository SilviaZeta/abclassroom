# Use include() to add paths from the catalog application
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('account/login/', views.login_view, name='login'),
    path('account/signup/', views.signup_view, name='signup'),
    path('account/signup/validate_username/', views.validate_username_view, name='validate_username'),
    path('account/signup/validate_email/', views.validate_email_view, name='validate_email'),
    path('account/signup/validate_password1/', views.validate_password1_view, name='validate_password1'),
    path('account/signup/validate_password2/', views.validate_password2_view, name='validate_password2'),

    path('account/logout/', views.logout_view, name='logout'),

    path('account/password_reset/', auth_views.PasswordResetView.as_view( \
        template_name='password_reset/password_reset_form.html'), name='password_reset_form'),

    path('account/password_reset/done/', auth_views.PasswordResetDoneView.as_view( \
        template_name='password_reset/password_reset_done.html'), name='password_reset_done'),

    path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( \
        template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),

    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view( \
        template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
    
    path('<username>/update_profile/', views.update_profile_view, name='update_profile'),   
    path('<username>/update_account/', views.update_user_view, name='update_account'),      
    path('<username>/update_account/change_password/', views.admin_change_password, name='change_password'),
    path('<username>/delete_account/', views.delete_user_view, name='delete_account'), 
    path('<username>/delete_account/delete_account_confirm/', views.delete_account_confirm_view, name='delete_account_confirm'),


]

