document.getElementById("del-open-popup-btn").addEventListener("click",function(){
    document.getElementsByClassName("main_container")[0].classList.add("active");
  });
  
  document.getElementById("del-dismiss-popup-btn").addEventListener("click",function(){
    document.getElementsByClassName("main_container")[0].classList.remove("active");
  });