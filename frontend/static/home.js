document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');

    if (token) {
        document.getElementById('auth-link').innerHTML = '<a href="#" id="logout">Logout</a>';
        document.getElementById('auth-register-link').style.display = 'none';

        document.getElementById('logout').addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.href = '/login';
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');

    searchForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const formData = new FormData(searchForm);
        const query = new URLSearchParams(formData).toString();

        const response = await fetch(`/search?${query}`);
        if (response.ok) {
            const results = await response.json();
            resultsContainer.innerHTML = '';
            results.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.classList.add('book-item');
                bookElement.innerHTML = `
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                    <a href="/book/${book.id}">View Details</a>
                `;
                resultsContainer.appendChild(bookElement);
            });
        } else {
            resultsContainer.innerHTML = '<p>No books found.</p>';
        }
    });
});
