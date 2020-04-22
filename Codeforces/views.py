from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import requests
import urllib.request
from html.parser import HTMLParser
from html.entities import name2codepoint
import time
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
import urllib.request
from html.parser import HTMLParser
from html.entities import name2codepoint
import time
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd
from django.contrib.sites import requests
import requests, bs4, csv, json, time
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import matplotlib
import numpy
import json
from django.urls import reverse
from collections import Counter

# Create your views here.
def home(request):

    if request.POST:
        if request.POST['handle']:
            url = 'https://codeforces.com/api/user.info?handles=' + str(request.POST['handle'])
            response = requests.get(url)
            name = str(request.POST['handle'])
            soup2 = bs4.BeautifulSoup(response.text, "html.parser")
            l2 = json.loads(str(soup2))
            if l2['status'] != 'OK':
                return render(request, 'home_page.html', {'flag': 1})
            else:
                return render(request, 'analysis.html', {'name' :name})
    url = 'https://codeforces.com/contests'
    response = requests.get(url)
    doc = lh.fromstring(response.content)
    tr_elements = doc.xpath('//tr')
    cfcontests = []
    for i in tr_elements[1:]:
        c1 = i[0].text_content()
        t1 = i[2].text_content()
        if c1 == 'Name':
            break
        else:
            cfcontests.append({'con':c1,'time':t1})
    url2 = 'https://www.codechef.com/contests'
    response2 = requests.get(url2)
    doc = lh.fromstring(response2.content)
    tr_elements2 = doc.xpath('//tr')
    c3 = tr_elements2[9][0].text_content()
    t3 = tr_elements2[9][2].text_content()
    c4 = tr_elements2[10][0].text_content()
    t4 = tr_elements2[10][2].text_content()
    return render(request, 'home_page.html',
                  {'cfcontests': cfcontests, 'c3': c3, 'c4': c4, 't3': t3, 't4': t4})

    