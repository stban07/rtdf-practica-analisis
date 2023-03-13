

//TIMER AQUI ESTA LA LOGICA DEL CONTADOR

class Timer {
    constructor(callback, timeInterval, options) {
        this.timeInterval = timeInterval;

        // Add method to start timer
        this.start = () => {
            // Set the expected time. The moment in time we start the timer plus whatever the time interval is.
            this.expected = Date.now() + this.timeInterval;
            // Start the timeout and save the id in a property, so we can cancel it later
            this.theTimeout = null;

            if (options.immediate) {
                callback();
            }

            this.timeout = setTimeout(this.round, this.timeInterval);
            console.log('Timer Startedlll');
        };
        // Add method to stop timer
        this.stop = () => {

            clearTimeout(this.timeout);
            console.log('Timer Stoppedooo');
        };
        // Round method that takes care of running the callback and adjusting the time
        this.round = () => {
            console.log('timeout', this.timeout);
            // The drift will be the current moment in time for this round minus the expected time..
            let drift = Date.now() - this.expected;
            // Run error callback if drift is greater than time interval, and if the callback is provided
            if (drift > this.timeInterval) {
                // If error callback is provided
                if (options.errorCallback) {
                    options.errorCallback();
                }
            }
            callback();
            // Increment expected time by time interval for every round after running the callback function.
            this.expected += this.timeInterval;
            console.log('Drift:', drift);
            console.log('Next round time interval:', this.timeInterval - drift);
            // Run timeout again and set the timeInterval of the next iteration to the original time interval minus the drift.
            this.timeout = setTimeout(this.round, this.timeInterval - drift);
        };
    }
}
//-------------------------------------------------------------





//SONIDOS DEL METRONOMO
const audioCtx = new AudioContext();

const click1 = new Audio('/static/app/recursos/sonidos-metronomo/click1.mp3');
const click2 = new Audio('/static/app/recursos/sonidos-metronomo/click2.mp3');

const source1 = audioCtx.createMediaElementSource(click1);
const source2 = audioCtx.createMediaElementSource(click2);
source1.connect(audioCtx.destination);
source2.connect(audioCtx.destination);
//CONFIGURACIONES DEL METRONOMO
let bpm = 140;
let beatsPerMeasure = 4;
let count = 0;
let isRunning = false;
let tempoTextString = 'Medium';

//DECLARACION DE VARIBLE CON SU SELECTOR HTML
const tempoDisplay = document.querySelector('.tempo');
const tempoText = document.querySelector('.tempo-text');
const decreaseTempoBtn = document.querySelector('.decrease-tempo');
const increaseTempoBtn = document.querySelector('.increase-tempo');
const tempoSlider = document.querySelector('.slider');
const startStopBtn = document.querySelector('.start-stop');
const subtractBeats = document.querySelector('.subtract-beats');
const addBeats = document.querySelector('.add-beats');
const measureCount = document.querySelector('.measure-count');

//EVENTOS CLICK DE LAS VARIABLE DECLARADAS  HTML VOCALIZACION

decreaseTempoBtn.addEventListener('click', () => {
    if (bpm <= 20) { return };
    bpm--;
    validateTempo();
    updateMetronome();
});

increaseTempoBtn.addEventListener('click', () => {
    if (bpm >= 280) { return };
    bpm++;
    validateTempo();
    updateMetronome();
});

tempoSlider.addEventListener('input', () => {
    bpm = tempoSlider.value;
    validateTempo();
    updateMetronome();
});

subtractBeats.addEventListener('click', () => {
    if (beatsPerMeasure <= 2) { return };
    beatsPerMeasure--;
    measureCount.textContent = beatsPerMeasure;
    count = 0;
});

addBeats.addEventListener('click', () => {
    if (beatsPerMeasure >= 12) { return };
    beatsPerMeasure++;
    measureCount.textContent = beatsPerMeasure;
    count = 0;
});


// startStopBtn.addEventListener('click', () => {
//     count = 0;
//     if (!isRunning) {
//         metronome.start();
//         isRunning = true;
//         startStopBtn.textContent = 'STOP';
//     } else {
//         metronome.stop();
//         isRunning = false;
//         startStopBtn.textContent = 'START';
//     }
// });






//FUNCIONES DEL METRONOMO
function updateMetronome() {
    tempoDisplay.textContent = bpm;
    tempoSlider.value = bpm;
    metronome.timeInterval = 60000 / bpm;
    if (bpm <= 40) { tempoTextString = "Super Slow" };
    if (bpm > 40 && bpm < 80) { tempoTextString = "Slow" };
    if (bpm > 80 && bpm < 120) { tempoTextString = "Getting there" };
    if (bpm > 120 && bpm < 180) { tempoTextString = "Nice and Steady" };
    if (bpm > 180 && bpm < 220) { tempoTextString = "Rock n' Roll" };
    if (bpm > 220 && bpm < 240) { tempoTextString = "Funky Stuff" };
    if (bpm > 240 && bpm < 260) { tempoTextString = "Relax Dude" };
    if (bpm > 260 && bpm <= 280) { tempoTextString = "Eddie Van Halen" };

    tempoText.textContent = tempoTextString;
}
function validateTempo() {
    if (bpm <= 20) { return };
    if (bpm >= 280) { return };
    //document.getElementById('total_bpm').value = bpm
}

function playClick() {
    console.log(count);

    console.log("PLAY CLICK METRONOMO");
    if (count === beatsPerMeasure) {
        count = 0;
        console.log("3");
    }
    if (count === 0) {
        click1.play();
        click1.currentTime = 0;
        console.log("!");
    } else {
        click2.play();
        click2.currentTime = 0;
        console.log("2");
    }
    count++;
    //document.getElementById('total_beats').value = beatsPerMeasure
}

const metronome = new Timer(playClick, 60000 / bpm, { immediate: true });

