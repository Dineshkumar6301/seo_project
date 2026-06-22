let selectedProject = null;
let selectedService = null;
let selectedModule = null;
let selectedChecklist = null;
let selectedCategory = null;

/* ==========================
PROJECT
========================== */

async function selectProject(projectId, el){

selectedProject = projectId;

document.querySelectorAll(".project-item")
    .forEach(x => x.classList.remove("project-active"));

el.classList.add("project-active");

const response = await fetch(
    `/activities/api/project-services/${projectId}/`
);

const services = await response.json();

renderCategories(services);
}

/* ==========================
SERVICES
========================== */


let categoryServices = {};

function renderCategories(services){

    categoryServices = {};

    services.forEach(service => {

        const category =
            service.category_name || "Others";

        if(!categoryServices[category]){
            categoryServices[category] = [];
        }

        categoryServices[category].push(service);
    });

    let html = "";

    Object.keys(categoryServices).forEach(category => {

        html += `
            <button
                type="button"
                class="btn btn-outline-dark m-1 category-btn"
                onclick="selectCategory('${category}', this)">

                ${category}
            </button>
        `;
    });

    document.getElementById(
        "categoryContainer"
    ).innerHTML = html;
}


function selectCategory(category, el){

    selectedCategory = category;

    document.querySelectorAll(".category-btn")
        .forEach(btn => {

            btn.classList.remove("btn-dark");
            btn.classList.add("btn-outline-dark");
        });

    el.classList.remove("btn-outline-dark");
    el.classList.add("btn-dark");

    renderServices(
        categoryServices[category]
    );
}
function renderServices(services){

    let html = "";

    services.forEach(service => {

        const active =
            selectedService == service.id
            ? "btn-primary"
            : "btn-outline-primary";

        html += `
            <button
                type="button"
                class="btn ${active} m-1 service-btn"
                onclick="selectService(${service.id}, this)">

                ${service.name}

            </button>
        `;
    });

    document.getElementById(
        "servicesContainer"
    ).innerHTML = html;

    document.getElementById(
        "taskTypes"
    ).innerHTML = "";

    document.getElementById(
        "dynamicForm"
    ).innerHTML = "";
}

/* ==========================
MODULES
========================== */

async function selectService(
serviceId,
el
){


selectedService = serviceId;

document.querySelectorAll(".service-btn")
    .forEach(btn => {

        btn.classList.remove(
            "btn-primary"
        );

        btn.classList.add(
            "btn-outline-primary"
        );
    });

el.classList.remove(
    "btn-outline-primary"
);

el.classList.add(
    "btn-primary"
);

const response = await fetch(
    `/activities/api/service-modules/${serviceId}/`
);

const modules = await response.json();

renderModules(modules);


}

function renderModules(modules){

    let html = "";

    modules.forEach(module => {

        const active =
            selectedModule == module.id
            ? "btn-success"
            : "btn-outline-success";

        html += `
            <button
                type="button"
                class="btn ${active} m-1 module-btn"
                onclick="selectModule(${module.id}, this)">

                ${module.name}

            </button>
        `;
    });

    document.getElementById(
        "taskTypes"
    ).innerHTML = html;

    document.getElementById(
        "dynamicForm"
    ).innerHTML = "";
}

async function selectModule(
moduleId,
el
){


selectedModule = moduleId;

document.querySelectorAll(".module-btn")
    .forEach(btn => {

        btn.classList.remove(
            "btn-success"
        );

        btn.classList.add(
            "btn-outline-success"
        );
    });

el.classList.remove(
    "btn-outline-success"
);

el.classList.add(
    "btn-success"
);

const response = await fetch(
    `/activities/api/checklist-items/${moduleId}/`
);

const checklists = await response.json();

renderChecklists(checklists);


}

function renderChecklists(checklists){

    let html = `
        <h5 class="mb-3">
            Checklist Tasks
        </h5>
    `;

    checklists.forEach(task => {

        const active =
            selectedChecklist == task.id
            ? "border-primary"
            : "";

        html += `
            <div
                class="card p-2 mb-2 checklist-card ${active}"
                style="cursor:pointer"
                onclick="selectChecklist(${task.id})">

                ${task.item}

            </div>
        `;
    });

    document.getElementById(
        "dynamicForm"
    ).innerHTML = html;
}
/* ==========================
FORM
========================== */

