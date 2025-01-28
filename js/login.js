const username_input = document.getElementById('username');
const password_input = document.getElementById('password');

username_input.addEventListener('focus', () => {
username_input.placeholder = '';
});

username_input.addEventListener('blur', () => {
if (!username_input.value) {
    username_input.placeholder = 'username';
}
});

password_input.addEventListener('focus', () => {
password_input.placeholder = '';
});

password_input.addEventListener('blur', () => {
if (!password_input.value) {
    password_input.placeholder = 'password';
}
});
