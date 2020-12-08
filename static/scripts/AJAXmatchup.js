var createClock;
var callingBtnValue;
var gametype;
var matchid;
var matchexpired = 0;

function seeCountdown() {
  callingBtnValue = event.target.value;
  let container = document.getElementById(callingBtnValue);
  let displays = document.getElementsByClassName("expTime")
  let gametypeinput = container.nextElementSibling;
  gametype = gametypeinput.value;
  let matchidinput = gametypeinput.nextElementSibling;
  matchid = matchidinput.value;

  clearInterval(createClock);

  if(container.style.display == "none") {
    container.style.display = "block";
    createClock = setInterval(newerWay, 1000);
    for(let i = 0; i < displays.length; i++) {
      if(displays[i] != container){
        displays[i].style.display = "none";
      }
    }
  } else {
    container.style.display = "none";
    clearInterval(createClock)
  }
}

function hideCountdown() {
  clearInterval(createClock);
}



function refreshCountdown(data) {
  let container = document.getElementById(callingBtnValue);
  // Uncomment this code after done testing!!!!!
  let oneweek = 604800000;
  let weekFromSetup = Date.parse(data) + oneweek;
  
  
  // /* Comment this code out after done testing!! */
  // let oneweek = -999999999999;
  // let weekFromSetup = Date.parse(data) + oneweek;


  let timeTillExpiration = timebetween(Date.parse(new Date()), weekFromSetup);

  if(timeTillExpiration.includes("-")) {
    container.innerHTML = "Time to report match has expired"
    container.parentElement.previousElementSibling.previousElementSibling.firstElementChild.disabled = true;
    matchexpired = 1;
  } else{
    container.innerHTML = `Reporting window ends in: ${timeTillExpiration}`
  }

}

/* Code modified from htmlgoodies.com article by Robert Gravelle*/
function timebetween(date1, date2) {
  //Get 1 day in milliseconds
  var one_day = 1000*60*60*24;

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
  .catch(function(error) {
          console.log(error);
  })
  }

