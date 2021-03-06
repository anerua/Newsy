from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import http.client
import json, time

from .models import Story, Job


MAX_STORY_ITEMS = 1000
MAX_JOB_ITEMS = 1000

TOP_STORIES = 7
TOP_JOBS = 7

QUANTITY = 30

def home(request):

    yesterday_time = int(time.time()) - 86400
    stories = Story.objects.filter(time__gte=yesterday_time).order_by("-score")
    top_story = stories[0]
    top_stories = stories[1:TOP_STORIES]

    jobs = Job.objects.order_by('-time')
    top_job = jobs[0]
    top_jobs = jobs[1:TOP_JOBS]
    
    return render(request, "newsyapp/home.html", {
        "top_story": top_story,
        "top_stories": top_stories,
        "top_job": top_job,
        "top_jobs": top_jobs
    })


def stories(request):

    return render(request, "newsyapp/stories.html")


def get_stories(request):

    stories = Story.objects.order_by('-time')
    start = int(request.GET.get("start") or 0)
    quantity = int(request.GET.get("quantity") or QUANTITY)

    response = {}
    response["start"] = start
    response["quantity"] = quantity

    end = start + quantity
    if start >= stories.count():
        response["data"] = []
        return JsonResponse(response)
    elif start + quantity > stories.count():
        end = stories.count()

    data = []
    for i in range(start, end):
        story = stories[i]
        details = {
            "id": story.id,
            "by": story.by,
            "time": story.time,
            "descendants": story.descendants,
            "score": story.score,
            "title": story.title,
            "url": story.url,
        }
        data.append(details)
    
    response["data"] = data

    return JsonResponse(response)


def jobs(request):

    return render(request, "newsyapp/jobs.html")


def get_jobs(request):

    jobs = Job.objects.order_by('-time')
    start = int((request.GET.get("start") or 0))
    quantity = int(request.GET.get("quantity") or QUANTITY)

    response = {}
    response["start"] = start
    response["quantity"] = quantity

    end = start + quantity
    if start >= jobs.count():
        response["data"] = []
        return JsonResponse(response)
    elif start + quantity > jobs.count():
        end = jobs.count()

    data = []
    for i in range(start, end):
        job = jobs[i]
        details = {
            "id": job.id,
            "by": job.by,
            "time": job.time,
            "text": job.text,
            "title": job.title,
            "url": job.url,
        }
        data.append(details)
    
    response["data"] = data

    return JsonResponse(response)


def get_story(request, item_id):

    if Story.objects.filter(id=item_id).exists():
        item = Story.objects.get(id=item_id)
        return render(request, "newsyapp/item_detail.html", {
            "type": "Story",
            "item": item,
        })

    return HttpResponseNotFound()


def get_job(request, item_id):

    if Job.objects.filter(id=item_id).exists():
        item = Job.objects.get(id=item_id)
        return render(request, "newsyapp/item_detail.html", {
            "type": "Job",
            "item": item
        })

    return HttpResponseNotFound()


def fetch_item(item_id):

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
    payload = "{}"
    conn.request("GET", f"/v0/item/{item_id.strip()}.json?print=pretty", payload)
    res = conn.getresponse()
    data = res.read()

    item = json.loads(data.decode("utf-8"))

    if item["type"] == "story":
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
                    "descendants": descendants,
                    "score": score,
                    "title": item["title"],
                    "url": url}
        return details

    elif item["type"] == "job":
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


def update_stories():
    
    stories = Story.objects.in_bulk()
    stories_list = list(stories.values())

    count = 0

    for story_id in stories:
        new_info = fetch_item(str(story_id))
        if new_info:
            stories[story_id].descendants = new_info['descendants']
            stories[story_id].score = new_info['score']

        count += 1

    Story.objects.bulk_update(stories_list, ['descendants', 'score'])

    print(f"SUCCESSFULLY UPDATED {count} STORIES")
        

def delete_old_stories(new_id_list):

    if Story.objects.count() > MAX_STORY_ITEMS:
        
        all_stories = Story.objects.order_by('-time')
        old_stories = all_stories[MAX_STORY_ITEMS:]
        
        count = 0
        for story in old_stories:
            if str(story.id) not in new_id_list:
                story.delete()
                count += 1
        print(f"SUCCESSFULLY DELETED {count} OLD STORIES")
    else:
        print(f"THERE ARE NO OLD STORIES TO DELETE")
    

def delete_old_jobs(new_id_list):

    if Job.objects.count() > MAX_JOB_ITEMS:

        all_jobs = Job.objects.order_by('-time')
        old_jobs = all_jobs[MAX_JOB_ITEMS:]

        count = 0
        for job in old_jobs:
            if str(job.id) not in new_id_list:
                job.delete()
                count += 1
        print(f"SUCCESSFULLY DELETED {count} OLD JOBS")
    else:
        print(f"THERE ARE NO OLD JOBS TO DELETE")
