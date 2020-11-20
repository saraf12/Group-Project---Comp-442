window.addEventListener("DOMContentLoaded", function() {
   
    let iconsBtn = document.getElementsByClassName("icons");
    var len = iconsBtn.length;
    
    
    
    for(var i = 0; i < len; i++){
        iconsBtn[i].addEventListener("click", changeIcon);
    }
});
var current = 0;

function changeIcon(){
    let profile = document.getElementById("Uicon");
    var color = this.id;
    switch (this.id){
        case "black":
            profile.src = "../static/userIcon/black.png";
            break;
        case "Blue":
            profile.src = "../static/userIcon/Blue.png";
            break;
        case "darkBlue":
            profile.src = "../static/userIcon/darkBlue.png";
            break;
        case "gray":
            profile.src = "../static/userIcon/gray.png";
            break;
        case "green":
            profile.src = "../static/userIcon/green.png";
            break;
        case "lightBlue":
            profile.src = "../static/userIcon/lightBlue.png";
            break;
        case "lightGreen":
            profile.src = "../static/userIcon/lightGreen.png";
            break;
        case "orange":
            profile.src = "../static/userIcon/orange.png";
            break;
        case "pink":
            profile.src = "../static/userIcon/pink.png";
            break;
        case "purple":
            profile.src = "../static/userIcon/purple.png";
            break;
        case "red":
            profile.src = "../static/userIcon/red.png";
            break;
        case "yellow":
            profile.src = "../static/userIcon/yellow.png";
            break;
                    
        default:
            profile.src = "../static/userIcon/black.png";
            break;
    }
}