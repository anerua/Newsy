from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import http.client
import json

from .models import Story, Job, Comment


MAX_STORY_ITEMS = 1000
MAX_JOB_ITEMS = 1000


def get_stories(request):

    stories = Story.objects.order_by('-time')

    return render(request, "newsyapp/index.html", {"stories": stories})


def get_jobs(request):

    jobs = Job.objects.order_by('-time')

    return render(request, "newsyapp/jobs.html", {"jobs": jobs})


def get_story(request, item_id):

    if Story.objects.filter(id=item_id).exists():
        item = Story.objects.get(id=item_id)
        # comments = item.kids.all()
        return render(request, "newsyapp/item_detail.html", {
            "type": "Story",
            "item": item,
            # "comments": comments
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
        # kids = None
        # if "kids" in item:
        #     kids = item["kids"]
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
                    # "kids": kids,
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


# def fetch_or_get_comment(item_id):

#     if Comment.objects.filter(id=item_id).exists():
#         return Comment.objects.get(id=item_id)
    
#     else:
#         conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
#         payload = "{}"
#         conn.request("GET", f"/v0/item/{item_id}.json?print=pretty", payload)
#         res = conn.getresponse()
#         data = res.read()

#         item = json.loads(data.decode("utf-8"))

#         if item["type"] == "comment":
#             new_comment = Comment(id=item["id"])
#             if "by" in item and item["by"]:
#                 new_comment.by = item["by"]
#             if "time" in item and item["time"]:
#                 new_comment.time = item["time"]
#             if "parent" in item and item["parent"]:
#                 new_comment.parent = item["parent"]
#             if "text" in item and item["text"]:
#                 new_comment.text = item["text"]
#             new_comment.save()

#             if "kids" in item and item["kids"]:
#                 for kid_id in item["kids"]:
#                     comment = fetch_or_get_comment(kid_id)
#                     new_comment.kids.add(comment)
#             return new_comment
#         else:
#             raise Exception


def update_stories():
    
    stories = Story.objects.in_bulk()
    stories_list = list(stories.values())

    count = 0

    for story_id in stories:
        new_info = fetch_item(str(story_id))
        if new_info:
            # for kid_id in new_info['kids']:
            #     if not Comment.objects.filter(id=kid_id).exists():
            #         new_comment = fetch_or_get_comment(kid_id)
            #         stories[story_id].kids.add(new_comment)

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


# def delete_old_comments():

#     count = 0
#     for comment in Comment.objects.all():
#         if (not Story.objects.filter(id=comment.parent).exists()) and (not Comment.objects.filter(id=comment.parent).exists()):
#             comment.delete()
#             count += 1
    
#     print(f"SUCCESSFULLY DELETED {count} COMMENTS")