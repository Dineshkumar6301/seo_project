

/* columns that should display FULL (no truncation) */
const FULL_COLS = ['url', 'submitted_url'];

/* max chars for all other columns */
const TRUNC_LEN = 30;

let fullData = {};

let selectedProject = null;
let selectedCategory = null;
let selectedService = null;
let selectedTask = null;

let currentPage = 1;
const rowsPerPage = 10;

async function selectProject(projectId, el = null){

    selectedProject = projectId;

    document.querySelectorAll(".project-item")
        .forEach(e => e.classList.remove("project-active"));

    // prevent undefined error
    if(el){
        el.classList.add("project-active");
    }

    resetUI();

    try{

        fullData = {};

        let res = await fetch(
            `/activities/api/project-services/${selectedProject}/`
        );

        fullData = await res.json();

        renderCategories(false);

        await loadDataFast();

    }catch(err){

        console.log(err);

        alert("Error loading services");
    }
}
async function clearProject(el){

    selectedProject = null;

    selectedCategory = null;

    selectedService = null;

    selectedTask = null;

    editId = null;

    fullData = {};

    document.querySelectorAll(".project-item")
        .forEach(e => e.classList.remove("project-active"));

    el.classList.add("project-active");

    resetUI();

    await loadDataFast();
}

function resetUI(){

    document.getElementById(
        "categoriesContainer"
    ).innerHTML = "";

    document.getElementById(
        "servicesContainer"
    ).innerHTML = "";

    document.getElementById(
        "taskTypes"
    ).innerHTML = "";

    document.querySelectorAll(
        "#dynamicForm input, #dynamicForm textarea, #dynamicForm select"
    ).forEach(el => {

        if(el.type !== "button"){
            el.value = "";
        }
    });
    selectedCategory = null;
    selectedService = null;
    selectedTask = null;
}



function renderCategories(autoSelect = true){

    let c = document.getElementById(
        "categoriesContainer"
    );

    c.innerHTML = "";

    Object.keys(fullData)
    .sort((a, b) => a.localeCompare(b))
    .forEach(category => {

        c.innerHTML += `
        <span
            class="service-badge category-badge"
            onclick="selectCategory('${category}', this)">

            ${category}

        </span>`;
    });

    if(autoSelect){

        let firstCategory = Object.keys(fullData)[0];

        if(firstCategory){

            selectCategory(
                firstCategory,
                document.querySelector(".category-badge")
            );
        }
    }
}

