from django.http import HttpResponse
from django.shortcuts import render
import http.client

# Create your views here.

def get_topstories(request):

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"

    conn.request("GET", "/v0/topstories.json?print=pretty", payload)

    res = conn.getresponse()
    data = res.read()

    items = data.decode("utf-8")

    items = items.replace("[", "")
    items = items.replace("]", "")
    
    news_list = items.split(",")

    return render(request, "newsyapp/index.html", {"news_list": news_list})


