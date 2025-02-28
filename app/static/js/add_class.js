const name_input = document.getElementById('class_name');

name_input.addEventListener('focus', () => {
name_input.placeholder = '';
});

name_input.addEventListener('blur', () => {
if (!name_input.value) {
    name_input.placeholder = 'Class Name';
}
});
