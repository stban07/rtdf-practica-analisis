const selector=document.getElementById('audio-select')
const user=document.getElementById('user')
const audio_info=document.getElementById('audio_info')


function actualizar_audio(){
    console.log('cambio, buscando')
    console.log(selector.value);
    console.log(user.value)
    $.get('/admin-analisis/user_info',{
        user:user.value,id:selector.value,ajax:1},function(FormData){
            audio_info.innerHTML=FormData;
    })
}