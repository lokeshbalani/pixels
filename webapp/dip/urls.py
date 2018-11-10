from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('histplt/', views.histogram_plot_view, name='histplt'),
    path('histeq/', views.histogram_eq_view, name='histeq'),
    path('median-filter/', views.median_filter_view, name='median-filter'),
    path('median-filter/diy/', views.median_filter_diy_view, name='median-filter-diy'),
    path('median-filter/lec/', views.median_filter_lec_view, name='median-filter-lec'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
