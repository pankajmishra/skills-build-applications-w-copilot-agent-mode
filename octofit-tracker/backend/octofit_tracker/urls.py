"""octofit_tracker URL Configuration

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import views

router = DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'workouts', views.WorkoutViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)

@api_view(['GET'])
def api_root_codespace(request, format=None):
    """
    Return API endpoints using $CODESPACE_NAME when available to avoid relying on request scheme/host.
    """
    cs_name = os.environ.get('CODESPACE_NAME')
    if cs_name:
        base = f"https://{cs_name}-8000.app.github.dev"
    else:
        scheme = 'https' if request.is_secure() else 'http'
        base = f"{scheme}://{request.get_host()}"
    return Response({
        'teams': f"{base}/api/teams/",
        'users': f"{base}/api/users/",
        'activities': f"{base}/api/activities/",
        'workouts': f"{base}/api/workouts/",
        'leaderboard': f"{base}/api/leaderboard/",
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root_codespace, name='api-root'),
    path('api/', include(router.urls)),
]
