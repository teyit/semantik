"""polarization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from polarization.accounts.views import CreateNodeView, HomeView, NodeView
from polarization.search.views import SearchView, CreateSearchView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Auth
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name="login"),
    url(r'^logout/$', auth_views.logout, name="logout"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    # accounts
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^nodes/$', NodeView.as_view()),
    url(r'^api/nodes/$', CreateNodeView.as_view()),

    # search
    url(r'^search/$', SearchView.as_view()),
    url(r'^search/add/$', CreateSearchView.as_view()),
]
