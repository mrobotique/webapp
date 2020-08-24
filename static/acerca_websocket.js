var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('info_fabricacion', function(message) {
    document.getElementById("modelo").innerHTML = message.modelo;
    document.getElementById("serialNumber").innerHTML = message.serialNumber;
});

socket.on('my_response', function(message) {
    document.getElementById("version").innerHTML = message.version;
    document.getElementById("card").innerHTML = message.card;
    var horometro = message.horometro;
    if (horometro<=8000){
        document.getElementById("horometro").innerHTML = horometro + " H.";
        }

    if ((horometro>8000) && (horometro<=8500)){
        document.getElementById("horometro").innerHTML = "<span style='color:orange;'>" +  horometro + " H.</span>";
    }

    if ((horometro>8500) && (horometro<=9000)){
        document.getElementById("horometro").innerHTML = "<span style='color:red;'>" +  horometro + " H.</span>";
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