"""JBElection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from JBApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Index),
    path('login',views.login),
    path('otp',views.validate_otp,name='otp'),
    path('result',views.result),
    path('resultProgress',views.resultProgress),
    path('delete',views.delete),

    path('admin_home',views.admin_home),
    path('adm_hod',views.adm_hod,name='adm_hod'),
    path('adm_elec',views.adm_elec),
    path('adm_liveElec',views.adm_liveElec),
    path('adm_completeElec',views.adm_completeElec),
    path('adm_eroll',views.adm_eroll),
    path('adm_obj',views.adm_obj),
    path('adm_nomi',views.adm_nomi),
    path('adm_paper', views.view_paper_trails, name='view_paper_trails'),

    path('hod_home',views.hod_home),
    path('hod_faculty',views.hod_faculty,name="hod_fac"),
    path('hod_eroll',views.hod_eroll),
    path('hod_approveEroll',views.hod_approveEroll),
    path('hod_obj',views.hod_obj),
    path('hod_nomi',views.hod_nomi),

    path('fac_home',views.fac_home),
    path('fac_stud',views.fac_stud),
    path('fac_eroll',views.fac_eroll,name='fac_eroll'),
    path('fac_nomi',views.fac_nomi),
    path('fac_approvNomi',views.fac_approvNomi),

    path('stud_home',views.stud_home),
    path('stude_eroll',views.stude_eroll),
    path('stude_nomi',views.stude_nomi),
    path('stude_cand',views.stude_cand),
    path('stude_vote',views.stude_vote),
    path('stud_addvote',views.stud_addvote),
]
