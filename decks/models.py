from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Deck(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)  # Store as comma-separated values
    image_url = models.URLField(max_length=500, blank=True, default="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&auto=format&fit=crop&q=60")  # Default study image

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    difficulty_level = models.IntegerField(default=0)  # 0: Easy, 1: Medium, 2: Hard

    def __str__(self):
        return f"{self.question[:50]}..."

    def mark_reviewed(self, success):
        self.last_reviewed = timezone.now()
        self.review_count += 1
        
        # Simple spaced repetition algorithm
        if success:
            # If successful, increase interval exponentially
            interval = 2 ** (self.review_count - 1) * 24  # hours
        else:
            # If failed, reset to review in 1 hour
            interval = 1
            self.review_count = 0
        
        self.next_review = timezone.now() + timezone.timedelta(hours=interval)
        self.save()

    class Meta:
        ordering = ['next_review']
