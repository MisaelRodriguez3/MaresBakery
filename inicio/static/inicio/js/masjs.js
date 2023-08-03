const slider = document.querySelector('.slider-container');
let slidePosition = 0;
const slides = document.querySelectorAll('.item');
const totalSlides = slides.length;
const slideWidth = slides[0].offsetWidth;

// Calcula el ancho total del carrusel
const totalWidth = slideWidth * totalSlides;

// Clona los elementos y los agrega al final del carrusel
slider.innerHTML += slider.innerHTML;

// Ajusta el ancho del contenedor según el totalWidth
slider.style.width = `${totalWidth * 2}px`;

// Función para mover el carrusel a la siguiente posición
function moveToNextSlide() {
    slidePosition++;
    slider.style.transition = 'transform 0.5s ease';
    slider.style.transform = `translateX(-${slideWidth * slidePosition}px)`;

    if (slidePosition === totalSlides) {
        setTimeout(() => {
            slider.style.transition = 'none';
            slider.style.transform = 'translateX(0)';
            slidePosition = 0;
        }, 500);
    }
}

// Configura el intervalo para mover automáticamente el carrusel cada 3 segundos
setInterval(moveToNextSlide, 3000);