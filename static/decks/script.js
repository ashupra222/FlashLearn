function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

const modal = document.getElementById('reviewModal');
const flashcard = document.getElementById('flashcard');
const questionElem = document.getElementById('cardQuestion');
const answerElem = document.getElementById('cardAnswer');
const deckTitleElem = document.getElementById('deckTitle');
const progressIndicators = document.querySelectorAll('.progress-indicator');
const cardCounters = document.querySelectorAll('.card-counter');

// Add click event listener for the flashcard
flashcard.addEventListener('click', () => {
    flipCard();
});

let currentDeck = [];
let currentIndex = 0;
let isFlipped = false;
let stats = {
  known: 0,
  unknown: 0
};

const sampleCards = {
  Biology: [
    { 
      question: "What is the powerhouse of the cell?", 
      answer: "Mitochondria"
    },
    { 
      question: "What is the process by which plants make their food?", 
      answer: "Photosynthesis"
    },
    { 
      question: "What is the basic unit of life?", 
      answer: "Cell"
    }
  ],
  History: [
    { 
      question: "When did World War 2 start?", 
      answer: "1939"
    },
    { 
      question: "Who wrote '1984'?", 
      answer: "George Orwell"
    },
    { 
      question: "What was D-Day?", 
      answer: "The Allied invasion of Normandy on June 6, 1944"
    }
  ]
};

async function startReview(deckId) {
    try {
        // Fetch cards from the backend
        const response = await fetch(`/dashboard/api/decks/${deckId}/cards/`);
        if (!response.ok) {
            throw new Error('Failed to fetch cards');
        }
        const data = await response.json();
        
        if (!data.cards || data.cards.length === 0) {
            alert('No cards found in this deck!');
            return;
        }

        currentDeck = data.cards;
        deckTitleElem.textContent = data.deck_title;
        resetState();
        shuffleDeck();
        showCard();
        openModal();
        updateProgress();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load cards. Please try again.');
    }
}

function resetState() {
    currentIndex = 0;
    isFlipped = false;
    stats = { known: 0, unknown: 0 };
    flashcard.classList.remove('flipped');
}

function openModal() {
    modal.classList.remove('hidden');
    modal.classList.add('visible');
    flashcard.focus();
    document.addEventListener('keydown', handleKeyPress);
}

function shuffleDeck() {
    for (let i = currentDeck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [currentDeck[i], currentDeck[j]] = [currentDeck[j], currentDeck[i]];
    }
}

function showCard() {
    const card = currentDeck[currentIndex];
    fadeContent(false);
    
    setTimeout(() => {
        questionElem.textContent = card.question;
        answerElem.textContent = card.answer;
        
        if (isFlipped) {
            flashcard.classList.remove('flipped');
            isFlipped = false;
        }
        
        updateProgress();
        fadeContent(true);
    }, 300);
}

function fadeContent(fadeIn) {
    const opacity = fadeIn ? '1' : '0';
    questionElem.style.opacity = opacity;
    answerElem.style.opacity = opacity;
}

function flipCard() {
    isFlipped = !isFlipped;
    flashcard.classList.toggle('flipped');
}

async function markCard(known) {
    try {
        const card = currentDeck[currentIndex];
        
        // Update stats
        stats[known ? 'known' : 'unknown']++;
        
        // Send review result to backend
        await fetch(`/dashboard/api/cards/${card.id}/review/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ success: known })
        });

        if (currentIndex < currentDeck.length - 1) {
            currentIndex++;
            showCard();
        } else {
            showResults();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to save review result. Please try again.');
    }
}

function updateProgress() {
    const total = currentDeck.length;
    const current = currentIndex + 1;
    const percentage = Math.round((current/total) * 100);
    
    progressIndicators.forEach(progress => {
        progress.textContent = `Progress: ${percentage}%`;
    });
    
    cardCounters.forEach(counter => {
        counter.textContent = `${current}/${total}`;
    });
}

function showResults() {
    const total = currentDeck.length;  // Use total deck length instead of stats sum
    const correct = stats.known;
    const needsReview = stats.unknown;
    const percentage = Math.round((correct / total) * 100);
    
    const message = `
        🎉 Review Complete!
        
        Cards Reviewed: ${total}
        Correct: ${correct}
        Needs Review: ${needsReview}
        Success Rate: ${percentage}%
        
        Great job! Keep practicing to improve.
    `;
    
    alert(message);
    closeReview();
}

function handleKeyPress(e) {
    if (!modal.classList.contains('visible')) return;
    
    switch(e.key.toLowerCase()) {
        case ' ':
        case 'f':
            e.preventDefault();
            flipCard();
            break;
        case 'arrowright':
        case 'k':
            e.preventDefault();
            markCard(true);
            break;
        case 'arrowleft':
        case 'j':
            e.preventDefault();
            markCard(false);
            break;
        case 'escape':
            e.preventDefault();
            closeReview();
            break;
    }
}

function closeReview() {
    modal.classList.remove('visible');
    setTimeout(() => {
        modal.classList.add('hidden');
        resetState();
        document.removeEventListener('keydown', handleKeyPress);
    }, 300);
}

// Mobile Menu Toggle
function toggleMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navItems = document.querySelector('.nav-items');
    hamburger.classList.toggle('active');
    navItems.classList.toggle('active');
}

// Close menu when clicking a link
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', () => {
        const hamburger = document.querySelector('.hamburger');
        const navItems = document.querySelector('.nav-items');
        
        hamburger.classList.remove('active');
        navItems.classList.remove('active');
    });
});

// Utility function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}