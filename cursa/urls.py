"""cursa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from cursa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.auth, name="auth"),
    path('login/', views.login, name="login"),
    path('newUser/', views.newUser, name="newUser"),
    path('createUser/', views.createUser, name='createUser'),
    path('changeUser/', views.changeUser, name='changeUser'),
    path('delUser/', views.delUser, name='delUser'),
    path('addorg/',views.addorg, name="addorg"),
    path('addOrgToJSON/', views.addOrgToJSON, name='addOrgToJSON'),
    path('changeDirector/',views.changeDir, name='changeDir'),
    path('delOrg/', views.delOrg, name='delOrg'),
    path('changeOrg/', views.changeOrg, name='changeOrg'),
    path('addoffer/', views.addoffer, name='addoffer'),
    path('changeOrgName/', views.changeOrgName, name='changeOrgName'),
    path('addOrder/', views.addOrder, name='addOrder'),
    path('changeEmpOrg/', views.changeEmpOrg, name='changeEmpOrg'),
    path('cab/', views.cabPagePrepare, name='cabPagePrepare'),
    path('changeUserInfo/', views.changeUserInfo, name='changeUserInfo'),
    path('choseUser/', views.choseUser, name='choseUser'),
    path('changeOrder/', views.changeOrder, name='changeOrder'),
    path('home/', views.home, name='home')

]
