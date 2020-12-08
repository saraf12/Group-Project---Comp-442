window.addEventListener("DOMContentLoaded", function() {
    let recordBtn = document.getElementsByClassName("recordBtn");

    var len = recordBtn.length;
    for(var i = 0; i < len; i++){
      recordBtn[i].addEventListener("click", showRecord);
    }
    
});

function showRecord(){
  tableID = "recordTable" + this.id;
  let table = document.getElementById(tableID);
  if(table.style.display == ""){
    console.log("B");
    table.style.display = "block";
  }else{
    console.log("N");
    table.style.display = "";
  }
}

function gamesTab(evt, games){
    var i, tabcontent, tablinks;
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
