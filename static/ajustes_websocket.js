var commCounter = 0;
var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {
    if(commCounter === 6) commCounter = 0;
    if(commCounter===0) document.getElementById("msg_id").innerHTML = "<i class='fas fa-network-wired' style='font-size:160%; color:purple'>";
    if(commCounter===2) document.getElementById("msg_id").innerHTML = "<i class='fas fa-network-wired' style='font-size:160%; color:gray'>";
    if(commCounter===3) document.getElementById("msg_id").innerHTML = "<i class='fas fa-network-wired' style='font-size:160%; color:#100935'>";
    if(commCounter===5) document.getElementById("msg_id").innerHTML = "<i class='fas fa-network-wired' style='font-size:160%; color:gray'>";
    commCounter += 1;
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
    var hardware_byte = buzzer + 2 * lampara1 + 4 * lampara2 + 8 * lampara3 + 16 * lampara4 + 32 * lampara5 + 64 * lampara6
    var flag_time = 0;
    var flag_hardware = 1;
    socket.emit('startButton',{'time':[flag_time,0], 'mask':[flag_hardware, hardware_byte]});
};

socket.on('set_toggle_status', function(msg){
    //console.log(msg);
    document.getElementById("toggle_buzzer").checked = msg.buzzer; //msg es int pero si funciona 1/0 como true/false
    document.getElementById("toggle_lampara1").checked = msg.lamp_1; //msg es int pero si funciona 1/0 como true/false
    document.getElementById("toggle_lampara2").checked = msg.lamp_2; //msg es int pero si funciona 1/0 como true/false
    document.getElementById("toggle_lampara3").checked = msg.lamp_3; //msg es int pero si funciona 1/0 como true/false
    document.getElementById("toggle_lampara4").checked = msg.lamp_4; //msg es int pero si funciona 1/0 como true/false
    document.getElementById("toggle_lampara5").checked = msg.lamp_5; //msg es int pero si funciona 1/0 como true/false
    document.getElementById("toggle_lampara6").checked = msg.lamp_6; //msg es int pero si funciona 1/0 como true/false

});

socket.on('setDateResponse', function(msg){
    alert("Nueva fecha y hora:  " + msg);
});