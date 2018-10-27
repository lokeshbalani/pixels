from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('histplt/', views.histogram_plot_view, name='histplt'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
