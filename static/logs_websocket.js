var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {

    });
window.onload = function() {
        socket.emit('connect');
};

function deleteButton(){
  var txt;
  if (confirm("Esta accion borrara la base de datos de manera definitiva!")) {
    txt = "You pressed OK!";
    socket.emit('delete_file')
  } else {
    txt = "You pressed Cancel!";
  }
  document.getElementById("prueba").innerHTML = txt;
}

function sendText(){
    socket.emit('myText', {'data':document.getElementById("myText").value})
    //console.log(document.getElementById("myText").value)
}