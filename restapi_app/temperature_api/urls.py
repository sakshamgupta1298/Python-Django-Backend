from django.urls import path
from . import views

urlpatterns = [
    path('temperature-readings/<int:city_id>/', views.TemperatureStatsView.as_view(), name='temperature-readings'),
]
