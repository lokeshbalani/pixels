from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html
    return render(request, 'index.html')

def histogram_plot_view(request):
    # Specify your own template name/location
    template_name = 'modules/histogram/hist-plt.html'  

    return render(request, template_name)