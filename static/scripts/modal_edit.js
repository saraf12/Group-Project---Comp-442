
  document.getElementById("edit-open-popup-btn").addEventListener("click",function(){
    document.getElementsByClassName("num_container")[0].classList.add("active");
  });
  
  document.getElementById("edit-dismiss-popup-btn").addEventListener("click",function(){
    document.getElementsByClassName("num_container")[0].classList.remove("active");
  });