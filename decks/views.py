from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import Deck, Card

# Create your views here.

@login_required
def home(request):
    # Get user's decks
    user_decks = Deck.objects.filter(owner=request.user)
    
    # Get public decks (excluding user's own decks)
    public_decks = Deck.objects.filter(is_public=True).exclude(owner=request.user)
    
    # For each deck, get the progress stats
    for deck in user_decks:
        total_cards = deck.cards.count()
        mastered_cards = deck.cards.filter(review_count__gte=5).count()  # Consider cards reviewed 5+ times as mastered
        due_cards = deck.cards.filter(next_review__lte=timezone.now()).count()
        
        deck.total_cards = total_cards
        deck.mastered_cards = mastered_cards
        deck.due_cards = due_cards
        deck.progress = (mastered_cards / total_cards * 100) if total_cards > 0 else 0
    
    context = {
        'user_decks': user_decks,
        'public_decks': public_decks,
    }
    
    return render(request, 'decks/index.html', context)

@login_required
def get_deck_cards(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    
    # Check if user has access to the deck
    if not deck.is_public and deck.owner != request.user:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    cards = deck.cards.all()
    cards_data = [
        {
            'id': card.id,
            'question': card.question,
            'answer': card.answer,
        }
        for card in cards
    ]
    
    return JsonResponse({
        'deck_title': deck.title,
        'cards': cards_data
    })

@login_required
def review_card(request, card_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    card = get_object_or_404(Card, id=card_id)
    
    # Check if user has access to the card's deck
    if not card.deck.is_public and card.deck.owner != request.user:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        success = data.get('success', False)
        
        # Update card review status
        card.mark_reviewed(success)
        
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
