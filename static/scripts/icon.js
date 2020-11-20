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
    let Iprofile = document.getElementById("Iprofile");
    var color = this.id;
    switch (this.id){
        case "black":
            profile.src = "../static/userIcon/black.png";
            Iprofile.value = "black.png";
            //console.log(Iprofile.value);
            break;
        case "Blue":
            profile.src = "../static/userIcon/Blue.png";
            Iprofile.value = "Blue.png";
            //console.log(Iprofile.value);
            break;
        case "darkBlue":
            profile.src = "../static/userIcon/darkBlue.png";
            Iprofile.value = "darkBlue.png";
            // console.log(Iprofile.value);
            break;
        case "gray":
            profile.src = "../static/userIcon/gray.png";
            Iprofile.value = "gray.png";
            //console.log(Iprofile.value);
            break;
        case "green":
            profile.src = "../static/userIcon/green.png";
            Iprofile.value = "green.png";
            //console.log(Iprofile.value);
            break;
        case "lightBlue":
            profile.src = "../static/userIcon/lightBlue.png";
            Iprofile.value = "lightBlue.png";
            console.log(Iprofile.value);
            break;
        case "lightGreen":
            profile.src = "../static/userIcon/lightGreen.png";
            Iprofile.value = "lightGreen.png";
            //console.log(Iprofile.value);
            break;
        case "orange":
            profile.src = "../static/userIcon/orange.png";
            Iprofile.value = "orange.png";
            //console.log(Iprofile.value);
            break;
        case "pink":
            profile.src = "../static/userIcon/pink.png";
            Iprofile.value = "pink.png";
            //console.log(Iprofile.value);
            break;
        case "purple":
            profile.src = "../static/userIcon/purple.png";
            Iprofile.value = "purple.png";
            //console.log(Iprofile.value);
            break;
        case "red":
            profile.src = "../static/userIcon/red.png";
            Iprofile.value = "red.png";
            //console.log(Iprofile.value);
            break;
        case "yellow":
            profile.src = "../static/userIcon/yellow.png";
            Iprofile.value = "yellow.png";
            //console.log(Iprofile.value);
            break;
                    
        default:
            profile.src = "../static/userIcon/black.png";
            Iprofile.value = "black.png";
            //console.log(Iprofile.value);
            break;
    }
}