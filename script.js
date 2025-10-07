document.addEventListener('DOMContentLoaded', () => {
    const drawButton = document.getElementById('draw-card-btn');
    const cardDisplayContainer = document.getElementById('card-display-container');
    const cardFlipper = document.querySelector('.card-flipper');

    // Card front elements
    const cardName = document.getElementById('card-name');
    const cardImage = document.getElementById('card-image');
    const cardDescription = document.getElementById('card-description');
    const uprightHeader = document.getElementById('upright-header');
    const uprightMeaningEl = document.getElementById('upright-meaning');
    const reversedHeader = document.getElementById('reversed-header');
    const reversedMeaningEl = document.getElementById('reversed-meaning');

    let cardsData = [];
    let isCardShowing = false;

    // Fetch card data from JSON file
    fetch('cards.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            cardsData = data;
        })
        .catch(error => {
            console.error('Error fetching card data:', error);
            const container = document.querySelector('.tarot-container');
            container.innerHTML = '<h1>Error</h1><p>Could not load card data. Please check the console for details and try again later.</p>';
        });

    function drawAndRevealCard() {
        if (cardsData.length === 0) {
            alert('Card data is not loaded yet. Please wait a moment and try again.');
            return;
        }

        // Randomly select a card
        const randomIndex = Math.floor(Math.random() * cardsData.length);
        const selectedCard = cardsData[randomIndex];

        // Randomly decide if the card is upright or reversed
        const isReversed = Math.random() < 0.5;

        // Populate the card front elements
        cardName.textContent = selectedCard.name;
        cardImage.src = selectedCard.image;
        cardImage.alt = selectedCard.name;
        cardDescription.textContent = selectedCard.description;

        if (isReversed) {
            cardName.textContent += ' (Reversed)';
            uprightHeader.style.display = 'none';
            uprightMeaningEl.style.display = 'none';
            reversedHeader.style.display = 'block';
            reversedMeaningEl.style.display = 'block';
            reversedMeaningEl.textContent = selectedCard.interpretation.reversed;
        } else {
            cardName.textContent += ' (Upright)';
            reversedHeader.style.display = 'none';
            reversedMeaningEl.style.display = 'none';
            uprightHeader.style.display = 'block';
            uprightMeaningEl.style.display = 'block';
            uprightMeaningEl.textContent = selectedCard.interpretation.upright;
        }

        // Flip to the front
        cardFlipper.classList.add('flipped');
        isCardShowing = true;
    }

    drawButton.addEventListener('click', () => {
        if (isCardShowing) {
            // If a card is already showing, flip it back first
            cardFlipper.classList.remove('flipped');
            // Wait for the flip-back animation to complete before drawing a new card
            setTimeout(drawAndRevealCard, 500); // 500ms is half of the 0.9s transition
        } else {
            // If it's the first draw, show the container and draw
            cardDisplayContainer.classList.remove('hidden');
            drawAndRevealCard();
        }
    });
});