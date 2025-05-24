"""
URL configuration for tech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve 
from .views import *
urlpatterns = [
    path('',home , name='home'),
    path('register',register     , name='register'),
    path('login',connexion     , name='login'),
    path('log-out',deconnect     , name='deconnexion'),
    path('contact',contact , name='contact'),
    path('myproject',myproject , name='myproject'),
    path('my_admin/create_project', createproject, name='project_create'),
    path('my_admin/create_formation', create_formation, name='formation_create'),
    path('my_admin/create_category', create_categ, name='create_categ'),
    path('my_admin/create_technology', create_tech, name='create_tech'),
    path('formations/<int:pk>/edit/', update_formation, name='formation_update'),
    path('formations/', myformation, name='myformation'),
    path('formations/<int:id>', detatilform, name='detailform'),
    path('project/<int:id>', projectdetail, name='detailprojet'),
    path('formution/<int:id>', Formationinf, name='detailinfo'),
    path('dashbord/administration', admin_dashboard, name='admin_dashbord'),
    path('dashbord/attestation<int:id>', Attestation, name='attestation'),
    path('admin/utilisateurs/', gestion_utilisateurs, name='gestion_utilisateurs'),
    path('admin/participation/<int:id>/delete/', delete_participation, name='delete_participation'),
    path('admin/technologies/', list_tech, name='list_tech'),
    path('admin/technologies/<int:id>/delete/', delete_tech, name='delete_tech'),
    path('admin/categories/', list_categories, name='list_categories'),
    path('admin/categories/<int:id>/delete/', delete_category, name='delete_category'),
    path('admin/projects/', list_projects, name='list_projects'),
    path('admin/projects/<int:id>/delete/', delete_project, name='delete_project'),
    path('admin/formations/', list_formations, name='list_formations'),
    path('admin/formations/<int:id>/delete/', delete_formation, name='delete_formation'),
    # path('admin/participation/<int:id>/update/', update_participation, name='update_participation'),
    path('my_admin/category/<int:id>/update/', update_categ, name='update_categ'),
    path('my_admin/technology/<int:id>/update/', update_tech, name='update_tech'),
    path('my_admin/project/<int:id>/update/', update_project, name='update_project'),
    path('my_admin/participation/<int:id>/update/', update_participation, name='update_participation'),
    path('admin/participations/', ParticipationListView, name='participations_list'),
    path('admin/participations/<int:f_id>/upload/', upload_attestation, name='upload_attestation'),
    path('contact-pending/', contact_view, name='contacted'),





    
]
