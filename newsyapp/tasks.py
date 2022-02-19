from celery import shared_task
import http.client

from .models import Job
from newsyapp import views

# from celery import Celery


# app = Celery()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(60.0, sync_jobs_task.s(), name='add-every-10', expires=30)


@shared_task
def sync_jobs_task():

    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")
    payload = "{}"
    conn.request("GET", "/v0/jobstories.json?print=pretty", payload)
    res = conn.getresponse()
    data = res.read()

    jobs = data.decode("utf-8")
    jobs = jobs.replace("[", "")
    jobs = jobs.replace("]", "")
    
    jobs_list = jobs.split(",")
    jobs_list = [x.strip() for x in jobs_list]

    added_jobs = 0
    for job_id in jobs_list:
        if Job.objects.filter(id=job_id).exists():
            continue

        response = views.fetch_item(job_id)
        if response and response["type"] == "job":
                Job.objects.create(id=response["id"],
                                    by=response["by"],
                                    time=response["time"],
                                    text=response["text"],
                                    title=response["title"],
                                    url=response["url"])
                added_jobs += 1

    print(f"SUCCESSFULLY ADDED {added_jobs} NEW JOBS TO THE DATABASE")

    views.delete_old_jobs(jobs_list)

# app.conf.beat_schedule = {
#     'add-every-10': {
#         'task': 'tasks.sync_jobs_task',
#         'schedule': 60.0,
#         # 'args': (16, 16)
#     },
# }