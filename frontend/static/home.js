document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');

    if (searchForm && resultsContainer) { // Check if search form and results container exist
        searchForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(searchForm);
            const query = new URLSearchParams(formData).toString();

            const response = await fetch(`/search?${query}`);
            if (response.ok) {
                const results = await response.json();
                resultsContainer.innerHTML = '';
                
                results.forEach(book => {
                    console.log('Hi')
                    const bookElement = document.createElement('div');
                    bookElement.classList.add('book-item');
                    bookElement.innerHTML = `
                        <h3>${book.title}</h3>
                        <p>Author: ${book.author}</p>
                    `;
                    resultsContainer.appendChild(bookElement);
                });
            } else {
                resultsContainer.innerHTML = '<p>No books found.</p>';
            }
        });
    }
});
