const name_input = document.getElementById('student_name');
const family_input = document.getElementById('student_family');
const national_code_input = document.getElementById('student_national_code');
const password_input = document.getElementById('student_password');

name_input.addEventListener('focus', () => {
name_input.placeholder = '';
});

name_input.addEventListener('blur', () => {
if (!name_input.value) {
    name_input.placeholder = 'Student Name';
}
});

//===========================================

family_input.addEventListener('focus', () => {
family_input.placeholder = '';
});

family_input.addEventListener('blur', () => {
if (!family_input.value) {
    family_input.placeholder = 'Student Family';
}
});

//===========================================

national_code_input.addEventListener('focus', () => {
    national_code_input.placeholder = '';
});

national_code_input.addEventListener('blur', () => {
if (!national_code_input.value) {
    national_code_input.placeholder = 'Student National Code';
}
});

//===========================================

password_input.addEventListener('focus', () => {
    password_input.placeholder = '';
});

password_input.addEventListener('blur', () => {
if (!password_input.value) {
    password_input.placeholder = 'Student Password';
}
});