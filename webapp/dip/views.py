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
    # Specify your own template name/location
    template_name = 'modules/histogram/hist-plt.html'  

    return render(request, template_name)

def image_upload(request):
    if request.method == 'POST' and request.FILES['usr-uploaded-img']:
        usr_img = request.FILES['usr-uploaded-img']
        fs = FileSystemStorage()
        filename = fs.save(usr_img.name, usr_img)
        uploaded_image_url = fs.url(filename)

        template_name = 'modules/histogram/hist-plt.html'
        return render(request, template_name, {
            'uploaded_image_url': uploaded_image_url
        })

def model_form_upload(request):
    template_name = 'modules/histogram/hist-plt.html'

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('histplt')
    else:
        form = ImageForm()

    return render(request, template_name, {
        'form': form
    })