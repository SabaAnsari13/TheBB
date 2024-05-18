document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();  // Prevent the default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password
            }),
        });

        if (response.ok) {
            window.location.href = '/home';
        } else {
            const result = await response.json();
            errorMessage.textContent = result.detail;
        }
    } catch (error) {
        errorMessage.textContent = 'An error occurred. Please try again.';
    }
});
