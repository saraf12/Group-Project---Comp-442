function giveAcceptConfirmation () {
    console.log(this.responseText);
}
  
  var confirm = new XMLHttpRequest();
  confirm.addEventListener("load", giveAcceptConfirmation);
  confirm.open("GET", "/acceptconfirmation/");
  confirm.send();