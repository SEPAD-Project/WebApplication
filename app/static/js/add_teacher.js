const national_code_input = document.getElementById('teacher_national_code');
const password_input = document.getElementById('teacher_password');

national_code_input.addEventListener('focus', () => {
national_code_input.placeholder = '';
});

national_code_input.addEventListener('blur', () => {
if (!national_code_input.value) {
    national_code_input.placeholder = 'Teacher National Code';
}
});

//===========================================

password_input.addEventListener('focus', () => {
password_input.placeholder = '';
});

password_input.addEventListener('blur', () => {
if (!password_input.value) {
    password_input.placeholder = 'Teacher Password';
}
});
