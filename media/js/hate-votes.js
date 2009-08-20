var xmlHttp = null;

function VoteUp(str) {
    try {
        // Firefox, Opera 8.0+, Safari, IE7
        xmlHttp = new XMLHttpRequest();
    }
    catch(e) {
        // Old IE
        try {
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch(e) {
            alert("Your browser does not support XMLHTTP!");
            return;
        }
    }

    //alert("should be working" + str);
    var url = "http://www.hateonyourjob.com/vote_up/" + str;
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    //alert(document.getElementById("item" + str).innerHTML);
    document.getElementById("item" + str).innerHTML = xmlHttp.responseText;
}

function VoteDown(str)
 {
    try
    {
        // Firefox, Opera 8.0+, Safari, IE7
        xmlHttp = new XMLHttpRequest();
    }
    catch(e)
    {
        // Old IE
        try
        {
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch(e)
        {
            alert("Your browser does not support XMLHTTP!");
            return;
        }
    }
    //alert("should be working");
    var url = "http://www.hateonyourjob.com/vote_down/" + str;
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    document.getElementById("item" + str).innerHTML = xmlHttp.responseText;
}