function selectCategory(category, el){

    selectedCategory = category;

    document.querySelectorAll(".category-badge")
        .forEach(e =>
            e.classList.remove("active-category")
        );

    el.classList.add("active-category");

    let servicesBox = document.getElementById(
        "servicesContainer"
    );

    servicesBox.innerHTML = "";

    let services = fullData[category];

    Object.keys(services)
    .sort((a, b) => a.localeCompare(b))
    .forEach(service => {
    
        servicesBox.innerHTML += `
        <span
            class="service-badge"
            onclick="selectService('${service}', this)">

            ${service}

        </span>`;
    });

    document.getElementById(
        "taskTypes"
    ).innerHTML = "";

    document.getElementById(
        "dynamicForm"
    ).innerHTML = "";
}
function selectService(service, el){

    selectedService = service;

    document.querySelectorAll(".service-badge")
        .forEach(e => {

            e.classList.remove("active-service");

            e.style.background = "";
            e.style.color = "";
            e.style.borderColor = "";
        });

    if(el){

        el.classList.add("active-service");

        el.style.background = "#2563eb";
        el.style.color = "#fff";
        el.style.borderColor = "#2563eb";
    }

    let taskBox = document.getElementById(
        "taskTypes"
    );

    taskBox.innerHTML = "";

    let tasks =
        fullData[selectedCategory][service];

    Object.keys(tasks)
    .sort((a, b) => a.localeCompare(b))
    .forEach(task => {

        taskBox.innerHTML += `
        <button
            type="button"
            class="btn btn-outline-primary m-1 task-btn"
            onclick="selectTask('${task}', this)">

            ${task}

        </button>`;
    });

    document.getElementById(
        "dynamicForm"
    ).innerHTML = "";
}
function selectTask(task, el){

    selectedTask = task;

    document.querySelectorAll(".task-btn")
        .forEach(btn => {

            btn.classList.remove("btn-primary");

            btn.classList.add("btn-outline-primary");
        });

    if(el){

        el.classList.remove("btn-outline-primary");

        el.classList.add("btn-primary");
    }

    let form = document.getElementById(
        "dynamicForm"
    );

    form.innerHTML = "";

    let fields =
        fullData[selectedCategory]
                [selectedService]
                [task];

    fields.forEach(field => {

        let input = "";

        /* TEXTAREA */
        if(field.field_type === "textarea"){

            input = `
            <textarea
                class="form-control"
                name="${field.name}">
            </textarea>`;
        }

        /* SELECT */
        else if(field.field_type === "select"){

            input = `
            <select
                class="form-control"
                name="${field.name}">

                ${(field.options || [])
                    .map(o => `
                        <option value="${o}">
                            ${o}
                        </option>
                    `).join("")}

            </select>`;
        }

        /* FILE */
        else if(field.field_type === "file"){

            input = `
            <input
                type="file"
                class="form-control"
                name="${field.name}">
            `;
        }

        /* NORMAL */
        else{

            input = `
            <input
                type="${field.field_type || 'text'}"
                class="form-control"
                name="${field.name}">
            `;
        }

        form.innerHTML += `
        <div class="mb-3">

            <label>
                ${field.label}
            </label>

            ${input}

        </div>`;
    });

    form.innerHTML += `
    <button
        type="button"
        class="btn btn-success w-100"
        onclick="saveData()">

        Save

    </button>`;
}

async function deleteRow(id){

    if(!confirm("Are you sure you want to delete this entry?")){
        return;
    }

    try{

        let res = await fetch(
            `/activities/api/delete/${id}/`,
            {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCSRF()
                }
            }
        );

        let result = await res.json();

        if(result.error){
            alert(result.error);
            return;
        }

        await loadDataFast();

    }catch(err){

        console.log(err);
        alert("Delete failed");
    }
}


async function loadData(){

    let url = `/activities/api/list/?`;

    if(selectedProject){
        url += `project=${selectedProject}&`;
    }

    let filterType =
        document.getElementById("filterType").value;

    let startDate =
        document.getElementById("startDate").value;

    let endDate =
        document.getElementById("endDate").value;

    url += `filter=${filterType}&`;
    url += `start=${startDate}&`;
    url += `end=${endDate}`;

    try{

        let res = await fetch(url);
        let data = await res.json();
        renderTable(data);

    }catch(err){

        console.log(err);
        alert("Error loading table");
    }
}


