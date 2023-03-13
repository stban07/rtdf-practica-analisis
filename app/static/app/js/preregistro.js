


clickRut = () => {

    
    let input1 = document.querySelector("#rut-input").value;

    if (!input1) {
        alert("Por favor, rellene todos los campos");
        return;
    }else{

    $.ajax({
       url: "/buscar_rut/",
       type: "POST",
       data:  { rut: input1 },
       success: function(response) {
        if (response.Nombre){
          alert("Hola Eres Fonoaudilogo") 
          $('#rutvalidate').hide();
          $('#id_tipo_user').hide();
          $('#formulario').show();
          let tipo_user = document.querySelector("#id_tipo_user");
          
          let rut = document.querySelector("#id_rut");
          let nombre = document.querySelector("#id_nombre");
          let apellido = document.querySelector("#id_apellido")
          

          
          let FullName = response.Nombre
          FullName = FullName.split(" ")
          rut.value = response.rut
          rut.readOnly = true
          nombre.value = FullName[0]
          nombre.readOnly = true
          apellido.value = FullName[2]
          apellido.readOnly = true
          tipo_user.value = "FonoAudiologo"
        }else if (response.NO){
          alert("RUT ya fue registrado/Preregistrado")  
            
        }else if (response.SI){
          alert("No tenemos Informacion del Rut, Complete el formulario de PreRegistro") 
          $('#rutvalidate').hide();
          $('#id_tipo_user').hide(); 
          $('#formulario').show();
          let input1 = document.querySelector("#rut-input").value;
          let rut = document.querySelector("#id_rut");
          rut.value = input1
          rut.readOnly = true
          document.querySelector("#id_tipo_user").value = "Desconocido";
        }else if (response.STOP){
          alert("RUT ya fue registrado/Preregistrado")  
        }



       }
     });

}
}



miFormulario.addEventListener("submit", function(event) {

//   if (rut.getAttribute("readonly")) {
//     rut.removeAttribute("readonly");
//   } else {
//     rut.setAttribute("readonly", "readonly");
// }



});











//agrega . y - a el Rut
 const rutInput = document.querySelector("#rut-input");

  rutInput.addEventListener("input", function() {
    let rut = this.value;
    rut = rut.replace(/[^0-9kK]+/g, "");

    if (rut.length > 1) {
      rut = rut.slice(0, rut.length - 1) + "-" + rut.slice(rut.length - 1);
    }

    if (rut.length > 4) {
      rut = rut.slice(0, -5) + "." + rut.slice(-5);
    }

    if (rut.length > 8) {
      rut = rut.slice(0, -9) + "." + rut.slice(-9);
    }

    this.value = rut;
  });


