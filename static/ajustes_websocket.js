var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {
    document.getElementById("msg_id").innerHTML = message.msg_id;
    document.getElementById("date").innerHTML = message.date;
    document.getElementById("time").innerHTML = message.time;
    });

window.onload = function() {
        socket.emit('connect');
        socket.emit('request_toggle_status');
};


function sendText(){
    socket.emit('myText', {'data':document.getElementById("myText").value})
    //console.log(document.getElementById("myText").value)
};

// Submit form with class function.
function submit_TimeData() {
            var fecha = document.getElementById("fecha").value;
            var hora = document.getElementById("hora").value;
            if ((fecha === "") || (hora === "")) {
                alert("Hora y Fecha tienen que ser completados");
            }
            else{
                var password = prompt("Introduzca la contraseña",' ');
                if (password=="12345678"){
                    socket.emit("set_dateTime", {'hora':hora, 'fecha':fecha});
                }
                else {
                alert("Password invalido");
                }
            }
};

function submit_Conf() {
    /*  Para setear el valor de los checkboxes
     *  document.getElementById("toggle_lampara4").checked = true;
    */
    var buzzer = document.getElementById("toggle_buzzer").checked;
    var lampara1 = document.getElementById("toggle_lampara1").checked;
    var lampara2 = document.getElementById("toggle_lampara2").checked;
    var lampara3 = document.getElementById("toggle_lampara3").checked;
    var lampara4 = document.getElementById("toggle_lampara4").checked;
    var lampara5 = document.getElementById("toggle_lampara5").checked;
    var lampara6 = document.getElementById("toggle_lampara6").checked;
    socket.emit("set_hardwareConfig",{"buzzer":buzzer, "lampara1":lampara1, "lampara2":lampara2, "lampara3":lampara3,
                "lampara4":lampara4, "lampara5":lampara5, "lampara6":lampara6});
};

socket.on('set_toggle_status', function(msg){
    document.getElementById("toggle_buzzer").checked = msg; //msg es int pero si funciona 1/0 como true/false
});

socket.on('setDateResponse', function(msg){
    alert("Nueva fecha y hora:  " + msg);
});