function renderTable(data){

    let head       = document.getElementById("tableHead");
    let body       = document.getElementById("tableBody");
    let pagination = document.getElementById("paginationContainer");

    if(!data.length){

        head.innerHTML = "";

        body.innerHTML = `
        <tr>
            <td colspan="20">
                <div class="empty-box">
                    No activities found
                </div>
            </td>
        </tr>`;

        pagination.innerHTML = "";

        return;
    }

    /* =========================
       TABLE HEAD
    ========================== */

    head.innerHTML = `
        <th>S.no</th>
        <th>Project</th>
        <th>Category</th>
        <th>Service</th>
        <th>Task</th>
        <th>Keyword</th>
        <th>Submitted URL</th>
        <th>Target URL</th>
        <th style="min-width:400px;">Other Data</th>
        <th>Action</th>
    `;

    /* =========================
       PAGINATION
    ========================== */

    let start         = (currentPage - 1) * rowsPerPage;
    let end           = start + rowsPerPage;
    let paginatedData = data.slice(start, end);

    body.innerHTML = "";

    /* =========================
       TABLE BODY
    ========================== */

    paginatedData.forEach((r, index) => {

        let rowData = r.data || {};

        /* =========================
           KEYWORD
        ========================== */

        let keyword =
            rowData.KEYWORD ||
            rowData.keyword ||
            rowData.Keyword ||
            "-";

        /* =========================
           SUBMITTED URL
        ========================== */

        let submitted =
            rowData.SUBMITTED_URL ||
            rowData.submitted_url ||
            rowData.Submitted_url ||
            "";

        let submittedHTML = "-";

        if(submitted){

            submittedHTML = String(submitted)
            .split(/[\n,]+/)
            .filter(x => x.trim())
            .map(link => `

                <div class="mb-1">

                    <a href="${link.trim()}"
                       target="_blank"
                       style="
                         color:#2563eb;
                         text-decoration:none;
                         display:block;
                         max-width:220px;
                         white-space:nowrap;
                         overflow:hidden;
                         text-overflow:ellipsis;
                       ">

                        ${link.trim()}

                    </a>

                </div>

            `).join("");
        }

        /* =========================
           TARGET URL
        ========================== */

        let target =
            rowData.Target_url ||
            rowData.target_url ||
            "";

        let targetHTML = "-";

        if(target){

            targetHTML = String(target)
            .split(/[\n,]+/)
            .filter(x => x.trim())
            .map(link => `

                <div class="mb-1">

                    <a href="${link.trim()}"
                       target="_blank"
                       style="
                         color:#059669;
                         text-decoration:none;
                         display:block;
                         max-width:220px;
                         white-space:nowrap;
                         overflow:hidden;
                         text-overflow:ellipsis;
                       ">

                        ${link.trim()}

                    </a>

                </div>

            `).join("");
        }

        /* =========================
           OTHER DATA
        ========================== */

        let otherHTML = "";

        Object.entries(rowData).forEach(([key, value]) => {

            let lower = key.toLowerCase();

            /* skip separate columns */
            if(
                lower === "keyword" ||
                lower === "submitted_url" ||
                lower === "target_url"
            ){
                return;
            }

            if(value === null || value === ""){
                return;
            }

            otherHTML += `

                <div style="
                    margin-bottom:8px;
                    padding:8px 10px;
                    background:#f8fafc;
                    border:1px solid #e2e8f0;
                    border-radius:8px;
                    font-size:13px;
                ">

                    <strong style="
                        display:block;
                        margin-bottom:4px;
                        color:#334155;
                    ">

                        ${formatLabel(key)}

                    </strong>

                    <div style="
                        color:#0f172a;
                        word-break:break-word;
                        white-space:normal;
                    ">

                        ${value}

                    </div>

                </div>
            `;
        });

        if(!otherHTML){
            otherHTML = "-";
        }

        /* =========================
           FINAL ROW
        ========================== */

        body.innerHTML += `

        <tr>

            <td>${start + index + 1}</td>

            <td>${r.project_name || ""}</td>

            <td>${r.category || ""}</td>

            <td>${r.service_name || r.service || ""}</td>

            <td>${r.task_type || r.task || ""}</td>

            <td style="min-width:180px;">
                ${keyword}
            </td>

            <td class="col-url">
                ${submittedHTML}
            </td>

            <td class="col-url">
                ${targetHTML}
            </td>

            <td style="
                min-width:420px;
                max-width:520px;
            ">
                ${otherHTML}
            </td>

            <td>

                <div class="d-flex gap-1">

                    <button
                        class="btn btn-sm btn-primary"
                        onclick="editRow(${r.id})">

                        ✏️

                    </button>

                    <button
                        class="btn-delete"
                        onclick="deleteRow(${r.id})">

                        🗑

                    </button>

                </div>

            </td>

        </tr>
        `;
    });

    /* =========================
       PAGINATION BUTTONS
    ========================== */

    let totalPages = Math.ceil(
        data.length / rowsPerPage
    );

    pagination.innerHTML = "";

    for(let i = 1; i <= totalPages; i++){

        pagination.innerHTML += `

        <button
            class="btn btn-sm pagination-btn
            ${i === currentPage
                ? 'btn-primary'
                : 'btn-outline-primary'}"

            onclick="changePage(${i})">

            ${i}

        </button>
        `;
    }
}
function changePage(page){

    currentPage = page;

    loadData();
}

