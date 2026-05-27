
let currentPage = 1;
let dateFilter = "{{ date_filter|default:'all' }}";
let statusFilter = "{{ current_status|default:'' }}";
let searchTimer = null;


function getFilters() {

    const start =
        document.getElementById("startDate")?.value;

    const end =
        document.getElementById("endDate")?.value;

    if (
        (start && !end)
        ||
        (!start && end)
    ) {

        alert(
            "Please select both start and end date"
        );

        return null;
    }

    const useRange = start && end;

    if (useRange) {

        document
            .querySelectorAll(
                ".filter-group .pill"
            )
            .forEach(p => {

                p.classList.remove(
                    "active"
                );
            });
    }

    return {

        type:
            useRange
            ? ""
            : dateFilter,

        status: statusFilter,

        search:
            document.getElementById(
                "searchInput"
            )?.value || "",

        project:
            document.getElementById(
                "projectFilter"
            )?.value || "",

        start_date: start,

        end_date: end,

        page: currentPage,

        limit: 20
    };
}

function buildQuery(params) {

    return Object.entries(params)

        .filter(
            ([, v]) =>
                v !== ""
                &&
                v !== null
                &&
                v !== undefined
        )

        .map(
            ([k, v]) =>
                `${k}=${encodeURIComponent(v)}`
        )

        .join("&");
}


function setStatusFilter(val) {

    if (statusFilter === val) {

        statusFilter = "";

    } else {

        statusFilter = val;
    }

    currentPage = 1;

    document
        .querySelectorAll(".stat-card")
        .forEach(c => {

            c.classList.remove(
                "active-filter"
            );
        });

    if (statusFilter) {

        document
            .querySelector(
                `.stat-card.${statusFilter}`
            )
            ?.classList.add(
                "active-filter"
            );
    }

    loadDashboard();
}


function setDateFilter(e, val) {

    dateFilter = val;

    currentPage = 1;

    document.getElementById(
        "startDate"
    ).value = "";

    document.getElementById(
        "endDate"
    ).value = "";

    document
        .querySelectorAll(
            ".filter-group .pill"
        )
        .forEach(p => {

            p.classList.remove(
                "active"
            );
        });

    e.currentTarget.classList.add(
        "active"
    );

    loadDashboard();
}


function loadDashboard() {

    const filters = getFilters();

    if (!filters) return;

    const query =
        buildQuery(filters);

    document
        .getElementById(
            "loadingBar"
        )
        .classList.add(
            "active"
        );

    fetch(
        `/activities/api/dashboard/?${query}`
    )

    .then(res => res.json())

    .then(data => {

        document
            .getElementById(
                "loadingBar"
            )
            .classList.remove(
                "active"
            );

        updateKPIs(data.kpi);

        updateTable(data.table);

        updateMobileCards(data.table);

        updatePagination(
            data.pagination
        );
    })

    .catch(err => {

        console.log(err);

        document
            .getElementById(
                "loadingBar"
            )
            .classList.remove(
                "active"
            );
    });
}

function updateKPIs(kpi) {

    if (!kpi) return;

    document.getElementById(
        "kpi-pending"
    ).textContent =
        kpi.pending ?? "—";

    document.getElementById(
        "kpi-approved"
    ).textContent =
        kpi.approved ?? "—";

    document.getElementById(
        "kpi-rejected"
    ).textContent =
        kpi.rejected ?? "—";
}

