from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class CommType(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Comm(models.Model):
    title = models.CharField(max_length=140, blank=True)
    author = models.CharField(max_length=100, blank=True)
    post_date = models.DateField(default=timezone.now, blank=True)
    img_hero_src = models.CharField(max_length=255, blank=True)
    img_hero_title = models.CharField(max_length=80, blank=True)
    img_thumb_src = models.CharField(max_length=255, blank=True)
    img_thumb_title = models.CharField(max_length=80, blank=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField(blank=True)
    commtype = models.ForeignKey(CommType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    tags = models.ManyToManyField(Tag, default=None)

    class Meta:
        ordering = ["-post_date"]

    # use to represent the object
    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField(max_length=140, blank=True)
    img_thumb_src = models.CharField(max_length=255, blank=True)
    img_thumb_title = models.CharField(max_length=80, blank=True)
    img_gallery_src = models.CharField(max_length=255, blank=True)
    img_gallery_title = models.CharField(max_length=80, blank=True)
    category = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(default=timezone.now, blank=True)
    end_date = models.DateField(default=timezone.now, blank=True)
    short_desc = models.CharField(max_length=255, blank=True)
    long_desc = models.TextField(blank=True)
    img1_src = models.CharField(max_length=255, blank=True)
    img1_title = models.CharField(max_length=80, blank=True)
    img2_src = models.CharField(max_length=255, blank=True)
    img2_title = models.CharField(max_length=80, blank=True)
    img3_src = models.CharField(max_length=255, blank=True)
    img3_title = models.CharField(max_length=80, blank=True)
    client = models.CharField(max_length=200, blank=True)
    categories = models.ManyToManyField(Category, default=None)
    # commtype = models.ForeignKey(CommType, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ["-end_date"]

    # use to represent the object
    def __str__(self):
        return self.title


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=140)
    received_date = models.DateField(default=timezone.now)
    body = models.TextField()








