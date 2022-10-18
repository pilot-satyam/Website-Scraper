from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect
# Create your views here.
def scrape(request):
    if request.method == 'POST':
        site = request.POST.get('site','')
        #page = requests.get('http://www.google.com')
        page = requests.get(site,verify=False) #verify = False inorder to pass the SSL check,otherwise it will not scrape because every website has https
        soup = BeautifulSoup(page.text,'html.parser')
    #link_address = [] for representing it in the form of list initially
        for link in soup.find_all('a'):
        #link_address.append(link.get('href'))
            link_address = link.get('href')
            link_text = link.string
        #creating objects and saving it into the database
            Link.objects.create(address=link_address,name=link_text)
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()
    #return render(request,'myapp/result.html',{'link_address': link_address})
    return render(request,'myapp/result.html',{'data' : data})

def clear(request):
    Link.objects.all().delete()
    return render(request,'myapp/result.html')