var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {
    document.getElementById("msg_id").innerHTML = message.msg_id;
    document.getElementById("date").innerHTML = message.date;
    document.getElementById("time").innerHTML = message.time;
    });

window.onload = function() {
        socket.emit('connect');
};


function sendText(){
    socket.emit('myText', {'data':document.getElementById("myText").value})
    //console.log(document.getElementById("myText").value)
}