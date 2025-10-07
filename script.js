document.addEventListener('DOMContentLoaded', () => {
    const drawButton = document.getElementById('draw-card-btn');
    const cardDisplay = document.getElementById('card-display');
    const cardName = document.getElementById('card-name');
    const cardImage = document.getElementById('card-image');
    const cardDescription = document.getElementById('card-description');
    const uprightMeaningEl = document.getElementById('upright-meaning');
    const reversedMeaningEl = document.getElementById('reversed-meaning');
    const uprightHeader = uprightMeaningEl.previousElementSibling;
    const reversedHeader = reversedMeaningEl.previousElementSibling;

    let cardsData = [];

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

    drawButton.addEventListener('click', () => {
        if (cardsData.length === 0) {
            alert('Card data is not loaded yet. Please wait a moment and try again.');
            return;
        }

        // Randomly select a card
        const randomIndex = Math.floor(Math.random() * cardsData.length);
        const selectedCard = cardsData[randomIndex];

        // Randomly decide if the card is upright or reversed
        const isReversed = Math.random() < 0.5;

        // Populate the card display elements
        cardName.textContent = selectedCard.name;
        cardImage.src = selectedCard.image;
        cardImage.alt = selectedCard.name;
        cardDescription.textContent = selectedCard.description;

        if (isReversed) {
            cardName.textContent += ' (Reversed)';
            uprightMeaningEl.style.display = 'none';
            uprightHeader.style.display = 'none';
            reversedMeaningEl.style.display = 'block';
            reversedHeader.style.display = 'block';
            reversedMeaningEl.textContent = selectedCard.interpretation.reversed;
        } else {
            cardName.textContent += ' (Upright)';
            reversedMeaningEl.style.display = 'none';
            reversedHeader.style.display = 'none';
            uprightMeaningEl.style.display = 'block';
            uprightHeader.style.display = 'block';
            uprightMeaningEl.textContent = selectedCard.interpretation.upright;
        }

        // Show the card display
        cardDisplay.classList.remove('hidden');
    });
});