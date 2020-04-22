from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def home(request):
    return render(request,'home_page.html',{})
