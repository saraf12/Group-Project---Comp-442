window.addEventListener("DOMContentLoaded", function() {
    let recordBtn = document.getElementById("recordBtn");

    let submitBtn = document.getElementsByName("submitRecord");
    var len = submitBtn.length;
    for(var i = 0; i < len; i++){
        submitBtn[i].addEventListener("click", submitRecord);
    }
	
    recordBtn.addEventListener("click", showRecord);
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
    
}
