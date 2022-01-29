from django.http import HttpResponse
from django.shortcuts import render
import http.client
import json, time

from .models import Story, Job

# Create your views here.

def get_stories(request):

    stories = Story.objects.all()

    return render(request, "newsyapp/index.html", {"stories": stories})


def get_item(item_id):

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"

    conn.request("GET", f"/v0/item/{item_id.strip()}.json?print=pretty", payload)

    res = conn.getresponse()
    data = res.read()

    item = json.loads(data.decode("utf-8"))

    if item["type"] == "story":
        # item_time = int(item["time"])
        # elapsed_time = get_elapsed_time(item_time)

        descendants = None
        score = None
        url = None
        if "descendants" in item:
            descendants = item["descendants"]
        if "score" in item:
            score = item["score"]
        if "url" in item:
            url = item["url"]

        details = {"id": item["id"],
                    "type": item["type"],
                    "by": item["by"],
                    "time": item["time"],
                    # "kids": item["kids"], Use when Comments model is created
                    "descendants": descendants,
                    "score": score,
                    "title": item["title"],
                    "url": url}
        return details

    elif item["type"] == "job":
        # item_time = int(item["time"])
        # elapsed_time = get_elapsed_time(item_time)

        text = ""
        url = None
        if "text" in item:
            text = item["text"]
        if "url" in item:
            url = item["url"]


        details = {"id": item["id"],
                    "type": item["type"],
                    "by": item["by"],
                    "time": item["time"],
                    # "kids": item["kids"], Use when Comments model is created
                    "text": text,
                    "title": item["title"],
                    "url": url}
        return details
    
    else:
        return False

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


def sync_db(request):

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"

    conn.request("GET", "/v0/topstories.json?print=pretty", payload)

    res = conn.getresponse()
    data = res.read()

    items = data.decode("utf-8")

    items = items.replace("[", "")
    items = items.replace("]", "")
    
    items_list = items.split(",")

    added_no = 0
    for item_id in items_list[:50]:
        if item_exists(item_id, Story):
            continue
        if item_exists(item_id, Job):
            continue

        response = get_item(item_id)

        if response:
            if response["type"] == "story":
                new_story = Story(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    descendants=response["descendants"],
                                    score=response["score"],
                                    title=response["title"],
                                    url=response["url"])
                new_story.save()
                added_no += 1
            elif response["type"] == "job":
                new_story = Job(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    text=response["text"],
                                    title=response["title"],
                                    url=response["url"])
                new_story.save()
                added_no += 1
            else:
                print("How on Earth did you get here!!!")
    return HttpResponse(f"Successfully added {added_no} new items to the database!")


def item_exists(item_id, my_model):
    try:
        _ = my_model.objects.get(id=item_id)
        return True
    except my_model.DoesNotExist:
        return False