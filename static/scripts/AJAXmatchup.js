// window.addEventListener("DOMContentLoaded", function() {
//   //displayTime();
//   newerWay();
//   //const createClock = setInterval(displayTime, 1000);
//   const createClock = setInterval(newerWay, 1000);
// });

var createClock;
//ar cnt = 0;
var callingBtnValue;
var gametype;
var matchid;
var matchexpired = 0;

function seeCountdown() {
  callingBtnValue = event.target.value;
  let container = document.getElementById(callingBtnValue);
  //console.log(container);
  let displays = document.getElementsByClassName("expTime")
  let gametypeinput = container.nextElementSibling;
  gametype = gametypeinput.value;
  let matchidinput = gametypeinput.nextElementSibling;
  matchid = matchidinput.value;
  //console.log(container.nextElementSibling.value);
  
  // if(container == displays[0]) {
  //   console.log("They're equal");
  // } else {
  //   console.log("They're not equal");
  // }

  clearInterval(createClock);
 // console.log(container.style.display);
  if(container.style.display == "none") {
    container.style.display = "block";
    createClock = setInterval(newerWay, 1000);
    for(let i = 0; i < displays.length; i++) {
      //console.log(displays[i]);
      if(displays[i] != container){
        displays[i].style.display = "none";
      }
    }
  } else {
    container.style.display = "none";
    clearInterval(createClock)
  }

  //console.log(displays[0]);
  // if(container.style.display == "block") {
  //   console.log("Getting into else statement");
  //   clearInterval(createClock);
  //   console.log("making it past clearing statement");
  //   //let gameid = document.getElementById("expiration-btn").value;
  //   //container.innerHTML = "";
  //   container.style.display = "none"
  //   //cnt = 0;
  // } else {
  //   createClock = setInterval(newerWay, 1000);
  //   //cnt = 1;
  //   container.style.display = "block";
  //   for(let i = 0; i < displays.length; i++) {
  //     if (displays[i] != container) {
  //       displays[i].style.display = "none";
  //     }
  //   }
  // }
}

function hideCountdown() {
  clearInterval(createClock);
}


// function displayTime() {
//   let date = new Date();
//   //let dueDate = new Date(Date.UTC(2020, 11, 20, 12));
//   //let time = date.toLocaleTimeString();
//   document.querySelector('.clock').textContent = date;
// }


function refreshCountdown(data) {
  //let gameid = document.getElementById("expiration-btn").value;
  let container = document.getElementById(callingBtnValue);
  //console.log(container.id);
  // Uncomment this code after done testing!!!!!
  let oneweek = 604800000;
  let weekFromSetup = Date.parse(data) + oneweek;
  
  
  // /* Comment this code out after done testing!! */
  // let oneweek = -999999999999;
  // //console.log(Date.parse(data));
  // //DID NOT WORK!!
  // // let now = new Date();
  // // let utc_timestamp = Date.UTC(now.getUTCFullYear(),now.getUTCMonth(), now.getUTCDate() , 
  // //     now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds(), now.getUTCMilliseconds());
  // // console.log(utc_timestamp);
  // let weekFromSetup = Date.parse(data) + oneweek;
  // console.log(weekFromSetup);

  let timeTillExpiration = timebetween(Date.parse(new Date()), weekFromSetup);
  //console.log(timeTillExpiration);

  //let trialrun = timebetween(Date.parse(new Date()), Date.parse(data));
  //console.log(trialrun);

  if(timeTillExpiration.includes("-")) {
    container.innerHTML = "Time to report match has expired"
    container.parentElement.previousElementSibling.previousElementSibling.firstElementChild.disabled = true;
    //console.log(container.parentElement.previousElementSibling.previousElementSibling.firstElementChild);
    matchexpired = 1;
  } else{
    container.innerHTML = `Reporting window ends in: ${timeTillExpiration}`
  }

}

/* Code modified from htmlgoodies.com article by Robert Gravelle*/
function timebetween(date1, date2) {
  //Get 1 day in milliseconds
  var one_day = 1000*60*60*24;
  //console.log(date1);
 // console.log(date2);
  // Calculate the difference in milliseconds
  var difference_ms = date2 - date1;
  //take out milliseconds
  difference_ms = difference_ms/1000;
  var seconds = Math.floor(difference_ms % 60);
  difference_ms = difference_ms/60; 
  var minutes = Math.floor(difference_ms % 60);
  difference_ms = difference_ms/60; 
  var hours = Math.floor(difference_ms % 24);  
  var days = Math.floor(difference_ms/24);

  //return days + ' days, ' + hours + ' hours, ' + minutes + ' minutes';
  
  return days + ' days, ' + hours + ' hours, ' + minutes + ' minutes, and ' + seconds + ' seconds';
}



function newerWay() {
  //let gameid = document.getElementById(callingBtnValue).id;
  //let gameid = document.getElementById("expiration-btn").value;
  //console.log(gameid)
fetch(`/datecreated/${gametype}/${matchid}/${matchexpired}`)
  .then(function (response) {
    if (response.ok) { return response.json(); }
    else { return Promise.reject(response); }
  })
  .then(function(message){
    if(message == "Expired") {
      throw 'Game has expired'
    }
    else {
      return message;
    }
  })
  .then(refreshCountdown)
  // .then(function(value) {
    
  // })
  .catch(function(error) {
          console.log(error);
          //Doesn't work
          // clearInterval(createClock);
  })
  }

