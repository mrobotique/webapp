var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
var slider = document.getElementById("myTimeRange");
var time_label = document.getElementById("time_tag");
time_label.innerHTML = slider.value + " min."; // Display the default slider value

socket.on('my_response', function(message) {
    //console.log(arguments)
    //document.getElementById("p1").innerHTML ="iteration = " + message.data});
    //document.getElementById("p1").innerHTML = message.data

    });

window.onload = function() {
        socket.emit('connect');
};

function myButton(){
    socket.emit('myButton');
}

function startButton(){
    socket.emit('startButton',{'time':slider.value});
}

function stopButton(){
    socket.emit('stopButton');
}



function sendText(){
    socket.emit('myText', {'data':document.getElementById("myText").value})
    //console.log(document.getElementById("myText").value)
}

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  time_label.innerHTML = this.value  + " min.";
  //console.log(this.value);
}