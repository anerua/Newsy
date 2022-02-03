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

    item_type = get_item_type(item_id)
    if item_type in [Story, Job]:
        item = item_exists(item_id, item_type)
        if item and item_type == Job:
            return render(request, "newsyapp/item_detail.html", {
                "type": "Job",
                "item": item
            })
        elif item and item_type == Story:
            comments = []
            for comment_id in item.kids.all():
                comments.append(get_comment(comment_id))
            return render(request, "newsyapp/item_detail.html", {
                "type": "Story",
                "item": item,
                "comments": comments
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

        kids = None
        if "kids" in item:
            kids = item["kids"]
        if item["type"] == "comment":
            new_comment = Comment(id=item["id"],
                                    by=item["by"],
                                    time=item["time"],
                                    parent=item["parent"],
                                    kids=kids,
                                    text=item["text"])
            new_comment.save()
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
                new_story = Story(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    descendants=response["descendants"],
                                    score=response["score"],
                                    title=response["title"],
                                    url=response["url"])
                new_story.save()
                added_stories += 1
            elif response["type"] == "job":
                new_job = Job(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    text=response["text"],
                                    title=response["title"],
                                    url=response["url"])
                new_job.save()
                added_jobs += 1
            else:
                print("How on Earth did you get here!!!")
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