function formatLabel(text){

    return text
        .replaceAll("_", " ")
        .replace(/\b\w/g, l => l.toUpperCase());
}



function handleFilterChange(){

    let type = document.getElementById("filterType").value;

    if(type === "custom"){

        document.getElementById("startBox").style.display = "block";
        document.getElementById("endBox").style.display   = "block";

    }else{

        document.getElementById("startBox").style.display = "none";
        document.getElementById("endBox").style.display   = "none";
    }
}


function downloadExcel(){

    let filterType =
        document.getElementById("filterType").value;

    let startDate =
        document.getElementById("startDate").value;

    let endDate =
        document.getElementById("endDate").value;

    let url = `/activities/api/export/?export_type=daily&`;

    /* PROJECT */
    if(selectedProject){
        url += `project=${selectedProject}&`;
    }

    /* CATEGORY */
    if(selectedCategory){
        url += `category=${selectedCategory}&`;
    }

    /* SERVICE */
    if(selectedService){
        url += `service=${selectedService}&`;
    }

    /* TASK */
    if(selectedTask){
        url += `task=${selectedTask}&`;
    }

    /* FILTERS */
    url += `filter=${filterType}&`;

    url += `start=${startDate}&`;

    url += `end=${endDate}`;

    window.open(url, "_blank");
}

let editId = null;
async function editRow(id){

    try{

        const response = await fetch(
            `/activities/api/detail/${id}/`
        );

        const data = await response.json();

        console.log("EDIT DATA:", data);

        if(!data.success){

            alert("Activity not found");
            return;
        }

        editId = id;

        currentPage = 1;

        selectedProject  = data.project;
        selectedCategory = data.category;
        selectedService  = data.service_name || data.service;
        selectedTask     = data.task_type || data.task;

        document.querySelectorAll(".project-item")
            .forEach(e => {

                e.classList.remove("project-active");

                if(
                    e.getAttribute("onclick")
                    ?.includes(`(${selectedProject},`)
                ){
                    e.classList.add("project-active");
                }
            });
        const serviceResponse = await fetch(
            `/activities/api/project-services/${selectedProject}/`
        );

        fullData = await serviceResponse.json();
        renderCategories(false);
        const categoryEl =
            [...document.querySelectorAll(".category-badge")]
            .find(el =>
                el.innerText.trim() === selectedCategory
            );

        if(categoryEl){

            selectCategory(
                selectedCategory,
                categoryEl
            );
        }
        const serviceEl =
                [...document.querySelectorAll("#servicesContainer .service-badge")]
                .find(el =>
                    el.innerText.trim() === selectedService
                );

            if(serviceEl){

                selectService(
                    selectedService,
                    serviceEl
                );
            }

            await new Promise(resolve =>
                setTimeout(resolve, 50)
            );

            const taskEl =
                [...document.querySelectorAll(".task-btn")]
                .find(el =>
                    el.innerText.trim() === selectedTask
                );

            if(taskEl){

                selectTask(
                    selectedTask,
                    taskEl
                );
            }
        await new Promise(resolve =>
            setTimeout(resolve, 50)
        );
        const dynamicData =
            data.dynamic_data || {};

        Object.keys(dynamicData).forEach(key => {

            const normalizedKey = key.toLowerCase();

            const field = [...document.querySelectorAll(
                "#dynamicForm input, #dynamicForm textarea, #dynamicForm select"
            )].find(el =>
                el.name.toLowerCase() === normalizedKey
            );

            if(field){

                field.value = dynamicData[key];
            }
        });
        const btn = document.querySelector(
            "#dynamicForm button"
        );

        if(btn){

            btn.innerText = "Update";

            btn.classList.remove("btn-success");

            btn.classList.add("btn-primary");
        }
       const tableWrapper = document.querySelector(".table-scroll-wrapper");

        if(tableWrapper){

            tableWrapper.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }


    }
    catch(error){

        console.log(error);

        alert("Failed to load edit data");
    }
}


