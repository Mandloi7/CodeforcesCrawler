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

# Create your views here.
def home(request):
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

    