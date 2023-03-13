document.querySelector('#id_id_paciente').value = document.querySelector('#pacientes').value

$('#id_id_paciente').hide(); 
$('#id_id_fonoaudilogo').hide();
var miFormulario = document.getElementById("mi-formulario");
miFormulario.addEventListener("submit", function(event) {
  // Prevenir el envío del formulario
  event.preventDefault();
    alert("enviando")
  // Realizar acciones necesarias antes del envío del formulario
  // ...

    document.querySelector('#id_id_paciente').value = document.querySelector('#pacientes').value
  // Enviar el formulario manualmente
  miFormulario.submit();
});