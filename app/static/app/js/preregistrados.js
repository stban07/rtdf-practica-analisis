
clickpreregistrados = (a) => {
let ver = document.getElementById(a)
let elementos = ver.getElementsByTagName("td")
console.log(elementos)
document.getElementById("id_rut").value = elementos[0].innerHTML
document.getElementById("id_first_name").value = elementos[1].innerHTML
document.getElementById("id_first_name").readOnly = true
document.getElementById("id_last_name").value = elementos[2].innerHTML
document.getElementById("id_last_name").readOnly = true
document.getElementById("id_email").value = elementos[4].innerHTML
document.getElementById("id_email").readOnly = true

console.log(elementos[3].innerHTML)
esname = elementos[3].innerHTML




if( esname == "FonoAudiologo"){
    console.log("sssss")
    document.getElementById("id_id_tipo_user").value = 1
}else{
    console.log("ddddd")
    document.getElementById("id_id_tipo_user").value = 2
}



}
