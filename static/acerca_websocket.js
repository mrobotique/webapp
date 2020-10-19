var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('info_fabricacion', function(message) {
    document.getElementById("modelo").innerHTML = message.modelo;
    document.getElementById("serialNumber").innerHTML = message.serialNumber;
});

function zeroPad(n, width, z) {
    //Agrega ceros antes del numero.
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function toTimeString(totalSeconds){
    //convierte segundos a str 00h 00m 00s
    hours = Math.floor(totalSeconds / 3600);
    totalSeconds %= 3600;
    minutes = Math.floor(totalSeconds / 60);
    seconds = totalSeconds % 60;
    return zeroPad(hours,2) + "h  " + zeroPad(minutes,2) + "m  " + zeroPad(seconds,2) + "s";
};

socket.on('my_response', function(message) {
    document.getElementById("version").innerHTML = message.version;
    document.getElementById("card").innerHTML = message.card;
    var horometro = message.horometro;
    if (horometro<=8000){
        document.getElementById("horometro").innerHTML = toTimeString(horometro);
        }

    if ((horometro>8000) && (horometro<=8500)){
        document.getElementById("horometro").innerHTML = "<span style='color:orange;'>" +  toTimeString(horometro) + "</span>";
    }

    if ((horometro>8500) && (horometro<=9000)){
        document.getElementById("horometro").innerHTML = "<span style='color:red;'>" +  toTimeString(horometro) + "</span>";
    }
    if (horometro>9000){
        document.getElementById("horometro").innerHTML = "<span style='color:red;'> LLAME A SERVICIO </span>";
        }

    });
window.onload = function() {
        socket.emit('connect');
};

function myButton(){
    socket.emit('myButton')
}

function sendText(){
    socket.emit('myText', {'data':document.getElementById("myText").value})
    //console.log(document.getElementById("myText").value)
}

window.onload = function() {
        socket.emit('acerca_info');
};