window.addEventListener("DOMContentLoaded", function() {
    let tabBtn = document.getElementsByClassName("tab");
    var len =tabBtn.length;
    for(var i = 0; i < len; i++){
        tabBtn[i].addEventListener("click", showTable);
    }

    let allBtn = document.getElementById("viewAll");
    allBtn.addEventListener("click", showall);
    
});

function showTable(){
    var tid = this.value;

    let tables = document.getElementsByClassName("table");
    var len = tables.length;
    for(var i = 0; i < len; i++){
        tables[i].style.display = "none";
    }

    document.getElementById(tid).style.display = "block";
}

function showall(){
    let tables = document.getElementsByClassName("table");
    var len = tables.length;
    for(var i = 0; i < len; i++){
        tables[i].style.display = "block";
    }
}