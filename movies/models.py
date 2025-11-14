from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    duration_minutes = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g., 8.5
    thumbnail_url = models.URLField(max_length=500)
    video_url = models.URLField(max_length=500)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"