const iconMenu = document.querySelector('.menu__icon');
const menuBody = document.querySelector('.menu__body');
if (iconMenu){
    iconMenu.addEventListener("click", function(e){
        iconMenu.classList.toggle("_active");
        menuBody.classList.toggle("_active");
        document.body.classList.toggle("_active")
    });
}