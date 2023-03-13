
//INICIO DE FUNCION PARA GRABAR AUDIO CON JS
const init = () => {
    //PREGUNTA SI SOPORTA MICROFONO CON MEDIADEVICES
    const tieneSoporteUserMedia = () =>
        !!(navigator.mediaDevices.getUserMedia)

    // Si no soporta...
    // Amable aviso para que el mundo comience a usar navegadores decentes ;)
    if (typeof MediaRecorder === "undefined" || !tieneSoporteUserMedia())
        return alert("Tu navegador web no cumple los requisitos; por favor, actualiza tu navegador o utiliza Firefox o Google Chrome");


    // Declaración de elementos del DOM
    const $listaDeDispositivos = document.querySelector("#listaDeDispositivos"),
        $duracion = document.querySelector("#duracion"),
        $btnComenzarGrabacion = document.querySelector("#start_stop"),



        
    // Algunas funciones útiles
     limpiarSelect = () => {
        for (let x = $listaDeDispositivos.options.length - 1; x >= 0; x--) {
            $listaDeDispositivos.options.remove(x);
        }
    }

    const segundosATiempo = numeroDeSegundos => {
        let horas = Math.floor(numeroDeSegundos / 60 / 60);
        numeroDeSegundos -= horas * 60 * 60;
        let minutos = Math.floor(numeroDeSegundos / 60);
        numeroDeSegundos -= minutos * 60;
        numeroDeSegundos = parseInt(numeroDeSegundos);
        if (horas < 10) horas = "0" + horas;
        if (minutos < 10) minutos = "0" + minutos;
        if (numeroDeSegundos < 10) numeroDeSegundos = "0" + numeroDeSegundos;
        return `${horas}:${minutos}:${numeroDeSegundos}`;
    };

    // Variables "globales"
    let tiempoInicio, mediaRecorder, idIntervalo;
    const refrescar = () => {
        $duracion.textContent = segundosATiempo((Date.now() - tiempoInicio) / 1000);
    }


    // Consulta la lista de dispositivos de entrada de audio y llena el select
    const llenarLista = () => {
        navigator
            .mediaDevices
            .enumerateDevices()
            .then(dispositivos => {
                limpiarSelect();
                dispositivos.forEach((dispositivo, indice) => {
                    if (dispositivo.kind === "audioinput") {
                        const $opcion = document.createElement("option");
                        // Firefox no trae nada con label, que viva la privacidad
                        // y que muera la compatibilidad
                        $opcion.text = dispositivo.label || `Dispositivo ${indice + 1}`;
                        $opcion.value = dispositivo.deviceId;
                        $listaDeDispositivos.appendChild($opcion);
                    }
                })
            })
    };

    // Ayudante para la duración; no ayuda en nada pero muestra algo informativo
    const comenzarAContar = () => {
        tiempoInicio = Date.now();
        idIntervalo = setInterval(refrescar, 500);
        
    };

    // Comienza a grabar el audio con el dispositivo seleccionado
    const comenzarAGrabar = (op) => {
        if (!$listaDeDispositivos.options.length) return alert("No hay dispositivos");
        if (mediaRecorder) return alert("Excelente, completaste tu Ejercitación. Recuerda que debes ejercitar almenos 3 veces al día"); // No permitir que se grabe doblemente

        navigator.mediaDevices.getUserMedia({
            audio: {
                deviceId: $listaDeDispositivos.value,
            }
        })
            .then(
                stream => { 
                    a = document.querySelector("#segundos").textContent; 
                    mediaRecorder = new MediaRecorder(stream);                      // Comenzar a grabar con el stream
                    mediaRecorder.start();
                    ///////////
                    if(op === true){
                        comenzarAContar();
                    }else{
                        comenzarAContar();
                        metronome.start();
                        timerId = setTimeout(() => {
                            stop();
                        },  a  * 1100);
                    }
                    
                    const fragmentosDeAudio = [];                                   // En el arreglo pondremos los datos que traiga el evento dataavailable
                    mediaRecorder.addEventListener("dataavailable", evento => {     // Escuchar cuando haya datos disponibles
                        fragmentosDeAudio.push(evento.data);
                    });



                    // Cuando se detenga (haciendo click en el botón) se ejecuta esto
                    mediaRecorder.addEventListener("stop", () => {


                    let nombre = ""
                    if(op === true){
                        detenerConteo();
                        nombre = "intensidad"
                    }else{
                        detenerConteo();
                        metronome.stop();
                        nombre = "vocalizacion"
                    }

                    // Enviar audio
                    enviarAudio(fragmentosDeAudio,nombre);
                    });


                }
            )
            .catch(error => {
                console.log(error) // Aquí maneja el error, tal vez no dieron permiso
            });
    };


    const detenerConteo = () => {
        clearInterval(idIntervalo);
        tiempoInicio = null;
        $duracion.textContent = "La grabacion comenzara una vez precione el boton";
    }

     const stop = () => {
        if (!mediaRecorder) return
            detenerConteo();
            mediaRecorder.stop();
            mediaRecorder = null;
        $btnComenzarGrabacion.textContent = "COMENZAR";
     }


     const enviarAudio = (fragmentosDeAudio,name) => {

        var blob = new Blob(fragmentosDeAudio);

        // Crea un nuevo objeto FormData
        const formData = new FormData();


        var filer = new File([blob], "miaudio.mp3", { type: "audio/mp3" });
        formData.append('file', filer);
        formData.append('string', name);

        // Hace una solicitud POST al servidor Django usando el método fetch
         fetch('/save_audio/', {
         method: 'POST',
         body: formData});
     }



//METODO PARA GET DESDE JAVASCRIPT
    // async function getData() {
    //     const response = await fetch('/save_audio/', {method: 'GET'})
    //     const data = await response.json();
    //     console.log(data["segundos"]);
    //     segundo = data["segundos"]
    //     promesa(segundo);
    //     return data;
    //   }

    // promesa = () => {
    //      a = document.querySelector("#segundos").textContent;
    //      retr
    // }



    clickAudio = (a) => {
        console.log($btnComenzarGrabacion.textContent)
        let val = $btnComenzarGrabacion.textContent
        if(val === "PARAR"){
            stop();
            $btnComenzarGrabacion.textContent = "COMENZAR"
        }else if(val = "COMENZAR"){
            comenzarAGrabar(a);
            $btnComenzarGrabacion.textContent = "PARAR"
        }
     }

    

    // Cuando ya hemos configurado lo necesario allá arriba llenamos la lista

    llenarLista();
}





// Esperar a que el documento esté listo...
document.addEventListener("DOMContentLoaded", init);