from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import http.client
import json, time

from .models import Story, Job, Comment

# Create your views here.

def get_stories(request):

    stories = Story.objects.all()

    return render(request, "newsyapp/index.html", {"stories": stories})


def get_jobs(request):

    jobs = Job.objects.all()

    return render(request, "newsyapp/jobs.html", {"jobs": jobs})


def get_detail(request, item_id):

    if Story.objects.filter(id=item_id).exists():
        item = Story.objects.get(id=item_id)
        comments = []
        for comment in item.kids.all():
            comments.append(comment)
        return render(request, "newsyapp/item_detail.html", {
            "type": "Story",
            "item": item,
            "comments": comments
        })
    elif Job.objects.filter(id=item_id).exists():
        item = Job.objects.get(id=item_id)
        return render(request, "newsyapp/item_detail.html", {
            "type": "Job",
            "item": item
        })

    return HttpResponseNotFound()

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
        kids = None
        if "kids" in item:
            kids = item["kids"]
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
                    "kids": kids,
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
                    "text": text,
                    "title": item["title"],
                    "url": url}
        return details
    
    else:
        return False


def get_comment(item_id):

    comment = item_exists(item_id, Comment)
    if comment:
        return comment
    else:

        conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

        payload = "{}"

        conn.request("GET", f"/v0/item/{item_id}.json?print=pretty", payload)

        res = conn.getresponse()
        data = res.read()

        item = json.loads(data.decode("utf-8"))
        

        if item["type"] == "comment":
            new_comment = Comment.objects.create(id=item["id"])
            if "by" in item and item["by"]:
                new_comment.by = item["by"]
            if "time" in item and item["time"]:
                new_comment.time = item["time"]
            if "parent" in item and item["parent"]:
                new_comment.parent = item["parent"]
            if "text" in item and item["text"]:
                new_comment.text = item["text"]

            if "kids" in item and item["kids"]:
                for kid_id in item["kids"]:
                    comment = get_comment(kid_id)
                    new_comment.kids.add(comment)
            return new_comment
        else:
            raise Exception
    

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

    added_stories = 0
    added_jobs = 0
    for item_id in items_list:
        if item_exists(item_id, Story):
            continue
        if item_exists(item_id, Job):
            continue

        response = get_item(item_id)

        if response:
            if response["type"] == "story":
                new_story = Story.objects.create(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    descendants=response["descendants"],
                                    score=response["score"],
                                    title=response["title"],
                                    url=response["url"])
                if "kids" in response and response["kids"]:
                    for kid_id in response["kids"]:
                        comment = get_comment(kid_id)
                        new_story.kids.add(comment)

                added_stories += 1
            elif response["type"] == "job":
                new_job = Job.objects.create(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    text=response["text"],
                                    title=response["title"],
                                    url=response["url"])
                added_jobs += 1
            else:
                print("How on Earth did you get here!!!")
                raise Exception
    return HttpResponse(f"Successfully added {added_stories} new stories and {added_jobs} new jobs to the database!")


def item_exists(item_id, my_model):
    try:
        _ = my_model.objects.get(id=item_id)
        return _
    except my_model.DoesNotExist:
        return False


def get_item_type(item_id):
    
    if item_exists(item_id, Story):
        return Story
    elif item_exists(item_id, Job):
        return Job
    elif item_exists(item_id, Comment):
        return Comment
    else:
        return False