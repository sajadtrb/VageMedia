from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('upload_csv/', DashboardsView.as_view(template_name = 'pages/static/uploadcsv.html')),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]