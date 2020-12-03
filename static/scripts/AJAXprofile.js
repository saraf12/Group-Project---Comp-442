window.addEventListener("DOMContentLoaded", function() {
    let recordBtn = document.getElementById("recordBtn");
    recordBtn.addEventListener("click", showRecord);

});

function showRecord(){
    let table = document.getElementById("recordTable");
    if(table.style.display === ""){
        console.log("B");
        table.style.display = "block";
    }else{
        console.log("N");
        table.style.display = "";
    }
}


function gamesTab(evt, games){
    var i, tabcontent, tablinks;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            tabcontent = document.getElementsByClassName("recordInfo");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(games).style.display = "block";
            evt.currentTarget.className += " active";
        }
    };
    xmlhttp.open("GET","/profilepage/?showtab=true",true);
    xmlhttp.send();  
}

function showUser(str) {
    if (str == "") {
      document.getElementById("txtHint").innerHTML = "";
      return;
    } else {
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("txtHint").innerHTML = this.responseText;
        }
      };
      xmlhttp.open("GET","getuser.php?q="+str,true);
      xmlhttp.send();
    }
  }