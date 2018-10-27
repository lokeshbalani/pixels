from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('histplt/', views.histogram_plot_view, name='histplt'),
] 