async function selectChecklist(checklistId){

    selectedChecklist = checklistId;

    const response = await fetch(
        `/activities/api/task-fields/${checklistId}/`
    );

    const fields = await response.json();

    console.log(fields);

    renderDynamicFields(fields);
}

function renderDynamicFields(fields){
    window.currentFields = fields;

    let html = `

        <h5 class="mb-3">
            Activity Details
        </h5>

    `;

    fields.forEach(field => {

        if(field.field_type === "textarea"){

            html += `
                <div class="mb-3">

                    <label class="form-label">
                        ${field.label}
                    </label>

                    <textarea
                        id="field_${field.id}"
                        class="form-control"
                        rows="3"></textarea>

                </div>
            `;
        }

        else if(field.field_type === "number"){

            html += `
                <div class="mb-3">

                    <label class="form-label">
                        ${field.label}
                    </label>

                    <input
                        type="number"
                        id="field_${field.id}"
                        class="form-control">

                </div>
            `;
        }

        else if(field.field_type === "url"){

            html += `
                <div class="mb-3">

                    <label class="form-label">
                        ${field.label}
                    </label>

                    <input
                        type="url"
                        id="field_${field.id}"
                        class="form-control">

                </div>
            `;
        }

        else{

            html += `
                <div class="mb-3">

                    <label class="form-label">
                        ${field.label}
                    </label>

                    <input
                        type="text"
                        id="field_${field.id}"
                        class="form-control">

                </div>
            `;
        }

    });

    html += `

        <div class="mb-3">

            <label class="form-label">
                Hours
            </label>

            <input
                type="number"
                step="0.5"
                id="hours"
                class="form-control">

        </div>

        
        <button
            type="button"
            class="btn btn-success w-100"
            onclick="saveActivity()">

            Save Activity

        </button>

    `;

    document.getElementById(
        "dynamicForm"
    ).innerHTML = html;
}
/* ==========================
SAVE
========================== */

async function saveActivity(){
    if(!selectedChecklist){

    alert(
        "Please select a task."
    );

    return;
}

    try{

        const payload = {

            activity_id: editActivityId,

            project: selectedProject,

            service: selectedService,

            module: selectedModule,

            checklist: selectedChecklist,

            hours: document.getElementById(
                "hours"
            )?.value || "",

            dynamic_data: {}
        };

        (window.currentFields || []).forEach(field => {

            const element =
                document.getElementById(
                    `field_${field.id}`
                );

             payload.dynamic_data[
                field.name
            ] = element
                ? element.value
                : "";
        });

        console.log(payload);

        const response = await fetch(
            "/activities/api/save-activity/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie(
                        "csrftoken"
                    )
                },

                body: JSON.stringify(
                    payload
                )
            }
        );

        const data =
            await response.json();

        console.log(data);

        if(data.success){

            alert(
                editActivityId
                ? "Activity Updated Successfully"
                : "Activity Saved Successfully"
            );

           editActivityId = null;

            clearFormFields();

            loadData();

            setTimeout(() => {

                restoreCategoryActive();

            }, 100);

        }else{

            alert(
                data.error ||
                "Failed to Save"
            );
        }

    }catch(error){

        console.error(error);

        alert(
            "Something went wrong."
        );
    }
}

console.log(
    "Selected Category:",
    selectedCategory
);
function restoreCategoryActive() {

    document
        .querySelectorAll(".category-btn")
        .forEach(btn => {

            if (
                btn.textContent.trim() === selectedCategory
            ) {

                btn.classList.remove(
                    "btn-outline-dark"
                );

                btn.classList.add(
                    "btn-dark"
                );
            }
        });
}

function clearFormFields(){

    (window.currentFields || []).forEach(field => {

        const element =
            document.getElementById(
                `field_${field.id}`
            );

        if(element){

            element.value = "";
        }

    });

    const hours =
        document.getElementById(
            "hours"
        );

    if(hours){

        hours.value = "";
    }

}

