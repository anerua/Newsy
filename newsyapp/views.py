from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import http.client
import json

from .models import Story, Job, Comment


def get_stories(request):

    stories = Story.objects.all()

    return render(request, "newsyapp/index.html", {"stories": stories})


def get_jobs(request):

    jobs = Job.objects.all()

    return render(request, "newsyapp/jobs.html", {"jobs": jobs})


def get_story(request, item_id):

    if Story.objects.filter(id=item_id).exists():
        item = Story.objects.get(id=item_id)
        comments = item.kids.all()
        return render(request, "newsyapp/item_detail.html", {
            "type": "Story",
            "item": item,
            "comments": comments
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


def get_item(item_id):

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

    if Comment.objects.filter(id=item_id).exists():
        return Comment.objects.get(id=item_id)
    
    else:
        conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
        payload = "{}"
        conn.request("GET", f"/v0/item/{item_id}.json?print=pretty", payload)
        res = conn.getresponse()
        data = res.read()

        item = json.loads(data.decode("utf-8"))

        if item["type"] == "comment":
            new_comment = Comment(id=item["id"])
            if "by" in item and item["by"]:
                new_comment.by = item["by"]
            if "time" in item and item["time"]:
                new_comment.time = item["time"]
            if "parent" in item and item["parent"]:
                new_comment.parent = item["parent"]
            if "text" in item and item["text"]:
                new_comment.text = item["text"]
            new_comment.save()

            if "kids" in item and item["kids"]:
                for kid_id in item["kids"]:
                    comment = get_comment(kid_id)
                    new_comment.kids.add(comment)
            return new_comment
        else:
            raise Exception


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
    items_list = [x.strip() for x in items_list]

    added_stories = 0
    added_jobs = 0
    for item_id in items_list:
        if Story.objects.filter(id=item_id).exists() or Job.objects.filter(id=item_id).exists():
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


def update_stories(request):
    
    stories = Story.objects.in_bulk()
    stories_list = list(stories.values())

    count = 0

    for story_id in stories:
        new_info = get_item(str(story_id))
        if new_info:
            for kid_id in new_info['kids']:
                if not Comment.objects.filter(id=kid_id).exists():
                    new_comment = get_comment(kid_id)
                    stories[story_id].kids.add(new_comment)

            stories[story_id].descendants = new_info['descendants']
            stories[story_id].score = new_info['score']

        count += 1
        print(count, flush=True)

    Story.objects.bulk_update(stories_list, ['descendants', 'score'])

    return HttpResponse(f"Update successful!")
        

def delete_old_stories(request, new_id_list):
    old_stories = Story.objects.in_bulk()
    
    for story_id in old_stories:
        if str(story_id) not in new_id_list:
            old_stories[story_id].delete()
    

def delete_old_jobs(request, new_id_list):
    old_jobs = Job.objects.in_bulk()

    for job_id in old_jobs:
        if str(job_id) not in new_id_list:
            old_jobs[job_id].delete()


def delete_old_comments(request):

    for comment in Comment.objects.all():
        if (not Story.objects.filter(id=comment.parent).exists()) and (not Comment.objects.filter(id=comment.parent).exists()):
            comment.delete()