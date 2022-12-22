from django.shortcuts import render
from .models import *
# Create your views here.
class Baseview(View):
    views = {}

class Homeview(Baseview):
    def get(self,request):

        return render(request, 'index.html')