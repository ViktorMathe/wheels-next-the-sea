from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Review(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200]
        super().save(*args, **kwargs)