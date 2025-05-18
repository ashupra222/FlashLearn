from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decks.models import Deck, Card
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates dummy data for testing'

    def handle(self, *args, **kwargs):
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            email='test@example.com'
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: testuser'))

        # Python Programming Deck
        python_deck = Deck.objects.create(
            title='Python Programming Basics',
            description='Learn the fundamentals of Python programming language',
            owner=user,
            tags='#programming #python #basics',
            is_public=True,
            image_url='https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&auto=format&fit=crop&q=60'
        )

        # Python Cards
        Card.objects.create(
            deck=python_deck,
            question='What is Python?',
            answer='Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and released in 1991.'
        )

        Card.objects.create(
            deck=python_deck,
            question='What are Python\'s main data types?',
            answer='The main data types in Python are:\n- Numbers (int, float)\n- Strings (str)\n- Lists\n- Tuples\n- Dictionaries\n- Sets\n- Booleans'
        )

        Card.objects.create(
            deck=python_deck,
            question='What is a Python list comprehension?',
            answer='A list comprehension is a concise way to create lists in Python. It consists of brackets containing an expression followed by a for clause, then zero or more for or if clauses.\nExample: [x*2 for x in range(5)]'
        )

        # Web Development Deck
        web_deck = Deck.objects.create(
            title='Web Development Fundamentals',
            description='Master the basics of web development with HTML, CSS, and JavaScript',
            owner=user,
            tags='#webdev #html #css #javascript',
            is_public=True,
            image_url='https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=800&auto=format&fit=crop&q=60'
        )

        # Web Development Cards
        Card.objects.create(
            deck=web_deck,
            question='What is HTML?',
            answer='HTML (HyperText Markup Language) is the standard markup language for creating web pages. It describes the structure of web pages using markup.'
        )

        Card.objects.create(
            deck=web_deck,
            question='What is CSS used for?',
            answer='CSS (Cascading Style Sheets) is used for describing the presentation of a document written in HTML. It describes how elements should be rendered on screen, on paper, in speech, or on other media.'
        )

        Card.objects.create(
            deck=web_deck,
            question='What is JavaScript?',
            answer='JavaScript is a programming language that enables interactive web pages. It is an essential part of web applications and can be used for:\n- Dynamic content updates\n- Interactive features\n- Form validation\n- Animations'
        )

        self.stdout.write(self.style.SUCCESS('Successfully created dummy data')) 