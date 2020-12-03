var popupWindow = window;
window.addEventListener("DOMContentLoaded", function() {
    let requestBtn = document.getElementsByClassName("match-btn");
    var len = requestBtn.length;
    for(var i = 0; i < len; i++){
        requestBtn[i].addEventListener("click", getMatch);
    }


    let selectGameDropdown = document.getElementById("dropdown-menu");
    selectGameDropdown.addEventListener("change", selGame);

    
    // let game1btn = document.getElementById("game1");
    // game1btn.addEventListener("click", selectGame1);
    // let game2btn = document.getElementById("game2");
    // game2btn.addEventListener("click", selectGame2);
    // let game3btn = document.getElementById("game3");
    // game3btn.addEventListener("click", selectGame3);
    // let game4btn = document.getElementById("game4");
    // game4btn.addEventListener("click", selectGame4);

});

function selGame() {
    // console.log("made it inside the function!");
    let idOfSelGame = this.options[this.options.selectedIndex].id;
    // console.log(idOfSelGame);
    // console.log(this.options);

    let idOfTab = "Tab" + idOfSelGame;

    // console.log(this.options.length);

    // let selectedGame;

    for(let i = 1; i < this.options.length; i++){
       // console.log(this.options);
        let idOfCurrTab = "Tab" + this.options[i].id;
       // console.log(idOfCurrTab);
        let currTab = document.getElementById(idOfCurrTab);
       // console.log(currTab);
        if(this.options[i].id == idOfSelGame) {
           currTab.style.display = "inline";
           selectedGame = this.options[i].id;
        }
        else {
            currTab.style.display = "none";
        }
    }

    let lbid = "lb" + idOfSelGame;
    let lb = document.getElementsByClassName("lb");
    // let correctlb = document.getElementById(lbid);
    console.log(lb);

    console.log(lb.length);

    for(let i = 0; i < lb.length; i++) {
        console.log("This is lb[i]:")
        console.log(lb[i]);
        let idOfCurrLb = lb[i].id;
        let currLb = document.getElementById(idOfCurrLb);
        console.log(idOfCurrLb);
        console.log(currLb);
        if(idOfCurrLb == lbid) {
            currLb.style.display = "inline";
        }
        else {
            currLb.style.display = "none";
        }
    }

    // selectedGameDict = {
    //     gameid: selectedGame
    // };

    
    // let entry = {
    //     name: "Cathy",
    //     message: "Hi"
    // };

    // console.log(entry);

    // console.log(selectedGameDict);

    // fetch(`${window.origin}/ajaxtest/`, {
    //     method: "POST",
    //     credentials: "include",
    //     body: JSON.stringify(selectedGameDict),
    //     cache: "no-cache",
    //     headers: new Headers({
    //         "content-type": "application/json"
    //     })
    // })
    // .then(function(response) {
    //     if(response.status != 200) {
    //         console.log(`Response status was not 200 ${response.status}`);
    //         return ;
    //     }

    //     response.json().then(function (data) {
    //         console.log(data);
    //     })
    // })
    
}

function test() {

    // let entry = {
    //     name: "Cathy",
    //     message: "Hi"
    // };

    // console.log(entry);

    // fetch(`${window.origin}/ajaxtest/`, {
    //     method: "POST",
    //     credentials: "include",
    //     body: JSON.stringify(entry),
    //     cache: "no-cache",
    //     headers: new Headers({
    //         "content-type": "application/json"
    //     })
    // })
    // .then(function(response) {
    //     if(response.status != 200) {
    //         console.log(`Response status was not 200 ${response.status}`);
    //         return ;
    //     }

    //     response.json().then(function (data) {
    //         console.log(data);
    //     })
    // })
}

function getMatch(){
    console.log(this.id);
    let matchupurl = "/matchup/" + this.id;
    console.log(matchupurl);
    popupWindow.open(matchupurl, "matchup", "width=500,height=500");
    // popupWindow = window.open("matchup.html","matchup","width=300,height=200");
 
}


function closeWindow() {
    popupWindow.close();
}

