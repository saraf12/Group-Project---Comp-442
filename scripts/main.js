window.addEventListener("DOMContentLoaded", function() {
    let requestBtn = document.getElementById("match-btn");
	
    requestBtn.addEventListener("click", getMatch);

    let game1btn = document.getElementById("game1");
    game1btn.addEventListener("click", selectGame1);
    let game2btn = document.getElementById("game2");
    game2btn.addEventListener("click", selectGame2);
    let game3btn = document.getElementById("game3");
    game3btn.addEventListener("click", selectGame3);
    let game4btn = document.getElementById("game4");
    game4btn.addEventListener("click", selectGame4);

});

function getMatch(){
    popupWindow = window.open("../templates/matchup.html", "matchup", "width=500,height=500");
}

function selectGame1(){
    let g1li = document.getElementById("game1");
    g1li.style.backgroundColor = "grey";
    let g1btn = document.getElementById("g1btn");
    g1btn.style.backgroundColor = "grey";
    let g2li = document.getElementById("game2");
    g2li.style.backgroundColor = "#24abbd";
    let g2btn = document.getElementById("g2btn");
    g2btn.style.backgroundColor = "#24abbd";
    let g3li = document.getElementById("game3");
    g3li.style.backgroundColor = "#24abbd";
    let g3btn = document.getElementById("g3btn");
    g3btn.style.backgroundColor = "#24abbd";
    let g4li = document.getElementById("game4");
    g4li.style.backgroundColor = "#24abbd";
    let g4btn = document.getElementById("g4btn");
    g4btn.style.backgroundColor = "#24abbd";
}

function selectGame2(){
    let g1li = document.getElementById("game1");
    g1li.style.backgroundColor = "#24abbd";
    let g1btn = document.getElementById("g1btn");
    g1btn.style.backgroundColor = "#24abbd";
    let g2li = document.getElementById("game2");
    g2li.style.backgroundColor = "grey";
    let g2btn = document.getElementById("g2btn");
    g2btn.style.backgroundColor = "grey";
    let g3li = document.getElementById("game3");
    g3li.style.backgroundColor = "#24abbd";
    let g3btn = document.getElementById("g3btn");
    g3btn.style.backgroundColor = "#24abbd";
    let g4li = document.getElementById("game4");
    g4li.style.backgroundColor = "#24abbd";
    let g4btn = document.getElementById("g4btn");
    g4btn.style.backgroundColor = "#24abbd";
}

function selectGame3(){
    let g1li = document.getElementById("game1");
    g1li.style.backgroundColor = "#24abbd";
    let g1btn = document.getElementById("g1btn");
    g1btn.style.backgroundColor = "#24abbd";
    let g2li = document.getElementById("game2");
    g2li.style.backgroundColor = "#24abbd";
    let g2btn = document.getElementById("g2btn");
    g2btn.style.backgroundColor = "#24abbd";
    let g3li = document.getElementById("game3");
    g3li.style.backgroundColor = "grey";
    let g3btn = document.getElementById("g3btn");
    g3btn.style.backgroundColor = "grey";
    let g4li = document.getElementById("game4");
    g4li.style.backgroundColor = "#24abbd";
    let g4btn = document.getElementById("g4btn");
    g4btn.style.backgroundColor = "#24abbd";
}

function selectGame4(){
    let g1li = document.getElementById("game1");
    g1li.style.backgroundColor = "#24abbd";
    let g1btn = document.getElementById("g1btn");
    g1btn.style.backgroundColor = "#24abbd";
    let g2li = document.getElementById("game2");
    g2li.style.backgroundColor = "#24abbd";
    let g2btn = document.getElementById("g2btn");
    g2btn.style.backgroundColor = "#24abbd";
    let g3li = document.getElementById("game3");
    g3li.style.backgroundColor = "#24abbd";
    let g3btn = document.getElementById("g3btn");
    g3btn.style.backgroundColor = "#24abbd";
    let g4li = document.getElementById("game4");
    g4li.style.backgroundColor = "grey";
    let g4btn = document.getElementById("g4btn");
    g4btn.style.backgroundColor = "grey";
}