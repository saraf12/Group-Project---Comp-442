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

function submitRecord(){
    //What do we want the submit button to do
    
}

function editProfile(){
    let newWin = window.open("../templates/mainPage.html", "hello", "width=200,height=200");
    //newWin.document.write("Hello, world!");
}

