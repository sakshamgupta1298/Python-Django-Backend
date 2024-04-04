from django.urls import path
from .views import TemperatureStatsView
from .views import UploadTemperatureFile


urlpatterns = [
    path('temperature-readings/<int:city_id>/', TemperatureStatsView.as_view(), name='temperature-readings'),
    path('upload/', UploadTemperatureFile.as_view(), name='upload_temperature_file'),

]
