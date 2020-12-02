window.addEventListener("DOMContentLoaded", function() {
    let recordBtn = document.getElementById("recordBtn");
    recordBtn.addEventListener("click", showRecord);

    let submitBtn = document.getElementsByName("submitRecord");
    var len = submitBtn.length;
    for(var i = 0; i < len; i++){
        submitBtn[i].addEventListener("click", submitRecord);
    }
    
    let iconBtn = document.getElementById("profileIcons");
    iconBtn.addEventListener("click", editProfile);
});

function showRecord(){
    let table = document.getElementById("recordTable");
    if(table.style.display === "none"){
        console.log("B");
        table.style.display = "block";
    }else{
        console.log("N");
        table.style.display = "none";
    }
}

// function submitRecord(){
//     //What do we want the submit button to do
//     //this.disabled = true;
//     name = "result" + this.id;
//     let radioBtn = document.getElementsByName(name);
//     var len = radioBtn.length;
//     var x = 0;
//     for(var i = 0; i < len; i++){
//         if(radioBtn[i].checked == true){
//             x = 1;
//         }
//     }
//     if(x == 1){
//         this.display = "none";
//         for(var e = 0; e < len; e++){
//             radioBtn[e].disabled = true;
//         }
//     }
        

// }

// function editProfile(){
//     let newWin = window.open("../templates/mainPage.html", "hello", "width=200,height=200");
//     //newWin.document.write("Hello, world!");
// }

function showRecords(evt, games){
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