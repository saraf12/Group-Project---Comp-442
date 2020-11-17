window.addEventListener("DOMContentLoaded", function() {
    let requestBtn = document.getElementById("match-btn");
	
    requestBtn.addEventListener("click", getMatch);
});

function getMatch(){
    let pendingMatch = window.open("about:", "matchup", "width=00,height=200");
    pendingMatch.document.write("Hello, world!");
}

