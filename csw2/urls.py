"""
Definition of urls for csw2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from app.views import register
from app.views import area
from app.views import ship_view
from app.views import port_view
from app.views import admin_panel
from app.views import change_order_completed
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import statistics
from app.views import login_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', register, name='register'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('port/', port_view, name='port'),
    path('ship/', ship_view, name='ship'),
    path('login/', login_view, name='login'),
    path('area/', views.area, name='area'),
    path('edit_contract/<int:contract_id>/', views.area, name='edit_contract'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('delete_port/<int:port_id>/', views.delete_port, name='delete_port'),
    path('delete_ship/<int:ship_id>/', views.delete_ship, name='delete_ship'),
    path('edit_port/<int:port_id>/', views.edit_port, name='edit_port'),
    path('edit_ship/<int:ship_id>/', views.edit_ship, name='edit_ship'),
    path('change_order_completed/<int:route_id>/', change_order_completed, name='change_order_completed'),
    path('pay_payment/<int:payment_id>/', views.area, name='pay_payment'),
    path('statistics/', statistics, name='statistics'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]

