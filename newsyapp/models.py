from django.db import models


class Story(models.Model):
    id = models.IntegerField(primary_key=True)
    by = models.CharField(max_length=64, blank=True)
    time = models.IntegerField(blank=True, null=True)
    # kids = models.ManyToManyField("Comment", blank=True, related_name="stories") # use when Comment model is created
    descendants = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)


class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    by = models.CharField(max_length=64, blank=True)
    time = models.IntegerField(blank=True, null=True)
    # kids = models.ManyToManyField("Comment", blank=True, related_name="jobs") # use when Comment model is created
    text = models.TextField(blank=True)
    title = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)