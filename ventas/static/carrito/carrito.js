//aumentar, disminuir y elimanr items con ajax
const csrftoken = getCookie('csrftoken');

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  $(document).ready(function() {
    function actualizarTotal(total) {
      const parsedTotal = parseFloat(total); // Convert total to a number
      if (!isNaN(parsedTotal)) {
        const totalElement = document.querySelector('.total');
        totalElement.textContent = `Total: $${parsedTotal.toFixed(2)}`;
      } else {
        console.error("Invalid total value:", total);
      }
    }

    function removeItemFromPage(productoId) {
      const itemElement = $(`#item-${productoId}`);
      itemElement.remove();
    }
  
    function actualizarCarritoVacio() {
      const carritoItems = $(".item");
      if (carritoItems.length === 0) {
        window.location.reload();
      }
    }

    $('.eliminar-item').click(function(e) {
      e.preventDefault();
      const borrarURL = $(this).data("eliminar-url");
      eliminarItem(borrarURL);
    });

    $('.restar-item').click(function(e) {
      e.preventDefault();
      const restarURL = $(this).data("restar-url");
      restarItem(restarURL);
    });

    $('.aumentar-item').click(function(e) {
      e.preventDefault();
      const sumarURL = $(this).data("sumar-url");
      aumentarItem(sumarURL);
    });

    function updateQuantityOnPage(productoId, newQuantity) {
      const quantityElement = $(`#cantidad-${productoId}`);
      quantityElement.text(newQuantity);
    }


    function eliminarItem(url) {
      $.ajax({
        type: 'POST',
        url: url,
        data: {},
        headers: {
          'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function(data) {
          console.log(data.message);
          updateQuantityOnPage(data.producto_id, data.new_quantity);
          if (data.eliminar) {
            removeItemFromPage(data.producto_id);
          } else {
            const newQuantity = parseInt(data.new_quantity);
            if (newQuantity === 0) {
              removeItemFromPage(data.producto_id);
            }
          }
          actualizarCarritoVacio();
          if (typeof data.total_carrito === 'number') {
            const totalValue = data.total_carrito;
            actualizarTotal(totalValue);
          } else if (typeof data.total_carrito === 'object' && 'total_carrito' in data.total_carrito) {
            const totalValue = data.total_carrito.total_carrito;
            if (typeof totalValue === 'number') {
              actualizarTotal(totalValue);
            } else {
              console.error("Invalid total value:", data.total_carrito);
            }
          } else {
            console.error("Invalid total value:", data.total_carrito);
          }
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error(xhr.responseText);
        }
      });
    }

    function aumentarItem(url) {
      $.ajax({
        type: 'POST',
        url: url,
        data: {},
        headers: {
          'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function(data) {
          console.log(data.message);
          updateQuantityOnPage(data.producto_id, data.new_quantity);
          if (typeof data.total_carrito === 'number') {
            const totalValue = data.total_carrito;
            actualizarTotal(totalValue);
          } else if (typeof data.total_carrito === 'object' && 'total_carrito' in data.total_carrito) {
            const totalValue = data.total_carrito.total_carrito;
            if (typeof totalValue === 'number') {
              actualizarTotal(totalValue);
            } else {
              console.error("Invalid total value:", data.total_carrito);
            }
          } else {
            console.error("Invalid total value:", data.total_carrito);
          }
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error(xhr.responseText);
        }
      });
    }

    function restarItem(url) {
      $.ajax({
        type: 'POST',
        url: url,
        data: {},
        headers: {
          'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function(data) {
          console.log(data.message);
          updateQuantityOnPage(data.producto_id, data.new_quantity);
          if (data.new_quantity === 0) {
            removeItemFromPage(data.producto_id);
          }
          actualizarCarritoVacio();
          if (typeof data.total_carrito === 'number') {
            const totalValue = data.total_carrito;
            actualizarTotal(totalValue);
          } else if (typeof data.total_carrito === 'object' && 'total_carrito' in data.total_carrito) {
            const totalValue = data.total_carrito.total_carrito;
            if (typeof totalValue === 'number') {
              actualizarTotal(totalValue);
            } else {
              console.error("Invalid total value:", data.total_carrito);
            }
          } else {
            console.error("Invalid total value:", data.total_carrito);
          }
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error(xhr.responseText);
        }
      });
    }
  });


//boton comprar

function verCuestionario() {
  const compra = document.getElementById('compra-cuestionario');
  compra.style.display = 'flex';

  // Agregar evento de clic fuera del formulario para cerrar la ventana emergente
  window.addEventListener('click', cerrarCuestionario);
}

function cerrarCuestionario(event) {
  const compra = document.getElementById('compra-cuestionario');
  const compraContainer = document.querySelector('.compra-container');

  // Comprobar si se hizo clic fuera del formulario
  if (event.target === compra) {
    compra.style.display = 'none';
    // Eliminar el evento de clic fuera del formulario
    window.removeEventListener('click', cerrarCuestionario);
  }
}




//boton encargar
function verificarencargo(button) {
  const encargarURL = $(button).data("encargo-url");
  $.ajax({ 
    url: encargarURL,
    method: "GET",
    success: function(response) {
      if (response.califica) {
        mostrarCuestionario();
      } else {
        // Si no califica, redirigir a otra página
        if (response.redirect) {
          window.location.href = response.redirect;
        } else {
          // Si no hay URL de redirección, mostrar el mensaje de error
          Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'No califica para encargo',
            text: 'Debe haber al menos 20 piezas.',
            showConfirmButton: false,
            timer: 2500
          });
        }
      }
    },
    error: function(xhr, status, error) {
      // Manejo de errores si es necesario
      console.error(error);
    }
  });
}

const currentDate = new Date();
currentDate.setDate(currentDate.getDate() + 3);
const year = currentDate.getFullYear();
const month = String(currentDate.getMonth() + 1).padStart(2, '0');
const day = String(currentDate.getDate()).padStart(2, '0');
const formattedDate = `${year}-${month}-${day}`;
document.getElementById('fecha-entrega').setAttribute('min', formattedDate);

function mostrarCuestionario() {
  const modal = document.getElementById('modal-cuestionario');
  modal.style.display = 'flex';

  // Agregar evento de clic fuera del formulario para cerrar la ventana emergente
  window.addEventListener('click', cerrarCuestionarioExterno);
}

function cerrarCuestionarioExterno(event) {
  const modal = document.getElementById('modal-cuestionario');
  const modalContainer = document.querySelector('.modal-container');

  // Comprobar si se hizo clic fuera del formulario
  if (event.target === modal) {
    modal.style.display = 'none';
    // Eliminar el evento de clic fuera del formulario
    window.removeEventListener('click', cerrarCuestionarioExterno);
  }
}


