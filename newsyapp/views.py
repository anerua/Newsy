from django.shortcuts import render
import http.client
import json, time

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
    
    items_list = items.split(",")

    news_list = []
    for item_id in items_list[0:30]:
        item = get_item(item_id)
        if item:
            news_list.append((get_item(item_id)))

    return render(request, "newsyapp/index.html", {"news_list": news_list})


def get_item(item_id):

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"

    conn.request("GET", f"/v0/item/{item_id.strip()}.json?print=pretty", payload)

    res = conn.getresponse()
    data = res.read()

    item = json.loads(data.decode("utf-8"))

    if item["type"] not in ["job", "story"]:
        return False

    item_time = int(item["time"])
    elapsed_time = get_elapsed_time(item_time)

    details = {"id": item["id"], "title": item["title"], "time": elapsed_time}
    if "url" in item:
        details["url"] = item["url"]

    return details


def get_elapsed_time(item_time):

    diff_time = int(time.time()) - item_time

    if diff_time / 86400 < 1:
        if int(diff_time/3600) < 1:
            if int(diff_time/60) < 1:
                return f"{int(diff_time)} seconds ago"
            else:
                return f"{int(diff_time/60)} minutes ago"
        else:
            return f"{int(diff_time/3600)} hours ago"
    else:
        return f"{int(diff_time/86400)} days ago"
