document.addEventListener("DOMContentLoaded", function() {
    // Fetch featured books from backend
    fetch('/api/featured-books')
        .then(response => response.json())
        .then(data => {
            // Populate the "Featured Books" section with fetched data
            const bookList = document.querySelector('.book-list');
            data.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.classList.add('book');
                bookElement.innerHTML = `
                    <img src="${book.coverImageUrl}" alt="${book.title}">
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                    <p>ISBN: ${book.isbn}</p>
                `;
                bookList.appendChild(bookElement);
            });
        })
        .catch(error => console.error('Error fetching featured books:', error));

    // Search functionality
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');

    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm !== '') {
            // Perform search based on the search term (e.g., make AJAX request to backend)
            console.log('Search term:', searchTerm);
            // You can perform a search by name, author, and ISBN number here
            // For demonstration purposes, let's log the search term
        }
    });

    // Displaying latest updates
    const updatesList = document.getElementById('updates-list');

    // Dummy data for latest updates (replace with actual data from backend)
    const latestUpdates = [
        { text: 'New book added: "The Great Gatsby" by F. Scott Fitzgerald' },
        { text: 'Upcoming author event: Meet J.K. Rowling on April 15th' }
    ];

    // Populate the "Latest Updates" section with dummy data
    latestUpdates.forEach(update => {
        const updateItem = document.createElement('li');
        updateItem.textContent = update.text;
        updatesList.appendChild(updateItem);
    });
});