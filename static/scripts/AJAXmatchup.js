// window.addEventListener("DOMContentLoaded", function() {
//   //displayTime();
//   newerWay();
//   //const createClock = setInterval(displayTime, 1000);
//   const createClock = setInterval(newerWay, 1000);
// });

var createClock;
var cnt = 0;
var callingBtnValue;

function seeCountdown() {
  callingBtnValue = event.target.value;
  if(cnt == 0) {
    createClock = setInterval(newerWay, 1000);
    cnt = 1;
  } else {
    console.log("Getting into else statement");
    clearInterval(createClock);
    //let gameid = document.getElementById("expiration-btn").value;
    let container = document.getElementById(callingBtnValue);
    container.innerHTML = "";
    cnt = 0;
  }
}

function hideCountdown() {
  clearInterval(createClock);
}


function displayTime() {
  let date = new Date();
  //let dueDate = new Date(Date.UTC(2020, 11, 20, 12));
  //let time = date.toLocaleTimeString();
  document.querySelector('.clock').textContent = date;
}


function refreshCountdown(data) {
  //let gameid = document.getElementById("expiration-btn").value;
  let container = document.getElementById(callingBtnValue);
  console.log(container);
  let oneweek = 604800000;
  let weekFromSetup = Date.parse(data) + oneweek;
  //console.log(weekFromSetup);

  let timeTillExpiration = timebetween(Date.parse(new Date()), weekFromSetup);
  console.log(timeTillExpiration);

  let trialrun = timebetween(Date.parse(new Date()), Date.parse(data));
  //console.log(trialrun);

  container.innerHTML = `Reporting window ends in: ${timeTillExpiration}`
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
  
  return days + ' days, ' + hours + ' hours, ' + minutes + ' minutes, and ' + seconds + ' seconds';
}



function newerWay() {
  let gameid = document.getElementById("expiration-btn").value;
  console.log("gameid")
fetch(`/datecreated/${gameid}`)
  .then(function (response) {
    if (response.ok) { return response.json(); }
    else { return Promise.reject(response); }
  })
  .then(refreshCountdown)
  .catch(function(error) {
          console.log(error);
          //Doesn't work
          // clearInterval(createClock);
  })
  }

