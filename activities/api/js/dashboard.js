


function filterProjects(input){
  let val = input.value.toLowerCase();
  document.querySelectorAll(".list-group-item").forEach(el=>{
    el.style.display = el.innerText.toLowerCase().includes(val) ? "" : "none";
  });
}


function addServiceInstant(){

  let name = document.getElementById("serviceName").value.trim();
  let selectedCategory = document.getElementById("categorySelect").value;
  let newCategory = document.getElementById("newCategory").value.trim();

  let category = newCategory || selectedCategory;

  if(!name || !category){
    alert("Enter category and service");
    return;
  }

  fetch("/api/projects/add-service/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie('csrftoken')
    },
    body: JSON.stringify({
      name,
      category,
      project_id: "{{ selected_project.id }}"
    })
  })
  .then(res => res.json())
  .then(data => {

    if(data.success){
      location.reload(); 
    }else{
      alert(data.error);
    }

  });
}


function getCookie(name){
  let value = null;
  document.cookie.split(';').forEach(c=>{
    c = c.trim();
    if(c.startsWith(name + '=')){
      value = decodeURIComponent(c.substring(name.length + 1));
    }
  });
  return value;
}

