from django.urls import path

from register_app import views

app_name = 'register_app'
urlpatterns = [

    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),

    path('profile/<str:username>/', views.view_profile, name='view_profile'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

