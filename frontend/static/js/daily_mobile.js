
(function () {

  // Only mobile/tablet
  if (window.innerWidth >= 992) return;

  document.addEventListener("DOMContentLoaded", init);

  function init() {

    document.body.style.overflowX = "hidden";

    /* =====================================================
       NAVBAR HEIGHT
    ===================================================== */
    function getNavbarHeight() {

      const nav = document.querySelector(
        "nav, .navbar, header, #topbar, #navbar"
      );

      if (!nav) return 56;

      const rect = nav.getBoundingClientRect();

      return rect.height > 0
        ? Math.ceil(rect.height)
        : 56;
    }

    function applyNavHeight() {

      const h = getNavbarHeight();

      document.documentElement.style.setProperty(
        "--mob-nav-h",
        h + "px"
      );
    }

    applyNavHeight();

    window.addEventListener("load", applyNavHeight);

    window.addEventListener("resize", () => {

      applyNavHeight();

      // restore desktop view properly
      if (window.innerWidth >= 992) {
        location.reload();
      }
    });

    /* =====================================================
       RENAME ORIGINAL IDS
    ===================================================== */
    [
      "filterType",
      "startDate",
      "endDate",
      "startBox",
      "endBox",
      "categoriesContainer",
      "servicesContainer",
      "taskTypes",
      "dynamicForm",
      "tableHead",
      "tableBody",
      "paginationContainer"

    ].forEach(id => {

      const el = document.getElementById(id);

      if (el) {
        el.id = "_desktop_" + id;
      }
    });

    // desktop table wrappers
    document.querySelectorAll(".table-scroll-wrapper")
      .forEach(el => {

        el.classList.remove("table-scroll-wrapper");
        el.classList.add("_desktop_table_wrapper");
      });

    /* =====================================================
       CREATE PROJECT PANEL
    ===================================================== */
    const projectPanel = document.createElement("div");

    projectPanel.id = "mob-projects-panel";

    let cards = `
      <div class="mob-proj-card mob-all"
           data-pid=""
           data-pname="All Projects">

        <span>All Projects</span>
        <span class="mob-arrow">›</span>

      </div>
    `;

    // collect desktop project items
    document.querySelectorAll(".col-lg-3 .project-item")
      .forEach(el => {

        const match = (
          el.getAttribute("onclick") || ""
        ).match(/selectProject\((\d+)/);

        if (!match) return;

        const pid = match[1];

        const name = el.textContent.trim();

        cards += `
          <div class="mob-proj-card project-item"
               data-pid="${pid}"
               data-pname="${name}"
               onclick="selectProject(${pid}, this)">

            <span>${name}</span>
            <span class="mob-arrow">›</span>

          </div>
        `;
      });

    projectPanel.innerHTML = `
      <div class="mob-panel-header">

        <h2>Projects</h2>

      </div>

      <div class="mob-proj-list">

        ${cards}

      </div>
    `;

    /* =====================================================
       CREATE DETAIL PANEL
    ===================================================== */
    const detailPanel = document.createElement("div");

    detailPanel.id = "mob-detail-panel";

    detailPanel.innerHTML = `

      <div id="mob-topbar">

        <button id="mob-back-btn" type="button">

          <svg width="18"
               height="18"
               viewBox="0 0 24 24"
               fill="none"
               stroke="currentColor"
               stroke-width="2.5"
               stroke-linecap="round"
               stroke-linejoin="round">

            <polyline points="15 18 9 12 15 6"></polyline>

          </svg>

          Projects

        </button>

        <span id="mob-project-label"></span>

      </div>

      <!-- FILTER -->
      <div class="mob-card">

        <div class="mob-card-title">
          Filter
        </div>

        <div class="mob-filter-row">

          <div class="mob-filter-group">

            <label>Range</label>

            <select id="filterType"
                    onchange="handleFilterChange()">

              <option value="today">Today</option>
              <option value="week">Last Week</option>
              <option value="month">Last Month</option>
              <option value="custom">Custom</option>

            </select>

          </div>

          <div class="mob-filter-group"
               id="startBox"
               style="display:none;">

            <label>Start</label>

            <input type="date" id="startDate">

          </div>

          <div class="mob-filter-group"
               id="endBox"
               style="display:none;">

            <label>End</label>

            <input type="date" id="endDate">

          </div>

        </div>

        <div class="mob-filter-btns">

          <button class="mob-btn-apply"
                  onclick="loadDataFast()">

            Apply

          </button>

          <button class="mob-btn-excel"
                  onclick="downloadExcel()">

            Excel

          </button>

        </div>

      </div>

      <!-- CATEGORIES -->
      <div class="mob-card">

        <div class="mob-card-title">
          Categories
        </div>

        <div id="categoriesContainer"
             class="mob-pills"></div>

      </div>

      <!-- SERVICES -->
      <div class="mob-card">

        <div class="mob-card-title">
          Services
        </div>

        <div id="servicesContainer"
             class="mob-pills"></div>

      </div>

      <!-- TASK TYPES -->
      <div class="mob-card">

        <div class="mob-card-title">
          Task Type
        </div>

        <div id="taskTypes"></div>

      </div>

      <!-- FORM -->
      <div class="mob-card">

        <div class="mob-card-title">
          Fill Details
        </div>

        <form id="dynamicForm"></form>

      </div>

      <!-- TABLE -->
      <div class="mob-card">

        <div class="mob-card-title">
          Saved Data
        </div>

        <div class="mob-table-wrap">

          <table class="table table-bordered table-hover mb-0">

            <thead>
              <tr id="tableHead"></tr>
            </thead>

            <tbody id="tableBody"></tbody>

          </table>

        </div>

        <div id="paginationContainer"></div>

      </div>
    `;

    /* =====================================================
       APPEND PANELS
    ===================================================== */
    document.body.appendChild(projectPanel);
    document.body.appendChild(detailPanel);

    /* =====================================================
       PROJECT CLICK
    ===================================================== */
    projectPanel.addEventListener("click", function (e) {

      const card = e.target.closest(".mob-proj-card");

      if (!card) return;

      const pid = card.dataset.pid;
      const name = card.dataset.pname;

      document.getElementById(
        "mob-project-label"
      ).textContent = name;

      document.body.classList.add(
        "mob-detail-open"
      );

      detailPanel.scrollTop = 0;

      // reset cards
      document.querySelectorAll(".mob-proj-card")
        .forEach(c => {

          c.style.borderColor = "";
          c.style.background = "";
        });

      // active card
      card.style.borderColor = "#2563eb";
      card.style.background = "#eff6ff";

      if (pid) {

        selectProject(Number(pid), card);

      } else {

        if (window.clearProject) {
          clearProject(document.createElement("div"));
        }

        if (window.loadDataFast) {
          loadDataFast();
        }
      }
    });

    /* =====================================================
       BACK BUTTON
    ===================================================== */
    document.getElementById("mob-back-btn")
      .addEventListener("click", function () {

        document.body.classList.remove(
          "mob-detail-open"
        );

        document.querySelectorAll(".mob-proj-card")
          .forEach(c => {

            c.style.borderColor = "";
            c.style.background = "";
          });
      });

    /* =====================================================
       EDIT ROW WRAPPER
    ===================================================== */
    if (window.editRow) {

      const originalEditRow = window.editRow;

      window.editRow = async function (id) {

        document.body.classList.add(
          "mob-detail-open"
        );

        await originalEditRow(id);

        setTimeout(() => {

          const form = document.getElementById(
            "dynamicForm"
          );

          if (form) {

            form.scrollIntoView({
              behavior: "smooth",
              block: "start"
            });
          }

        }, 200);
      };
    }

    /* =====================================================
       INITIAL LOAD
    ===================================================== */
    if (window.loadDataFast) {
      loadDataFast();
    }
  }

})();
