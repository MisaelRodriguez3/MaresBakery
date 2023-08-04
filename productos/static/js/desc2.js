const inputCantidad = document.getElementById('input-cantidad');
const btnIncrement = document.getElementById('increment');
const btnDecrement = document.getElementById('decrement');
// Agregamos un evento clic al botón de incrementar
btnIncrement.addEventListener('click', () => {
  // Obtenemos el valor actual del input
  let valorActual = parseInt(inputCantidad.value);
  
  // Incrementamos el valor en 1
  valorActual += 1;
  
  // Actualizamos el valor del input con el nuevo valor
  inputCantidad.value = valorActual;
});
btnDecrement.addEventListener('click', () => {
  let valorActual = parseInt(inputCantidad.value);
  if (valorActual > 1) {
    valorActual -= 1;
    inputCantidad.value = valorActual;
  }
});

// Toggle
// Constantes Toggle Titles
const toggleDescription = document.querySelector(
	'.title-description'
);

const toggleReviews = document.querySelector('.title-reviews');

// Constantes Contenido Texto
const contentDescription = document.querySelector(
	'.text-description'
);

const contentReviews = document.querySelector('.text-reviews');

// Funciones Toggle
toggleDescription.addEventListener('click', () => {
	contentDescription.classList.toggle('hidden');
});

toggleReviews.addEventListener('click', () => {
	contentReviews.classList.toggle('hidden');
});

//Carrusel

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