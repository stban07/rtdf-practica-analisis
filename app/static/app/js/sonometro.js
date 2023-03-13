//microfono
class Microphone {
    constructor() {
        this.initialized = false;
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function (stream) {
                this.audioContext = new AudioContext();
                this.microphone = this.audioContext.createMediaStreamSource(stream);
                this.analyser = this.audioContext.createAnalyser();
                this.analyser.fftSize = 512;
                const bufferLength = this.analyser.frequencyBinCount;
                this.dataArray = new Uint8Array(bufferLength);
                this.microphone.connect(this.analyser);
                this.initialized = true;
            }.bind(this)).catch(function (err) {
                alert(err);
            });

    }
    getSample() {
        this.analyser.getByteTimeDomainData(this.dataArray);
        let normSamples = [...this.dataArray].map(e => e / 128 - 1);
        return normSamples;

    }
    getVolume() {
        this.analyser.getByteTimeDomainData(this.dataArray);
        let normSamples = [...this.dataArray].map(e => e / 128 - 1);
        let sum = 0;
        for (let i = 0; i < normSamples.length; i++) {
            sum += normSamples[i] * normSamples[i];
        }
        let volume = Math.sqrt(sum / normSamples.length);
        return volume;

    }
}

//visualizer
function main() {
    const canvas  = document.getElementById('myCanvas');
    const ctx     = canvas.getContext('2d');
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

    class Bar {
        constructor(x, y, width, height, color){
            this.x      = x;
            this.y      = y;
            this.width  = width;
            this.height = height;
            this.color  = color;
        }
        update(micInput){
            this.height = micInput * 1000;
        }
        
        draw(context) {
            context.fillStyle = this.color;
            context.fillRect(this.x, this.y, this.width, this.height);
        }
    }

    
    const microphone = new Microphone();
    let bars=[];
    let barWidth = canvas.width/256;
    function createBars(){
        for (i = 0; i < 256; i++){
            let color = 'hsl(' + i * 2 + ', 100%, 50%)';
            bars.push(new Bar(i * barWidth , canvas.height/2 , 1.9, 20, color))
        }
     
    }
    createBars();
    function animate() {
        if(microphone.initialized){
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const samples = microphone.getSample();
            bars.forEach(function (bar, i) {
                bar.update(samples[i]);
                bar.draw(ctx);
            });
        }
        requestAnimationFrame(animate);
    }
    animate();
}