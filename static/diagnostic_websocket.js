var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
socket.on('my_response', function(message) {
    //console.log(arguments)
    //document.getElementById("p1").innerHTML ="iteration = " + message.data});
    document.getElementById("msg_id").innerHTML = message.msg_id;
    document.getElementById("operationMode").innerHTML = message.operationMode;
    document.getElementById("date").innerHTML = message.date;
    document.getElementById("time").innerHTML = message.time;
    document.getElementById("version").innerHTML = message.version;
    document.getElementById("card").innerHTML = message.card;
    /*AUTO*/
    if(message.auto == 0){
        document.getElementById("auto").innerHTML = "<i class=\"fas fa-power-off\" style='font-size:24px;color:green'>";
    }
    else{
        document.getElementById("auto").innerHTML = "<i class=\"fas fa-power-off\" style='font-size:24px;color:gray'>";
    }
    /*DEADMAN1*/
    if(message.deadman1 == 0){
        document.getElementById("deadman1").innerHTML = "<i class=\"fas fa-power-off\" style='font-size:24px;color:green'>";
    }
    else{
        document.getElementById("deadman1").innerHTML = "<i class=\"fas fa-power-off\" style='font-size:24px;color:gray'>";
    }
    /*DEADMAN2*/
    if(message.deadman2 == 0){
        document.getElementById("deadman2").innerHTML = "<i class=\"fas fa-power-off\" style='font-size:24px;color:green'>";
    }
    else{
        document.getElementById("deadman2").innerHTML = "<i class=\"fas fa-power-off\" style='font-size:24px;color:gray'>";
    }
    /*PIR1*/
    if(message.pir1 == 1){
        document.getElementById("pir1").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:red'>";
    }
    else{
        document.getElementById("pir1").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:gray'>";
    }
    /*PIR2*/
    if(message.pir2 == 1){
        document.getElementById("pir2").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:red'>";
    }
    else{
        document.getElementById("pir2").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:gray'>";
    }
    /*PIR3*/
    if(message.pir3 == 1){
        document.getElementById("pir3").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:red'>";
    }
    else{
        document.getElementById("pir3").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:gray'>";
    }
    /*PIR4*/
    if(message.pir4 == 1){
        document.getElementById("pir4").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:red'>";
    }
    else{
        document.getElementById("pir4").innerHTML = "<i class=\"fas fa-user\" style='font-size:24px;color:gray'>";
    }
    /*MAG1*/
    if(message.mag1 == 0){
        document.getElementById("mag1").innerHTML = "<i class=\"fas fa-magnet\" style='font-size:24px;color:red'>";
    }
    else{
        document.getElementById("mag1").innerHTML = "<i class=\"fas fa-magnet\" style='font-size:24px;color:gray'>";
    }
    /*MAG2*/
    if(message.mag2 == 0){
        document.getElementById("mag2").innerHTML = "<i class=\"fas fa-magnet\" style='font-size:24px;color:red'>";
    }
    else{
        document.getElementById("mag2").innerHTML = "<i class=\"fas fa-magnet\" style='font-size:24px;color:gray'>";
    }

    /*LAMP1*/
    if(message.lamp1 == 0){
        document.getElementById("lamp1").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lamp1").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }

    /*LAMP2*/
    if(message.lamp2 == 0){
        document.getElementById("lamp2").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lamp2").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
     /*LAMP3*/
    if(message.lamp3 == 0){
        document.getElementById("lamp3").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lamp3").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
    /*LAMP4*/
    if(message.lamp4 == 0){
        document.getElementById("lamp4").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lamp4").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
    /*LAMP5*/
    if(message.lamp5 == 0){
        document.getElementById("lamp5").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lamp5").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
    /*LAMP6*/
    if(message.lamp6 == 0){
        document.getElementById("lamp6").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lamp6").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
     /*LAMP AUTO*/
    if(message.lampAuto == 0){
        document.getElementById("lampAuto").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lampAuto").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
    /*LAMPDEADMAN*/
    if(message.lampDeadman == 0){
        document.getElementById("lampDeadman").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("lampDeadman").innerHTML = "<i class=\"fas fa-lightbulb\" style='font-size:24px;color:purple'>";
    }
     /*Buzzer*/
    if(message.lamp6 == 0){
        document.getElementById("buzzer").innerHTML = "<i class=\"fas fa-volume-off\" style='font-size:24px;color:gray'>";
    }
    else{
        document.getElementById("buzzer").innerHTML = "<i class=\"fas fa-volume-up\" style='font-size:24px;color:green'>";
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