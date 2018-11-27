from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('histplt/', views.histogram_plot_view, name='histplt'),
    path('histeq/', views.histogram_eq_view, name='histeq'),
    path('erosion-filter/', views.erosion_filter_view, name='erosion-filter'),
    path('erosion-filter/diy/', views.erosion_filter_diy_view, name='erosion-filter-diy'),
    path('erosion-filter/lec/', views.erosion_filter_lec_view, name='erosion-filter-lec'),
    path('sobel-filter/', views.sobel_filter_view, name='sobel-filter'),
    path('sobel-filter/diy/', views.sobel_filter_diy_view, name='sobel-filter-diy'),
    path('sobel-filter/lec/', views.sobel_filter_lec_view, name='sobel-filter-lec'),
    path('globalthresholding/', views.globalthresholding_view, name='globalthresholding'),
    path('globalthresholding/diy/', views.globalthresholding_diy_view, name='globalthresholding-diy'),
    path('globalthresholding/lec/', views.globalthresholding_lec_view, name='globalthresholding-lec'),
    path('adaptivethresholding/', views.adaptivethresholding_view, name='adaptivethresholding'),
    path('adaptivethresholding/diy/', views.adaptivethresholding_diy_view, name='adaptivethresholding-diy'),
    path('adaptivethresholding/lec/', views.adaptivethresholding_lec_view, name='adaptivethresholding-lec'),
    path('averaging-filter/', views.averaging_filter_view, name='averaging-filter'),
    path('averaging-filter/diy/', views.averaging_filter_diy_view, name='averaging-filter-diy'),
    path('averaging-filter/lec/', views.averaging_filter_lec_view, name='averaging-filter-lec'),
    path('gaussian-filter/', views.gaussian_filter_view, name='gaussian-filter'),
    path('gaussian-filter/diy/', views.gaussian_filter_diy_view, name='gaussian-filter-diy'),
    path('gaussian-filter/lec/', views.gaussian_filter_lec_view, name='gaussian-filter-lec'),
    path('median-filter/', views.median_filter_view, name='median-filter'),
    path('median-filter/diy/', views.median_filter_diy_view, name='median-filter-diy'),
    path('median-filter/lec/', views.median_filter_lec_view, name='median-filter-lec'),
    path('bilateral-filter/', views.bilateral_filter_view, name='bilateral-filter'),
    path('bilateral-filter/diy/', views.bilateral_filter_diy_view, name='bilateral-filter-diy'),
    path('bilateral-filter/lec/', views.bilateral_filter_lec_view, name='bilateral-filter-lec'),
    path('connected-components/', views.connected_components_view, name='connected-components'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
