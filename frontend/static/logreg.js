document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': username,
                'password': password
            }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            window.location.href = '/home';
        } else {
            // Handle error
            alert('Login failed. Please check your username and password.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
