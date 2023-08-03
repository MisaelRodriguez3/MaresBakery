window.addEventListener("scroll", function(){
  var header = document.querySelector(".nav-bar");
  header.classList.toggle('down', window.scrollY > 0)});


const body = document.querySelector("body"),
      nav = document.querySelector("nav"),
      modeToggle = document.querySelector(".dark-light"),
      searchToggle = document.querySelector(".searchToggle"),
      sidebarOpen = document.querySelector(".sidebarOpen"),
      siderbarClose = document.querySelector(".siderbarClose");

      let getMode = localStorage.getItem("mode");
          if(getMode && getMode === "dark-mode"){
            body.classList.add("dark");
          }


        searchToggle.addEventListener("click" , () =>{
        searchToggle.classList.toggle("active");
      });
 
      

sidebarOpen.addEventListener("click" , () =>{
    nav.classList.add("active");
});

body.addEventListener("click" , e =>{
    let clickedElm = e.target;

    if(!clickedElm.classList.contains("sidebarOpen") && !clickedElm.classList.contains("menu") && !clickedElm.classList.contains("no-close")){
        nav.classList.remove("active");
    }
});

document.getElementById("dropdown").addEventListener("click", e => {
  e.stopPropagation(); // Evitar que el clic se propague al body
  document.getElementById("dropdown-menu").classList.toggle("active");
});

function info_item(producto_id) {
  window.location.href = `/productos/detalle-pan/${producto_id}/`;
};

document.addEventListener("DOMContentLoaded", function () {
  const agregarBotones = document.querySelectorAll(".agregar-item");

  agregarBotones.forEach((boton) => {
      boton.addEventListener("click", function () {
          const productoId = boton.dataset.itemId;
          const csrfToken = boton.dataset.csrfToken;

          // Realizar la solicitud AJAX
          const xhr = new XMLHttpRequest();
          const url = boton.dataset.itemUrl;
          xhr.open("POST", url);
          xhr.setRequestHeader("X-CSRFToken", csrfToken);
          xhr.onreadystatechange = function () {
              if (xhr.readyState === 4) {
                  if (xhr.status === 200) {
                      Swal.fire({
                          position: 'center',
                          icon: 'success',
                          title: 'Producto agregado',
                          showConfirmButton: false,
                          timer: 1500
                      });
                  } else {
                      Swal.fire({
                          position: 'center',
                          icon: 'error',
                          title: 'Error al agregar',
                          showConfirmButton: false,
                          timer: 1500
                      });
                  }
              }
          };
          const formData = new FormData();
          formData.append("cantidad", 1); // Cantidad fija de 1
          xhr.send(formData);
      });
  });
});

$(document).ready(function() {
    $('#search-form').on('submit', function(event) {
      event.preventDefault();
      var query = $('#search-input').val();
  
      $.ajax({
        url: '/buscar/',
        type: 'POST',
        data: { cuadro: query }, // Send the search query to the server
        dataType: 'json',
        success: function(response) {
          displayResults(response);
        },
        error: function(error) {
          console.log('Error:', error);
        }
      });
    });
  
    function displayResults(results) {
      var searchResults = $('#search-results');
      searchResults.empty();
  
      // Display products results
      if (results.products.length > 0) {
        var productHeading = $('<h2>Productos</h2>');
        searchResults.append(productHeading);
  
        var productResultList = $('<ul></ul>');
        results.products.forEach(function(result) {
          var listItem = $('<li></li>').text(result.name + ' - Precio: $' + result.price);
          productResultList.append(listItem);
        });
        searchResults.append(productResultList);
      }
  
      // Display categories results
      if (results.categories.length > 0) {
        var categoryHeading = $('<h2>Categorías</h2>');
        searchResults.append(categoryHeading);
  
        var categoryResultList = $('<ul></ul>');
        results.categories.forEach(function(result) {
          var listItem = $('<li></li>').text(result.name);
          categoryResultList.append(listItem);
        });
        searchResults.append(categoryResultList);
      }
  
      // If no results found
      if (results.products.length === 0 && results.categories.length === 0) {
        searchResults.append('<p>No results found.</p>');
      }
    }
  });