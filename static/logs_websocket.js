var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {

    });
window.onload = function() {
        socket.emit('connect');
};

socket.on('reload_log', function(){
    location.reload();
});

function deleteButton(){
  var txt;
  if (confirm("Esta accion borrara la base de datos de manera definitiva!")) {
    socket.emit('delete_file')
  }
}

function deleteSelected(){
  var txt;
  var total_rows = document.getElementsByName("tabla_bitacora")[0].rows.length;
  var data_rows = total_rows - 2; //menos el titulo y el heading

  if (confirm("Esta accion borrara los elementos seleccionados de manera definitiva!")) {
    var i;
    var result = []
    for (i = data_rows; i >=1 ; i--) //Invertido por que la lista de python viene invertida para tener la entrada mas nueva hasta  arriba
    {
       if (document.getElementById("check_" + i.toString()).checked )
       {
        result.push(1);
       }
       else
       {
        result.push(0)
       }
    }
    console.log(result);
    socket.emit('delete_entries', result)
  }
}

function sendText(){
    socket.emit('myText', {'data':document.getElementById("myText").value})
    //console.log(document.getElementById("myText").value)
}