// Seleciiono del DOMs la clase display y controllers
const display = document.querySelector('.display')
const controllerWrapper = document.querySelector('.controllers')


const State = ['Initial', 'Record', 'Download', 'Guardar']
let stateIndex = 0

//variables del audio
let mediaRecorder, chunks = [], audioURL = ''

// mediaRecorder setup for audio
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    console.log('mediaDevices supported..')

    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(stream => {
        mediaRecorder = new MediaRecorder(stream)

        mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data)
        }

        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, {'type': 'audio/ogg; codecs=opus'})
            chunks = []
            audioURL = window.URL.createObjectURL(blob)
            document.querySelector('audio').src = audioURL

        }
    }).catch(error => {
        console.log('Following error has occured : ',error)
    })
}else{
    stateIndex = ''
    application(stateIndex)
}

const clearDisplay = () => {
    // DEfino que le contenido de el div display como  vacio
    display.textContent = ''
}

const clearControls = () => {
    // Defino que el contenido de el div controller  como vacio
    controllerWrapper.textContent = ''
}


// Al iniciar la funcion record()  el stateindex sera  = 1 y comenzara a ejecutarse
// el primer caso del switch
// se define que comienze la grabacion
const record = () => {
    stateIndex = 1
    mediaRecorder.start()
    application(stateIndex)
}


// Al iniciar la funcion stopRecording()  el stateindex sera  = 2 y comenzara a ejecutarse
// el segundo caso del switch
// se define que se detenga la grabacion
const stopRecording = () => {
    stateIndex = 2
    mediaRecorder.stop()
    application(stateIndex)
}

// Al iniciar la funcion downloadAudio() 
//Se crearea el elemento en el Dom 'a'
// downloadLink.href = audioURL define el link de descarga
const downloadAudio = () => {
    const downloadLink = document.createElement('a')
    downloadLink.href = audioURL
    downloadLink.setAttribute('download', 'audio')
    downloadLink.click()
}

const addButton = (id, funString, text) => {
    const btn = document.createElement('button')
    btn.id = id
    btn.setAttribute('onclick', funString)
    btn.textContent = text
    controllerWrapper.append(btn)
}

const addMessage = (text) => {
    const msg = document.createElement('p')
    msg.textContent = text
    display.append(msg)
}

const addAudio = () => {
    const audio = document.createElement('audio')
    audio.controls = true

    //Ubicacion del audio   
    audio.src = audioURL
  

    console.log( audio.src);
    display.append(audio)
}

const saveAudio = () => {
    console.log("Hola mundo");
}



const application = (index) => {
    switch (State[index]) {
        case 'Initial':
            clearDisplay()
            clearControls()

            addButton('record', 'record()', 'Comenzar grabacion')
            break;

        case 'Record':
            clearDisplay()
            clearControls()

            addMessage('Escuchando')
            addButton('stop', 'stopRecording()', 'Detener Grabacion')
            break

        case 'Download':
            clearControls()
            clearDisplay()

            addAudio()
            addButton('record', 'record()', 'Grabar otra vez')
            break
        
        default:
            clearControls()
            clearDisplay()

            addMessage('Your browser does not support mediaDevices')
            break;
    }
 
}
 
function guardar() {
    console.log("Hola");
    console.log("La ubicacion del audio es: " + audioURL);
    const pruebaUrl = document.querySelector('.pruebaUrl')
    pruebaUrl.innerHTML= "<h1>"+audioURL+"</h1>"
}


application(stateIndex)


