window.addEventListener("DOMContentLoaded", function() {
    let requestBtn = document.getElementById("match-btn");
	
    requestBtn.addEventListener("click", getMatch);

});

function getMatch(){
    popupWindow = window.open("../templates/matchup.html", "matchup", "width=500,height=500");
}

