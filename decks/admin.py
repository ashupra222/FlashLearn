from django.contrib import admin
from .models import Deck, Card

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'updated_at', 'is_public')
    list_filter = ('is_public', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'tags')
    date_hierarchy = 'created_at'

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'deck', 'review_count', 'last_reviewed', 'next_review')
    list_filter = ('deck', 'created_at', 'difficulty_level')
    search_fields = ('question', 'answer')
    date_hierarchy = 'created_at'
