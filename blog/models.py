from django.db import models
CATEGORY_CHOICES = [
    ('others', 'Others'),
    ('industry_updates', 'Industry Updates'),
    ('resources', 'Resources')
]

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='blog_images/')
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='others')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title