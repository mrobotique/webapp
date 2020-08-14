var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {
    //console.log(arguments)
    //document.getElementById("p1").innerHTML ="iteration = " + message.data});
    document.getElementById("p1").innerHTML = message.data});

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