async function loadSavedActivities(){

    const response = await fetch(
        "/activities/api/list/?filter=today"
    );

    const rows = await response.json();

    document.getElementById(
        "tableHead"
    ).innerHTML = `
        <th>Date</th>
        <th>Project</th>
        <th>Service</th>
        <th>Task</th>
        <th>Keyword</th>
        <th>Target URL</th>
        <th>Submitted URL</th>
        <th>Other Data</th>
        <th>Hours</th>
        <th>Action</th>

    `;

    let html = "";

    rows.forEach(row => {

        html += `
            <tr>

                <td>${row.date}</td>

                <td>${row.project_name}</td>

                <td>${row.service_name}</td>

                <td>${row.task_type}</td>

                <td>${row.dynamic_data?.Keyword || ""}</td>

                <td>${row.dynamic_data?.Target_url || ""}</td>

                <td>${row.dynamic_data?.Submitted_url || ""}</td>

                <td>${row.dynamic_data?.hours || ""}</td>

                <td>
                    <button
                        class="btn btn-primary btn-sm"
                        onclick="editActivity(${row.id})">

                        Edit
                    </button>
                </td>

            </tr>
        `;
    });

    document.getElementById(
        "tableBody"
    ).innerHTML = html;
}



function handleFilterChange(){

    const filter =
        document.getElementById(
            "filterType"
        ).value;

    document.getElementById(
        "startBox"
    ).style.display =
        filter === "custom"
        ? "block"
        : "none";

    document.getElementById(
        "endBox"
    ).style.display =
        filter === "custom"
        ? "block"
        : "none";
}


/* ==========================
LOAD TABLE
========================== */

async function loadData(){

    const filter =
        document.getElementById(
            "filterType"
        ).value;

    const start =
        document.getElementById(
            "startDate"
        )?.value || "";

    const end =
        document.getElementById(
            "endDate"
        )?.value || "";

    let url =
        `/activities/api/list/?filter=${filter}&start=${start}&end=${end}`;

    if(selectedProject){

        url += `&project=${selectedProject}`;
    }

    const response =
        await fetch(url);

    const rows =
        await response.json();

    document.getElementById(
        "tableHead"
    ).innerHTML = `
    <tr>
        <th>Date</th>
        <th>Project</th>
        <th>Service</th>
        <th>Task</th>
        <th>Keyword</th>
        <th>Target URL</th>
        <th>Submitted URL</th>
        <th>Hours</th>
        <th>Other Data</th>
        <th>Action</th>
    </tr>
    `;

    let html = "";

    rows.forEach(row => {

        let otherData = "";

        Object.entries(
            row.dynamic_data || {}
        ).forEach(([key, value]) => {

            if(
                ![
                    "Keyword",
                    "keyword",
                    "Target_url",
                    "target_url",
                    "Submitted_url",
                    "submitted_url",
                    "hours",
                    "module"
                ].includes(key)
            ){

                otherData += `
                    <div class="mb-1">
                        <strong>${key}</strong> :
                        ${value ?? ""}
                    </div>
                `;
            }
        });

        if(otherData === ""){
            otherData = "-";
        }

    
        html += `
        <tr>

            <td>${row.date || ""}</td>

            <td>${row.project_name || ""}</td>

            <td>${row.service_name || ""}</td>

            <td>${row.task_type || ""}</td>

            <td>${row.dynamic_data?.Keyword || ""}</td>

            <td>
                ${
                    row.dynamic_data?.Target_url
                    ?
                    `<a
                        href="${row.dynamic_data.Target_url}"
                        target="_blank">

                        ${row.dynamic_data.Target_url}

                    </a>`
                    : ""
                }
            </td>

            <td>
                ${
                    (row.dynamic_data?.Submitted_url || "")
                    .split(",")
                    .map(link => link.trim())
                    .filter(link => link)
                    .map(link => `
                        <div>
                            <a
                                href="${link}"
                                target="_blank">

                                ${link}

                            </a>
                        </div>
                    `)
                    .join("")
                }
            </td>

            <td>${row.dynamic_data?.hours || ""}</td>

            <td>${otherData}</td>

            <td>
                <button
                    class="btn btn-primary btn-sm"
                    onclick="editActivity(${row.id})">

                    Edit

                </button>
            </td>

        </tr>
        `;
    });

    document.getElementById(
        "tableBody"
    ).innerHTML = html;
}



