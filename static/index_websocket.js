/* GAUGES */
//canvas initialization
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
//dimensions
var W = canvas.width;
var H = canvas.height;
//Variables
var degrees = 0;
var color = "#100935"; //UVSA Blue
var bgcolor = "#DDD";
var gauge_text;

function gauge_init()
	{
		//Clear the canvas everytime a chart is drawn
		ctx.clearRect(0, 0, W, H);

		//Background 360 degree arc
		ctx.beginPath();
		ctx.strokeStyle = bgcolor;
		ctx.lineWidth = 20;
		ctx.arc(W/2, H/2, 100, 0, Math.PI*2, false); //you can see the arc now
		ctx.stroke();

		//gauge will be a simple arc
		//Angle in radians = angle in degrees * PI / 180
		var radians = degrees * Math.PI / 180;
		ctx.beginPath();
		ctx.strokeStyle = color;
		ctx.lineWidth = 10;
		//The arc starts from the rightmost end. If we deduct 90 degrees from the angles
		//the arc will start from the topmost end
		ctx.arc(W/2, H/2, 100, 0 - 90*Math.PI/180, radians - 90*Math.PI/180, false);
		//you can see the arc now
		ctx.stroke();

		//Lets add the text
		ctx.fillStyle = color;
		ctx.font = "40px Arial";
	}

/* WEBSOCKETS */
var socket = io.connect(location.host); //location.host devuelve la ip del servidor:puerto
var slider = document.getElementById("myTimeRange");
var time_label = document.getElementById("time_tag");
time_label.innerHTML = slider.value + " min."; // Display the default slider value
var operationMode

socket.on('my_response', function(message) {
    //console.log(arguments)
    document.getElementById("date").innerHTML = message.date;
    document.getElementById("time").innerHTML = message.time;
    operationMode = message.operationMode;

    switch (message.state_machine_status)
    {
        case 0:
            break;
        case 1:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-history' style='font-size:160%; color:#394de6'>";
            document.getElementById("operationModeText").innerHTML = "Iniciando proceso";
            break;
        case 2:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-sun' style='font-size:160%; color:purple'>";
            document.getElementById("operationModeText").innerHTML = "Sanitizando";
            break;
        case 3:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-users' style='font-size:160%; color:#ffbf00'>";
            document.getElementById("operationModeText").innerHTML = "En pausa por deteccion";
            break;
        case 4:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-history' style='font-size:160%; color:#394de6'>";
            document.getElementById("operationModeText").innerHTML = "Reiniciando proceso";
            break;
        case 5:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-sun' style='font-size:160%; color:purple'>";
            document.getElementById("operationModeText").innerHTML = "Sanitizando - Manual";
            break;
        case 6:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-hand-paper' style='font-size:160%; color:#1d1f29'>";
            document.getElementById("operationModeText").innerHTML = "Modo manual";
            break;
        case 7:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-check' style='font-size:160%; color:orangered'>";
            document.getElementById("operationModeText").innerHTML = "En espera - Automatico";
            break;
        case 8:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-times' style='font-size:160%; color:red'>";
            document.getElementById("operationModeText").innerHTML = "Error";
            break;
        case 9:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-hand-point-up' style='font-size:160%; color:#bd00bd'>";
            document.getElementById("operationModeText").innerHTML = "Ingresando tiempo";
            break;
        case 10:
            document.getElementById("operationMode").innerHTML = "<i class='fas fa-skull' style='font-size:160%; color:#ffbf00'>";
            document.getElementById("operationModeText").innerHTML = "Proceso abortado - Presencia";
            break;
    };

    var total_time = message.total_time;
    var tiempo  = message.tiempoRestante  //document.getElementById("tiempoRestante").innerHTML
    var hr = Math.floor(tiempo/3600);
    var min = Math.floor((tiempo - (hr*3600))/60);
    var sec = tiempo - (min * 60);
    //document.getElementById("tiempoRestante").innerHTML = ('0'  + hr).slice(-2)+':'+('0'  + min).slice(-2)+':'+('0' + sec).slice(-2);
    if(!isNaN(message.count_down)){
    document.getElementById("count_down").value = 18 - message.count_down;
        gauge_init();
    	gauge_text = ('0'  + hr).slice(-2)+':'+('0'  + min).slice(-2)+':'+('0' + sec).slice(-2);
		//Lets center the text
		//deducting half of text width from position x
		text_width = ctx.measureText(gauge_text).width;
		//adding manual value to position y since the height of the text cannot
		//be measured easily. There are hacks but we will keep it manual for now.
		ctx.fillText(gauge_text, W/2 - text_width/2 , H/2 +15);
		degrees = (Math.floor(tiempo*360/total_time));
    }
    });

function launchIt(){
    // Fnc llamada por la funcion del boton de iniciar el proceso
    var flag_time = 1;
    var flag_hardware = 0;
    socket.emit('startButton',{'time':[flag_time, slider.value * 60], 'mask':[flag_hardware, 0]});
};

function startButton(){
    if (((slider.value * 60) < 300)  && (operationMode == 3)){
        if (confirm ("No se recomienda utilizar tiempos menores a 5 minutos.\nPresione \"OK\" para continuar o \"Cancel\" para regresar."))
        {
            launchIt();
        }
        else
        {
            slider.value = 5;
            time_label.innerHTML = 5  + " min.";
            time_label.innerHTML = 5  + " min.";

        }
    }
    else
    {
        launchIt();
    }
};

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  time_label.innerHTML = this.value  + " min.";
  //console.log(this.value);
}

window.onload = function() {
        socket.emit('connect');
	degrees = 0;
};
