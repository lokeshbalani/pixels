from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html
    return render(request, 'index.html')

def histogram_plot_view(request):
    template_name = 'modules/histogram/hist-plt.html'

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('index')
    else:
        form = ImageForm()

    return render(request, template_name, {
        'form': form
    })