function updateTable(rows) {

    const tbody =
        document.getElementById(
            "taskTable"
        );

    const thead =
        document.querySelector(
            "thead tr"
        );

    tbody.innerHTML = "";

    if (!rows || !rows.length) {

        thead.innerHTML = "";

        tbody.innerHTML = `

        <tr>

            <td colspan="20">

                <div class="empty-state">

                    <span class="empty-icon">
                        📭
                    </span>

                    No records found

                </div>

            </td>

        </tr>`;

        return;
    }


    thead.innerHTML = `

        <th>User</th>

        <th>Project</th>

        <th>Category</th>

        <th>Service</th>

        <th>Task</th>

        <th>Keyword</th>

        <th>Submitted URL</th>

        <th>Target URL</th>

        <th style="
            min-width:420px;
        ">
            Other Data
        </th>

        <th>Status</th>

        <th>Action</th>
    `;


    rows.forEach(r => {

        const badge = `
            <span class="
                badge
                badge-${r.status}
            ">
                ${capitalize(r.status)}
            </span>
        `;

        const actions =

            r.status === "pending"

            ? `

                <button
                    class="btn-approve"
                    onclick="
                        updateStatus(
                            ${r.id},
                            'approved'
                        )
                    ">

                    ✔

                </button>

                <button
                    class="btn-reject"
                    onclick="
                        updateStatus(
                            ${r.id},
                            'rejected'
                        )
                    ">

                    ✖

                </button>
            `

            : `—`;


        const data =
            r.dynamic_data || {};

        

        const keyword =

            data.KEYWORD
            ||
            data.keyword
            ||
            data.Keyword
            ||
            "-";


        const submitted =

            data.SUBMITTED_URL
            ||
            data.Submitted_url
            ||
            "";

        let submittedHTML = "-";

        if(submitted){

            submittedHTML = String(submitted)

            .split(/[\n,]+/)

            .filter(x => x.trim())

            .map(link => `

                <div style="
                    margin-bottom:6px;
                ">

                    <a href="${link.trim()}"
                       target="_blank"
                       class="proof-link"
                       style="
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

 
        const target =

            data.Target_url
            ||
            data.target_url
            ||
            "";

        let targetHTML = "-";

        if(target){

            targetHTML = String(target)

            .split(/[\n,]+/)

            .filter(x => x.trim())

            .map(link => `

                <div style="
                    margin-bottom:6px;
                ">

                    <a href="${link.trim()}"
                       target="_blank"
                       class="proof-link"
                       style="
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


        let otherHTML = "";

        Object.entries(data)

        .forEach(([key, value]) => {

            let lower =
                key.toLowerCase();

           

            if(

                lower === "keyword"
                ||
                lower === "submitted_url"
                ||
                lower === "target_url"

            ){
                return;
            }

            if(
                value === null
                ||
                value === ""
            ){
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


        tbody.innerHTML += `

        <tr>

            <td>

                <div class="user-name">

                    ${r.user__first_name || ""}
                    ${r.user__last_name || ""}

                </div>

            </td>

            <td>

                <span class="project-tag">

                    ${r.project__name || ""}

                </span>

            </td>

            <td>

                ${r.category || ""}

            </td>

            <td>

                ${r.service_name || ""}

            </td>

            <td>

                ${r.task_type || ""}

            </td>

            <td style="
                min-width:180px;
            ">

                ${keyword}

            </td>

            <td style="
                min-width:220px;
                max-width:260px;
            ">

                ${submittedHTML}

            </td>

            <td style="
                min-width:220px;
                max-width:260px;
            ">

                ${targetHTML}

            </td>

            <td style="
                min-width:420px;
                max-width:520px;
            ">

                ${otherHTML}

            </td>

            <td>

                ${badge}

            </td>

            <td class="action-cell">

                ${actions}

            </td>

        </tr>
        `;
    });
}

function updateMobileCards(rows) {

    const container =
        document.getElementById(
            "mobileCards"
        );

    if (!container) return;

    container.innerHTML = "";

    if (!rows || !rows.length) {

        container.innerHTML = `

        <div class="m-card">

            <div class="empty-state">

                <span class="empty-icon">
                    📭
                </span>

                No records found

            </div>

        </div>
        `;

        return;
    }

    rows.forEach(r => {

        const badge = `
            <span class="
                badge
                badge-${r.status}
            ">
                ${capitalize(r.status)}
            </span>
        `;

        const actions =

            r.status === "pending"

            ? `

                <button
                    class="btn-approve"
                    onclick="
                        updateStatus(
                            ${r.id},
                            'approved'
                        )
                    ">

                    ✔

                </button>

                <button
                    class="btn-reject"
                    onclick="
                        updateStatus(
                            ${r.id},
                            'rejected'
                        )
                    ">

                    ✖

                </button>
            `

            : "";

        let dynamicHtml = "";

        Object.entries(
            r.dynamic_data || {}
        ).forEach(([key, value]) => {

            dynamicHtml += `

            <div class="m-row">

                <div class="m-label">
                    ${formatLabel(key)}
                </div>

                <div style="
                    text-align:right;
                    max-width:60%;
                    word-break:break-word;
                ">
                    ${value || "-"}
                </div>

            </div>
            `;
        });

        container.innerHTML += `

        <div class="m-card">

            <div class="m-card-header">

                <div>

                    <div class="user-name">

                        ${r.user__first_name || ""}
                        ${r.user__last_name || ""}

                    </div>

                    <div class="user-role">

                        ${r.project__name || ""}

                    </div>

                </div>

                ${badge}

            </div>

            <div class="m-card-body">

                <div class="m-row">

                    <div class="m-label">
                        Category
                    </div>

                    <div>
                        ${r.category || "-"}
                    </div>

                </div>

                <div class="m-row">

                    <div class="m-label">
                        Service
                    </div>

                    <div>
                        ${r.service_name || "-"}
                    </div>

                </div>

                <div class="m-row">

                    <div class="m-label">
                        Task
                    </div>

                    <div>
                        ${r.task_type || "-"}
                    </div>

                </div>

                ${dynamicHtml}

            </div>

            <div class="m-actions">

                ${actions}

            </div>

        </div>
        `;
    });
    console.log(
    document.getElementById("mobileCards")
);
}

function updatePagination(p){

    const container =
        document.getElementById("pagination");

    if(!container || !p) return;

    container.innerHTML="";

    const current = p.page;
    const total = p.pages;

    if(total<=1) return;

    // Previous
    if(current>1){

        container.innerHTML += `
        <button
            onclick="goToPage(${current-1})"
            class="pill">

            <
        </button>
        `;
    }

    // show only 3 page numbers
    let start = Math.max(
        1,
        current-1
    );

    let end = Math.min(
        total,
        start+2
    );

    if(end-start<2){
        start=Math.max(
            1,
            end-2
        );
    }

    for(let i=start;i<=end;i++){

        container.innerHTML += `
        <button
            onclick="goToPage(${i})"
            class="pill
            ${i===current ? 'active':''}">

            ${i}

        </button>
        `;
    }

    // Next
    if(current<total){

        container.innerHTML += `
        <button
            onclick="goToPage(${current+1})"
            class="pill">

            >

        </button>
        `;
    }
}

function goToPage(p) {

    currentPage = p;

    loadDashboard();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function exportExcel() {

    const f = getFilters();

    if (!f) return;

    const query = buildQuery({

        type: f.type,

        start_date: f.start_date,

        end_date: f.end_date,

        search: f.search,

        project: f.project,

        status: f.status
    });

    window.open(
        `/activities/api/export/?export_type=approval&${query}`,
        "_blank"
    );
}

function updateStatus(id, status) {

    fetch(`/activities/api/approve/${id}/`, {

        method: "POST",

        headers: {

            "Content-Type":
                "application/json",

            "X-CSRFToken":
                getCookie("csrftoken")
        },

        body: JSON.stringify({
            status
        })
    })

    .then(res => res.json())

    .then(data => {

        if (data.success) {

            loadDashboard();
        }
    });
}


function capitalize(s) {

    return s

        ? s.charAt(0)
            .toUpperCase()
            + s.slice(1)

        : "";
}

function getCookie(name) {

    let value = null;

    document.cookie
        .split(";")
        .forEach(c => {

            c = c.trim();

            if (
                c.startsWith(
                    name + "="
                )
            ) {

                value = decodeURIComponent(
                    c.substring(
                        name.length + 1
                    )
                );
            }
        });

    return value;
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .getElementById(
                "searchInput"
            )

            ?.addEventListener(
                "input",
                () => {

                    clearTimeout(
                        searchTimer
                    );

                    searchTimer =
                        setTimeout(() => {

                            currentPage = 1;

                            loadDashboard();

                        }, 400);
                }
            );

        document
            .getElementById(
                "projectFilter"
            )

            ?.addEventListener(
                "change",
                () => {

                    currentPage = 1;

                    loadDashboard();
                }
            );

        document
            .getElementById(
                "startDate"
            )

            ?.addEventListener(
                "change",
                () => {

                    currentPage = 1;

                    loadDashboard();
                }
            );

        document
            .getElementById(
                "endDate"
            )

            ?.addEventListener(
                "change",
                () => {

                    currentPage = 1;

                    loadDashboard();
                }
            );

        loadDashboard();
    }
);



function formatLabel(text){

    return text
        .replaceAll("_", " ")
        .replace(/\b\w/g,
            l => l.toUpperCase()
        );
}

