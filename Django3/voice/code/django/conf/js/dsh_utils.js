function getHTTPObject() { 
    var xmlhttp; 
    if (!xmlhttp && typeof XMLHttpRequest != 'undefined') { 
        try { xmlhttp = new XMLHttpRequest(); } 
	catch (e) { xmlhttp = false; } 
    } return xmlhttp; 
}



function select_obj(whatKind, dshUid, img) {
    //whatKind: item,person,organization,keyword,event.
    //used to construct django URL, like "/select/item/blah".
    if (img.src == "/icons/ok.gif") return true;
    var http = getHTTPObject();
    http.open("GET","/select/"+escape(whatKind)+"/"+escape(dshUid),true);
    http.onreadystatechange = function() {
	if (http.readyState == 4) {
	    if (http.status == 200) {
		if (http.responseText == "True") {
		    window.status = "successfully selected " + dshUid;
		    img.src = "/icons/ok.gif";
                    img.width = 11;
                    img.height = 11;
		    img.title = "selected";
		} else {
		    window.status = "error in selecting " + dshUid;
		}
	    } else
		alert("Error: " + http.statusText);
	}
    }
    http.send(null);
}



function print_year() { 
    var d = new Date();
    document.write(d.getFullYear());
}



function add_sm_control() {
    //not used.  didn't work.
    controlStr = "<div id=\"control-template\"> <!-- control markup inserted dynamically after each link --> <div class=\"controls\"> <div class=\"statusbar\"> <div class=\"loading\"></div> <div class=\"position\"></div> </div> </div> <div class=\"timing\"> <div id=\"sm2_timing\" class=\"timing-data\"> <span class=\"sm2_position\">%s1</span> / <span class=\"sm2_total\">%s2</span></div> </div> <div class=\"peak\"> <div class=\"peak-box\"><span class=\"l\"></span><span class=\"r\"></span> </div> </div> </div> <div id=\"spectrum-container\" class=\"spectrum-container\"> <div class=\"spectrum-box\"> <div class=\"spectrum\"></div> </div> </div>";
    document.getElementById("dsh_sm_controls").innerHTML = controlStr;
}
