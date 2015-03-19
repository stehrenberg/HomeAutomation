var websocket;
var wsUri = "ws://192.168.56.101/echo";
var heartbeat_timer;

// 	Handle difference for browsers
if (window.addEventListener)
{
		window.addEventListener("load", init, false);
		window.addEventListener("unload", closeSocket, false);
}
else if (window.attachEvent)
{
		window.attachEvent("onload", init);
		window.attachEvent("onunload", closeSocket);
}



// ********************
// function definitions
// ********************

function init()
{	
	// initialize indicator colors
	setColor(1,"WHITE");
	setColor(2,"RED");
	// check whether browser supports websockets
    if ("WebSocket" in window){
    	
    	writeToScreen("This browser supports websockets");
    	
    	// start HEARTBEAT timer: if connected, send a heartbeat every half second
    	heartbeat_timer = setInterval(function()
                {
                    if(websocket && websocket.readyState == 1){
                        websocket.send('HEARTBEAT');
                    	setColor(1,"BLACK");
                    }  
                    else{
                    	setColor(2,"RED");
                    }                       
                }, 500);    	
    }
    else{
    	writeToScreen("This browser does not support websockets !!");
    	setColor(2,"BLACK");
    }  
}

// **************
// event handlers
// **************

function onMessage(evt)
{
	if(evt.data == '.'){ // HEARTBEAT response
		setTimeout(function(){setColor(1,"WHITE");}, 200); // set Indicator1 to white 200 ms after heartbeat response was reveived
	}else{
	    writeToScreen(evt.data);
	}
} 

function onOpen(evt)
{
	setColor(2,"GREEN")
}

function onClose(evt)
{
	setColor(2,"RED")
}

function onError(evt)
{
	alert(evt.data)
}


// *****************
// onclick functions 
// *****************

function connectWebSocket()
{
    if("WebSocket" in window){
        if(!websocket || websocket.readyState == 0 || websocket.readyState == 3){
            websocket = new WebSocket(wsUri);
            websocket.onopen = function(evt) { onOpen(evt) };
            websocket.onclose = function(evt) { onClose(evt) };
            websocket.onmessage = function(evt) { onMessage(evt) };
            websocket.onerror = function(evt) { onError(evt) };
            // sendMessage("websocket initiated, waiting ...") // this is to prevent time-out during ws connection set-up; the server expects some bytes ...
        }
    }
}
   
function closeSocket()
{
    if(websocket && (websocket.readyState == 1)){
        websocket.close();    
    }
}  

function getSocketState()
{
	msg = "Socket state: " + websocket.readyState.toString();
	writeToScreen(msg);
}

function stopHeartbeat()
{
	clearInterval(heartbeat_timer);
}

// *****************
// utility functions
// *****************

function sendMessage(message)
{
    if(websocket && websocket.readyState == 1){
        websocket.send(message);
    }  
}
 
function writeToScreen(message)
{
	document.all.output.innerHTML = message;
	setTimeout(function(){document.all.output.innerHTML = "";}, 2000);
}

function setColor(indicator_nr, color){
	// parameter color as string, like "RED"
	if(indicator_nr == 1){
		document.all.Indicator1.style.backgroundColor = color;
	}else if(indicator_nr == 2){
		document.all.Indicator2.style.backgroundColor = color;
	}
		
}