function downloadExcel(){

    window.open(
        "/activities/api/export/",
        "_blank"
    );
}


/* ==========================
INITIAL LOAD
========================== */

document.addEventListener(
    "DOMContentLoaded",
    function(){

        loadData();
    }
);
function getCookie(name){


let cookieValue = null;

if(document.cookie){

    const cookies =
        document.cookie.split(";");

    for(let cookie of cookies){

        cookie = cookie.trim();

        if(
            cookie.startsWith(
                name + "="
            )
        ){

            cookieValue =
                decodeURIComponent(
                    cookie.substring(
                        name.length + 1
                    )
                );

            break;
        }
    }
}

return cookieValue;


}

let editActivityId = null;

async function editActivity(id){

    try{

        const response = await fetch(
            `/activities/api/detail/${id}/`
        );

        const data =
            await response.json();

        if(!data.success){

            alert(
                data.error ||
                "Activity not found"
            );

            return;
        }

        editActivityId = id;

        window.editData =
            data.dynamic_data || {};

        selectedProject =
            data.project_id;
            document
    .querySelectorAll(
        ".project-item"
    )
    .forEach(item => {

        item.classList.remove(
            "project-active"
        );

        const onclick =
            item.getAttribute(
                "onclick"
            );

        if(
            onclick &&
            onclick.includes(
                `(${data.project_id},`
            )
        ){

            item.classList.add(
                "project-active"
            );
        }
    });

        selectedService =
            data.service_id;

        selectedModule =
            data.module_id;

        selectedChecklist =
            data.checklist_id;

        const servicesResponse =
            await fetch(
                `/activities/api/project-services/${data.project_id}/`
            );

        const services =
            await servicesResponse.json();

        renderCategories(
            services
        );
        selectedCategory =
            null;

        services.forEach(service => {

            if(
                service.id ==
                data.service_id
            ){

                selectedCategory =
                    service.category_name;
            }
        });

        
        
        if(selectedCategory){

            renderServices(
                categoryServices[
                    selectedCategory
                ]
            );
        }

        const modulesResponse =
            await fetch(
                `/activities/api/service-modules/${data.service_id}/`
            );

        const modules =
            await modulesResponse.json();

        renderModules(
            modules
        );

        const checklistsResponse =
            await fetch(
                `/activities/api/checklist-items/${data.module_id}/`
            );

        const checklists =
            await checklistsResponse.json();

        renderChecklists(
            checklists
        );

        const fieldsResponse =
            await fetch(
                `/activities/api/task-fields/${data.checklist_id}/`
            );

        const fields =
            await fieldsResponse.json();

        renderDynamicFields(
            fields
        );

        setTimeout(() => {

            fields.forEach(field => {

                const input =
                    document.getElementById(
                        `field_${field.id}`
                    );

                if(
                    input &&
                    window.editData[
                        field.name
                    ] !== undefined
                ){

                    input.value =
                        window.editData[
                            field.name
                        ];
                }
            });

            const hoursInput =
                document.getElementById(
                    "hours"
                );

            if(hoursInput){

                hoursInput.value =
                    window.editData.hours || "";
            }

        }, 200);

        window.scrollTo({

            top: 0,

            behavior: "smooth"
        });

    }catch(error){

        console.error(error);

        alert(
            "Failed to load activity."
        );
    }
}


function clearProject(el){

    selectedProject = null;
    selectedService = null;
    selectedModule = null;
    selectedChecklist = null;

    document.querySelectorAll(".project-item")
        .forEach(x =>
            x.classList.remove("project-active")
        );

    el.classList.add(
        "project-active"
    );

    document.getElementById(
        "categoryContainer"
    ).innerHTML = "";

    document.getElementById(
        "servicesContainer"
    ).innerHTML = "";

    document.getElementById(
        "taskTypes"
    ).innerHTML = "";

    document.getElementById(
        "dynamicForm"
    ).innerHTML = "";

    loadData();
}