async function saveData(){

    if(!selectedProject){
        alert("Select Project");
        return;
    }

    if(!selectedCategory){
        alert("Select Category");
        return;
    }

    if(!selectedService){
        alert("Select Service");
        return;
    }

    if(!selectedTask){
        alert("Select Task");
        return;
    }

    let payload = {

        project: selectedProject,

        category: selectedCategory,

        service_name: selectedService,

        task_type: selectedTask,
        date: new Date().toISOString().split('T')[0],

        dynamic_data: {}
    };

    let inputs = document.querySelectorAll(
        "#dynamicForm input, #dynamicForm textarea, #dynamicForm select"
    );

    inputs.forEach(i => {

        if(i.type === "file"){

            payload.dynamic_data[i.name] =
                i.files[0]
                ? i.files[0].name
                : "";

        }else{

            payload.dynamic_data[i.name] = i.value;
        }
    });

    try{

        let url = "/activities/api/upsert/";
        let method = "POST";

        if(editId){

            url = `/activities/api/update/${editId}/`;
            method = "PUT";
        }

        const res = await fetch(url, {

            method: method,

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRF()
            },

            body: JSON.stringify(payload)
        });

        const result = await res.json();

        console.log(result);

        if(result.error){

            alert(result.error);
            return;
        }

        showToast(
            editId
            ? "Updated Successfully"
            : "Saved Successfully"
        );

        editId = null;

        currentPage = 1;

        await loadDataFast();

        document.querySelectorAll(
    "#dynamicForm input, #dynamicForm textarea, #dynamicForm select"
            ).forEach(el => {

                if(el.type !== "button"){
                    el.value = "";
                }
            });
    
        const btn = document.querySelector(
            '#dynamicForm button'
        );

        if(btn){

            btn.innerText = "Save";

            btn.classList.remove("btn-primary");
            btn.classList.add("btn-success");
        }

    }
    catch(err){

        console.log(err);

        alert("Save failed");
    }
}


let cachedTableData = [];

async function loadDataFast(){

    let url = `/activities/api/list/?`;

    if(selectedProject){
        url += `project=${selectedProject}&`;
    }

    let filterType =
        document.getElementById("filterType").value;

    let startDate =
        document.getElementById("startDate").value;

    let endDate =
        document.getElementById("endDate").value;

    url += `filter=${filterType}&`;
    url += `start=${startDate}&`;
    url += `end=${endDate}`;

    try{

        const res = await fetch(url);

        cachedTableData = await res.json();

        renderTable(cachedTableData);

    }catch(err){

        console.log(err);
    }
}
function getCSRF(){

    return document.cookie
        .split('; ')
        .find(r => r.startsWith('csrftoken'))
        ?.split('=')[1];
}

function showToast(message){

    let toast = document.createElement("div");

    toast.innerText = message;

    toast.style.position = "fixed";
    toast.style.top = "20px";
    toast.style.right = "20px";
    toast.style.background = "#198754";
    toast.style.color = "#fff";
    toast.style.padding = "12px 18px";
    toast.style.borderRadius = "10px";
    toast.style.zIndex = "99999";
    toast.style.fontWeight = "600";
    toast.style.boxShadow = "0 6px 20px rgba(0,0,0,.15)";

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 2500);
}
