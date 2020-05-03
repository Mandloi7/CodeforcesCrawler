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
                url = 'https://codeforces.com/api/user.rating?handle=' + str(name)
                response = requests.get(url)
                soup2 = bs4.BeautifulSoup(response.text, "html.parser")
                l2 = json.loads(str(soup2))
                contest_count = len(l2['result'])
                col = []
                best_rank = 10000
                worst_rank = 0
                max_rating = 0
                lowest_rating = 10000
                current_rating = l2['result'][contest_count - 1]['newRating']
                rating_changes = []
                j = 1
                for t in l2['result']:
                    i = t['contestId']
                    d = t['rank']
                    c = t['contestName']
                    g = t['oldRating']
                    f = t['newRating']
                    e = f - g
                    h = 'https://codeforces.com/contest/' + str(i)
                    rating_changes.append(e)
                    best_rank = min(best_rank, d)
                    worst_rank = max(worst_rank, d)
                    max_rating = max(max_rating, f)
                    lowest_rating = min(lowest_rating, f)
                    col.append({'rank': d, 'con': c, 'change': e, 'new': f, 'old': g, 'link': h, 'count': j})
                    j += 1

                col.reverse()
                rating_changes.sort()
                max_up = rating_changes[len(rating_changes) - 1]
                max_down = rating_changes[0]
                max_down = min(0, max_down)

                # this is next comment which gives the submission history
                url1 = 'https://codeforces.com/api/user.status?handle=' + str(name) + '&from=1&count=10000'
                res = requests.get(url1)
                soup = bs4.BeautifulSoup(res.text, "html.parser")
                l = json.loads(str(soup))
                sub = []
                attempt = len(l['result'])  # attempts made by user
                attempted = set([])  # attempted questions
                solved_questions = set([])
                unsolved = set([])  # unsolved questions
                # different verdicts
                ac = 0
                tle = 0
                mle = 0
                ile = 0
                ce = 0
                re = 0
                wa = 0
                other = 0

                total_rating = list()
                solved_rating = list()
                final_rating_solved = list()
                problem_count = list()
                for i in range(50):
                    total_rating.append((i + 1) * 100)
                    solved_rating.append(0)

                languages = []
                indexes = []
                for item in l['result']:
                    if 'rating' in item['problem']:
                        cr = int(item['problem']['rating']) // 100
                        solved_rating[cr - 1] += 1

                    ask = str(item['problem']['contestId']) + '-' + str(item['problem']['index'])
                    asd = str(item['problem']['contestId']) + str(item['problem']['index']) + '-' + str(item['problem']['name'])
                    we = 'https://codeforces.com/problemset/problem/' + str(item['contestId']) + '/' + str(item['problem']['index'])
                    if item['verdict'] != "OK":
                        unsolved.add(we)

                    languages.append(item['programmingLanguage'])
                    indexes.append(item['problem']['index'][0])

                    attempted.add(asd)
                    if item['verdict'] == "OK":
                        solved_questions.add(we)
                        ac += 1
                    else:
                        if item['verdict'] == "WRONG_ANSWER":
                            wa += 1
                        else:
                            if item['verdict'] == "COMPILATION_ERROR":
                                ce += 1
                            else:
                                if item['verdict'] == "RUNTIME_ERROR":
                                    re += 1
                                else:
                                    if item['verdict'] == "TIME_LIMIT_EXCEEDED":
                                        tle += 1
                                    else:
                                        if item['verdict'] == "MEMORY_LIMIT_EXCEEDED":
                                            mle += 1
                                        else:
                                            if item['verdict'] == "IDLENESS_LIMIT_EXCEEDED":
                                                ile += 1
                                            else:
                                                other += 1

                series_for_lang = []
                cl = Counter(languages)
                for item in cl:
                    series_for_lang.append({
                        'name': item,
                        'y': cl[item]
                    })

                first_time_ac = 0
                for i in solved_questions:
                    if i in unsolved:
                        unsolved.remove(i)
                    else:
                        first_time_ac += 1
                unsolved_problems = list()
                for i in unsolved:
                    pr_name = str(i[42:])
                    my_pr_name = ""
                    for j in pr_name:
                        if j != '/':
                            my_pr_name += j
                        else:
                            my_pr_name += '-'
                    unsolved_problems.append({'link': i, 'name': my_pr_name})

                ic = Counter(indexes)
                ser_a = []
                ser_b = []
                for item in sorted(ic):
                    ser_a.append(item)
                    ser_b.append(ic[item])

                tried = len(attempted)
                accepted = len(attempted) - len(unsolved)

                for i in range(50):
                    if solved_rating[i] > 0:
                        final_rating_solved.append(total_rating[i])
                        problem_count.append(solved_rating[i])

                survived_series = {
                    'name': 'Solved',
                    'data': problem_count,
                    'color': 'black'
                }

                chart = {
                    'chart': {'type': 'column',
                              'plotBackgroundColor': 'green'},
                    'title': {'text': 'Rating wise problems solved'},
                    'xAxis': {'categories': final_rating_solved},
                    'series': [survived_series],
                    'credits': {
                        'enabled': False
                    }
                }

                dump = json.dumps(chart)

                chart2 = {
                    'chart': {'type': 'pie',
                              'plotBackgroundColor': 'red'},
                    'title': {'text': 'Attempts'},
                    'tooltip': {
                        'pointFormat': 'percentage : <b>{point.percentage:.1f}%</b>'
                    },
                    'series': [{
                        'name': 'verdicts',
                        'data': [
                            {
                                'name': 'Accepted(' + str(ac) + ')',
                                'y': ac
                            }, {
                                'name': 'Wrong Answer(' + str(wa) + ')',
                                'y': wa
                            }, {
                                'name': 'Compilation Error(' + str(ce) + ')',
                                'y': ce
                            }, {
                                'name': 'Runtime Error(' + str(re) + ')',
                                'y': re
                            }, {
                                'name': 'Memory limit Exceeded(' + str(mle) + ')',
                                'y': mle
                            }, {
                                'name': 'Time Limit Exceeded(' + str(tle) + ')',
                                'y': tle
                            }, {
                                'name': 'Idleness Limit Exceeded(' + str(ile) + ')',
                                'y': ile
                            }, {
                                'name': 'other(' + str(other) + ')',
                                'y': other
                            }
                        ]
                    }],
                    'credits': {
                        'enabled': False
                    }
                }
                dump2 = json.dumps(chart2)

                chart3 = {
                    'chart': {'type': 'pie',
                              'plotBackgroundColor': 'blue',
                              },
                    'title': {'text': 'Languages used'},
                    'tooltip': {
                        'pointFormat': 'percentage : <b>{point.percentage:.1f}%</b>'
                    },
                    'series': [{
                        'name': 'verdicts',
                        'data': series_for_lang
                    }],
                    'credits': {
                        'enabled': False
                    }
                }
                dump3 = json.dumps(chart3)

                chart4 = {
                    'chart': {'type': 'column',
                              'plotBackgroundColor': 'grey'},
                    'title': {'text': 'index wise problems solved'},
                    'xAxis': {'categories': ser_a},
                    'series': [{
                        'name': 'Solved',
                        'data': ser_b,
                        'color': 'black'
                    }],
                    'credits': {
                        'enabled': False
                    }
                }

                dump4 = json.dumps(chart4)

                load = l['result'][:50]
                for i in load:
                    ak = 'https://codeforces.com/contest/' + str(i['contestId']) + '/submission/' + str(i['id'])
                    fuck = str(i['contestId']) + str(i['problem']['index']) + '-' + str(i['problem']['name'])
                    pro = 'https://codeforces.com/problemset/problem/' + str(i['contestId']) + '/' + str(i['problem']['index'])
                    sub.append({'sub_id': i['id'], 'contest': i['contestId'], 'name': fuck, 'lang': i['programmingLanguage'],
                                'verdict': i['verdict'], 'link': ak, 'link2': pro})

                avg_sub = (100 * attempt // accepted) / 100

                return render(request, 'analysis.html',
                              {'name': name, 'c': col, 'contest_count': contest_count, 'sub': sub, 'sol_num': 50,
                               'attempts': attempt,
                               'ac': ac, 'other': other, 'tried': tried, 'chart': dump, 'chart2': dump2, 'worst_rank': worst_rank,
                               'best_rank': best_rank, 'max_rating': max_rating, 'lowest_rating': lowest_rating,
                               'current_rating': current_rating, 'max_up': max_up, 'max_down': max_down, 'chart3': dump3,
                               'chart4': dump4, 'unsolved_problems': unsolved_problems, 'solved': accepted,
                               'first_attempt_correct': first_time_ac, 'avg_sub': avg_sub
                               })














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

    