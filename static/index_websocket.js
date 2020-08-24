var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
var slider = document.getElementById("myTimeRange");
var time_label = document.getElementById("time_tag");
time_label.innerHTML = slider.value + " min."; // Display the default slider value

socket.on('my_response', function(message) {
    //console.log(arguments)
    //document.getElementById("p1").innerHTML ="iteration = " + message.data});
    //document.getElementById("p1").innerHTML = message.data
    document.getElementById("date").innerHTML = message.date;
    document.getElementById("time").innerHTML = message.time;
    if (message.operationMode == 3){
        document.getElementById("operationMode").innerHTML = "<i class='fas fa-hourglass-end' style='font-size:160%; color:grey'>";
    }
    else{
        document.getElementById("operationMode").innerHTML = "<i class='fas fa-hourglass' style='font-size:160%; color:purple'>";
    }

    var tiempo  = message.tiempoRestante  //document.getElementById("tiempoRestante").innerHTML
    var hr = Math.floor(tiempo/3600);
    var min = Math.floor((tiempo - (hr*3600))/60);
    var sec = tiempo - (min * 60);
    document.getElementById("tiempoRestante").innerHTML = ('0'  + hr).slice(-2)+':'+('0'  + min).slice(-2)+':'+('0' + sec).slice(-2);
    });

function startButton(){
    socket.emit('startButton',{'time':slider.value * 60});
}

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  time_label.innerHTML = this.value  + " min.";
  //console.log(this.value);
}

window.onload = function() {
        socket.emit('connect');
};
