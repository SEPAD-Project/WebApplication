const school_name = document.getElementById('school-name');
const school_code = document.getElementById('school-code');
const manager_personal_code = document.getElementById('manager-personal-code');
const province = document.getElementById('province');
const city = document.getElementById('city');

school_name.addEventListener('focus', () => {
school_name.placeholder = '';
});

school_name.addEventListener('blur', () => {
if (!school_name.value) {
    school_name.placeholder = 'School name';
}
});

//=============================================

school_code.addEventListener('focus', () => {
school_code.placeholder = '';
});

school_code.addEventListener('blur', () => {
if (!school_code.value) {
    school_code.placeholder = 'School code';
}
});

//=============================================

manager_personal_code.addEventListener('focus', () => {
    manager_personal_code.placeholder = '';
});
    
manager_personal_code.addEventListener('blur', () => {
if (!manager_personal_code.value) {
    manager_personal_code.placeholder = 'Manager personal code';
}
});

//=============================================

province.addEventListener('focus', () => {
    province.placeholder = '';
});
    
province.addEventListener('blur', () => {
if (!province.value) {
    province.placeholder = 'province';
}
});

//=============================================

city.addEventListener('focus', () => {
    city.placeholder = '';
});
    
city.addEventListener('blur', () => {
if (!city.value) {
    city.placeholder = 'city';
}
});