// function selectGame1(){
//     let g1li = document.getElementById("game1");
//     g1li.style.backgroundColor = "grey";
//     let g1btn = document.getElementById("g1btn");
//     g1btn.style.backgroundColor = "grey";
//     let g2li = document.getElementById("game2");
//     g2li.style.backgroundColor = "#24abbd";
//     let g2btn = document.getElementById("g2btn");
//     g2btn.style.backgroundColor = "#24abbd";
//     let g3li = document.getElementById("game3");
//     g3li.style.backgroundColor = "#24abbd";
//     let g3btn = document.getElementById("g3btn");
//     g3btn.style.backgroundColor = "#24abbd";
//     let g4li = document.getElementById("game4");
//     g4li.style.backgroundColor = "#24abbd";
//     let g4btn = document.getElementById("g4btn");
//     g4btn.style.backgroundColor = "#24abbd";

//     let g1 = document.getElementById("Tab1");
//     g1.style.display = "inline";
//     let g2 = document.getElementById("Tab2");
//     g2.style.display = "none";
//     let g3 = document.getElementById("Tab3");
//     g3.style.display = "none";
//     let g4 = document.getElementById("Tab4");
//     g4.style.display = "none";
// }

// function selectGame2(){
//     let g1li = document.getElementById("game1");
//     g1li.style.backgroundColor = "#24abbd";
//     let g1btn = document.getElementById("g1btn");
//     g1btn.style.backgroundColor = "#24abbd";
//     let g2li = document.getElementById("game2");
//     g2li.style.backgroundColor = "grey";
//     let g2btn = document.getElementById("g2btn");
//     g2btn.style.backgroundColor = "grey";
//     let g3li = document.getElementById("game3");
//     g3li.style.backgroundColor = "#24abbd";
//     let g3btn = document.getElementById("g3btn");
//     g3btn.style.backgroundColor = "#24abbd";
//     let g4li = document.getElementById("game4");
//     g4li.style.backgroundColor = "#24abbd";
//     let g4btn = document.getElementById("g4btn");
//     g4btn.style.backgroundColor = "#24abbd";


//     let g1 = document.getElementById("Tab1");
//     g1.style.display = "none";
//     let g2 = document.getElementById("Tab2");
//     g2.style.display = "inline";
//     let g3 = document.getElementById("Tab3");
//     g3.style.display = "none";
//     let g4 = document.getElementById("Tab4");
//     g4.style.display = "none";
// }

// function selectGame3(){
//     let g1li = document.getElementById("game1");
//     g1li.style.backgroundColor = "#24abbd";
//     let g1btn = document.getElementById("g1btn");
//     g1btn.style.backgroundColor = "#24abbd";
//     let g2li = document.getElementById("game2");
//     g2li.style.backgroundColor = "#24abbd";
//     let g2btn = document.getElementById("g2btn");
//     g2btn.style.backgroundColor = "#24abbd";
//     let g3li = document.getElementById("game3");
//     g3li.style.backgroundColor = "grey";
//     let g3btn = document.getElementById("g3btn");
//     g3btn.style.backgroundColor = "grey";
//     let g4li = document.getElementById("game4");
//     g4li.style.backgroundColor = "#24abbd";
//     let g4btn = document.getElementById("g4btn");
//     g4btn.style.backgroundColor = "#24abbd";


//     let g1 = document.getElementById("Tab1");
//     g1.style.display = "none";
//     let g2 = document.getElementById("Tab2");
//     g2.style.display = "none";
//     let g3 = document.getElementById("Tab3");
//     g3.style.display = "inline";
//     let g4 = document.getElementById("Tab4");
//     g4.style.display = "none";
// }

// function selectGame4(){
//     let g1li = document.getElementById("game1");
//     g1li.style.backgroundColor = "#24abbd";
//     let g1btn = document.getElementById("g1btn");
//     g1btn.style.backgroundColor = "#24abbd";
//     let g2li = document.getElementById("game2");
//     g2li.style.backgroundColor = "#24abbd";
//     let g2btn = document.getElementById("g2btn");
//     g2btn.style.backgroundColor = "#24abbd";
//     let g3li = document.getElementById("game3");
//     g3li.style.backgroundColor = "#24abbd";
//     let g3btn = document.getElementById("g3btn");
//     g3btn.style.backgroundColor = "#24abbd";
//     let g4li = document.getElementById("game4");
//     g4li.style.backgroundColor = "grey";
//     let g4btn = document.getElementById("g4btn");
//     g4btn.style.backgroundColor = "grey";


//     let g1 = document.getElementById("Tab1");
//     g1.style.display = "none";
//     let g2 = document.getElementById("Tab2");
//     g2.style.display = "none";
//     let g3 = document.getElementById("Tab3");
//     g3.style.display = "none";
//     let g4 = document.getElementById("Tab4");
//     g4.style.display = "inline";
// }