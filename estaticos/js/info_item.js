function info_item(producto_id) {
  window.location.href = `/productos/detalle-pan/${producto_id}/`;
};

$(document).ready(function () {
  $("#agregar-item").submit(function (event) {
    event.preventDefault();
    var itemURL = $(this).data("item-url");
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: itemURL, 
      data: formData,
      dataType: "json",
      success: function (response) {
        Swal.fire({
          position: 'center',
          icon: 'success',
          title: 'Producto agregado',
          showConfirmButton: false,
          timer: 1000
        })
      },
      error: function (xhr, status, error) {
        Swal.fire({
          position: 'center',
          icon: 'error',
          title: 'Error al agregar',
          showConfirmButton: false,
          timer: 1000
        })
      },
    });
  });
});

$(document).ready(function () {
  $("#form-opinion").submit(function (event) {
    event.preventDefault();
    var opinionURL = $(this).data("opinion-url");
    var formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: opinionURL, 
      data: formData,
      dataType: "json",
      success: function (response) {
        Swal.fire({
          position: 'center',
          icon: 'success',
          title: 'Opinión enviada',
          showConfirmButton: false,
          timer: 1000
        })
        $("#mensaje").val("");
      },
      error: function (xhr, status, error) {
        Swal.fire({
          position: 'center',
          icon: 'error',
          title: 'Error al enviar opinión',
          showConfirmButton: false,
          timer: 1000
        })
      },
    });
  });
});