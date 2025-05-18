from django.urls import path
from . import views

app_name = 'decks'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/decks/<int:deck_id>/cards/', views.get_deck_cards, name='get_deck_cards'),
    path('api/cards/<int:card_id>/review/', views.review_card, name='review_card'),
] 