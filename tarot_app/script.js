document.addEventListener('DOMContentLoaded', () => {
    const drawButton = document.getElementById('draw-card-btn');
    const cardDisplayContainer = document.getElementById('card-display-container');
    const cardFlipper = document.querySelector('.card-flipper');

    // Card front elements
    const cardName = document.getElementById('card-name');
    const cardImage = document.getElementById('card-image');
    const cardSymbolism = document.getElementById('card-symbolism');
    const cardWisdom = document.getElementById('card-wisdom');

    const uprightSection = document.getElementById('upright-section');
    const uprightMeaningEl = document.getElementById('upright-meaning');
    const uprightAdviceEl = document.getElementById('upright-advice');

    const reversedSection = document.getElementById('reversed-section');
    const reversedMeaningEl = document.getElementById('reversed-meaning');
    const reversedQuestionEl = document.getElementById('reversed-question');

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

        const randomIndex = Math.floor(Math.random() * cardsData.length);
        const selectedCard = cardsData[randomIndex];
        const isReversed = Math.random() < 0.5;

        // Populate common elements
        cardName.textContent = selectedCard.name;
        cardImage.src = selectedCard.image;
        cardImage.alt = selectedCard.name;

        // Safely access nested properties
        const interpretation = selectedCard.interpretation || {};
        cardSymbolism.textContent = interpretation.symbolism || '';
        cardWisdom.textContent = interpretation.wisdom || '';

        // Populate upright/reversed sections
        if (isReversed) {
            cardName.textContent += ' (Reversed)';
            uprightSection.style.display = 'none';
            reversedSection.style.display = 'block';

            const reversedData = interpretation.reversed || {};
            reversedMeaningEl.textContent = reversedData.meaning || '';
            reversedQuestionEl.textContent = reversedData.question || '';
        } else {
            cardName.textContent += ' (Upright)';
            reversedSection.style.display = 'none';
            uprightSection.style.display = 'block';

            const uprightData = interpretation.upright || {};
            uprightMeaningEl.textContent = uprightData.meaning || '';
            uprightAdviceEl.textContent = uprightData.advice || '';
        }

        // Flip to the front
        cardFlipper.classList.add('flipped');
        isCardShowing = true;
    }

    drawButton.addEventListener('click', () => {
        if (isCardShowing) {
            // Flip back before drawing a new card
            cardFlipper.classList.remove('flipped');
            setTimeout(drawAndRevealCard, 500);
        } else {
            // First draw
            cardDisplayContainer.classList.remove('hidden');
            drawAndRevealCard();
        }
    });
});