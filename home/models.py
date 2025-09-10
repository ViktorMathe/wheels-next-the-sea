from django.db import models
import re

class AboutUs(models.Model):
    content = models.TextField()  # CKEditor5 will handle rich text

    def __str__(self):
        return "About Us Content"
    
    def save(self, *args, **kwargs):
        # enforce target="_blank" on all links before saving
        self.content = re.sub(r'<a ', '<a target="_blank" ', self.content)
        super().save(*args, **kwargs)