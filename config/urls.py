from django.contrib import admin
from django.urls import path
from app.views import HouseList, HouseDetail, AgentProfile, ProfileUpdate


urlpatterns = [
    path('', HouseList.as_view(), name='houses'),
    path('profile/<str:pk>/', AgentProfile.as_view(), name='profile'),
    path('profile-update/<str:pk>/', ProfileUpdate.as_view(), name='profile-update'),
    path('detail/<str:pk>/', HouseDetail.as_view(), name='house'),
    path('admin/', admin.site.urls),
]