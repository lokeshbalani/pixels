from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """View function for home page of site."""
    
    # Render the HTML template index.html
    return render(request, 'index.html')
    #return HttpResponse("Hello, world. You're at the Digital Image Processing Project index.")