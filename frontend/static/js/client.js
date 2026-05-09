
(function () {

  'use strict';



  var state = {

    type: 'all',
    page: 1,
    limit: 10,
    lastTotal: null,
    loading: false
  };

  var chartInstance = null;
  var pollTimer = null;



  var tableBody =
    document.getElementById(
      'taskTableBody'
    );

  var paginationWrap =
    document.getElementById(
      'paginationWrap'
    );

  var perPageSelect =
    document.getElementById(
      'perPageSelect'
    );

  var exportBtn =
    document.getElementById(
      'exportBtn'
    );

  

  function escHtml(str) {

    return String(str)

      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function badgeClass(status) {

    if (status === 'approved')
      return 'badge-approved';

    if (status === 'pending')
      return 'badge-pending';

    return 'badge-rejected';
  }

  function buildQuery(extra) {

    var startDate =
      document.getElementById(
        'startDate'
      )?.value;

    var endDate =
      document.getElementById(
        'endDate'
      )?.value;

    var params = {

      type: state.type,
      page: state.page,
      limit: state.limit
    };

    if (startDate)
      params.start_date = startDate;

    if (endDate)
      params.end_date = endDate;

    if (extra)
      Object.assign(params, extra);

    return Object.keys(params)

      .filter(function(k){

        return (
          params[k] !== '' &&
          params[k] != null
        );
      })

      .map(function(k){

        return (
          k + '=' +
          encodeURIComponent(params[k])
        );
      })

      .join('&');
  }

  

  function renderKPI(kpi) {

    document.getElementById(
      'kpiTotal'
    ).textContent = kpi.total || 0;

    document.getElementById(
      'kpiApproved'
    ).textContent = kpi.approved || 0;

    document.getElementById(
      'kpiPending'
    ).textContent = kpi.pending || 0;

    document.getElementById(
      'kpiRejected'
    ).textContent = kpi.rejected || 0;
  }

  /* ───────────────── LINKS ───────────────── */

  function renderLinks(text, color) {

    if (!text) return '-';

    return String(text)

      .split(/[\n,]+/)

      .filter(Boolean)

      .map(function(link){

        link = link.trim();

        return `

          <div style="margin-bottom:8px;">

            <a
              href="${escHtml(link)}"
              target="_blank"
              rel="noopener noreferrer"
              class="link-item"
              style="
                color:${color};
                display:block;
                text-decoration:none;
                white-space:nowrap;
                overflow:hidden;
                text-overflow:ellipsis;
                max-width:100%;
              ">

              ${escHtml(link)}

            </a>

          </div>
        `;
      })

      .join('');
  }

  /* ───────────────── TABLE ───────────────── */

  function renderTable(rows) {

    if (!rows || !rows.length) {

      tableBody.innerHTML = `

        <tr class="empty-row">

          <td colspan="9">

            📋 No tasks found

          </td>

        </tr>
      `;

      return;
    }

    let html = '';

    rows.forEach(function(r){

      let keyword =
        r.keyword ||
        r.KEYWORD ||
        r.data?.keyword ||
        r.data?.KEYWORD ||
        '-';

      let submitted =
        r.SUBMITTED_URL ||
        r.submitted_url ||
        r.data?.SUBMITTED_URL ||
        r.data?.submitted_url ||
        '';

      let target =
        r.TARGET_URL ||
        r.target_url ||
        r['Target url'] ||
        r.data?.TARGET_URL ||
        r.data?.target_url ||
        '';

      let otherHTML = '';

      Object.entries(
        r.data || {}
      ).forEach(function([k,v]){

        let lower =
          String(k).toLowerCase();

        if (

          lower.includes('keyword')

          ||

          (
            lower.includes('submitted') &&
            lower.includes('url')
          )

          ||

          (
            lower.includes('target') &&
            lower.includes('url')
          )

        ) {
          return;
        }

        if (!v) return;

        otherHTML += `

          <div style="
            margin-bottom:8px;
            padding:8px;
            background:#f8fafc;
            border:1px solid #e2e8f0;
            border-radius:8px;
            font-size:12px;
          ">

            <strong>

              ${escHtml(
                k.replaceAll('_',' ')
              )}

            </strong>

            <div style="
              margin-top:3px;
              word-break:break-word;
            ">

              ${escHtml(String(v))}

            </div>

          </div>
        `;
      });

      html += `

        <tr>

          <td>

            ${escHtml(
              r.project__name || '—'
            )}

          </td>

          <td>

            ${escHtml(
              r.service_name || '—'
            )}

          </td>

          <td>

            ${escHtml(
              r.task_type || '—'
            )}

          </td>

          <td style="
            min-width:220px;
            max-width:300px;
          ">

            ${escHtml(String(keyword))}

          </td>

          <td style="
            min-width:260px;
            max-width:360px;
          ">

            ${renderLinks(
              submitted,
              '#2563eb'
            )}

          </td>

          <td style="
            min-width:260px;
            max-width:360px;
          ">

            ${renderLinks(
              target,
              '#059669'
            )}

          </td>

          <td style="
            min-width:320px;
            max-width:420px;
          ">

            ${otherHTML || '-'}

          </td>

          <td>

            <span class="
              badge
              ${badgeClass(r.status)}
            ">

              ${escHtml(
                r.status || 'pending'
              )}

            </span>

          </td>

          <td>

            ${escHtml(
              r.date || '—'
            )}

          </td>

        </tr>
      `;
    });

    requestAnimationFrame(function(){

      tableBody.innerHTML = html;

    });
  }

  /* ───────────────── CHART ───────────────── */

  function renderChart(labels, data) {

    const ctx =
      document.getElementById(
        'chartCanvas'
      );

    if (!ctx) return;

    if (chartInstance) {

      chartInstance.data.labels = labels;
      chartInstance.data.datasets[0].data = data;
      chartInstance.update();

      return;
    }

    chartInstance = new Chart(ctx, {

      type: 'line',

      data: {

        labels: labels,

        datasets: [{

          label: 'Tasks',

          data: data,

          borderColor: '#4338ca',

          backgroundColor:
            'rgba(67,56,202,0.07)',

          borderWidth: 2,
          fill: true,
          tension: 0.4
        }]
      },

      options: {

        responsive: true,
        maintainAspectRatio: true
      }
    });
  }

  /* ───────────────── PAGINATION ───────────────── */

  function renderPagination(p) {

    if (!p || p.pages <= 1) {

      paginationWrap.innerHTML = '';
      return;
    }

    let html = '';

    if (p.page > 1) {

      html += `
        <button
          class="pill"
          data-page="${p.page - 1}">

          ← Prev

        </button>
      `;
    }

    for (

      let i = 1;

      i <= p.pages;

      i++

    ) {

      html += `

        <button
          class="pill ${i === p.page ? 'active' : ''}"
          data-page="${i}">

          ${i}

        </button>
      `;
    }

    if (p.page < p.pages) {

      html += `
        <button
          class="pill"
          data-page="${p.page + 1}">

          Next →

        </button>
      `;
    }

    paginationWrap.innerHTML = html;
  }

  /* ───────────────── LOAD DASHBOARD ───────────────── */

  async function loadDashboard(silent=false) {

    if (state.loading) return;

    state.loading = true;

    if (!silent) {

      tableBody.innerHTML = `

        <tr class="loading-row">

          <td colspan="9">

            <span class="spinner"></span>

            Loading...

          </td>

        </tr>
      `;
    }

    try {

      const res = await fetch(

        '/activities/api/dashboard/?' +
        buildQuery(),

        {
          headers: {
            'X-Requested-With':
            'XMLHttpRequest'
          }
        }
      );

      const data = await res.json();

      requestAnimationFrame(function(){

        renderKPI(
          data.kpi || {}
        );

        renderTable(
          data.table || []
        );

        renderPagination(
          data.pagination || {}
        );
      });

      setTimeout(function(){

        if (data.chart) {

          renderChart(

            data.chart.labels || [],

            data.chart.data || []
          );
        }

      }, 50);

      state.lastTotal =
        data.kpi?.total || 0;
    }

    catch(err){

      console.error(err);

      tableBody.innerHTML = `

        <tr class="empty-row">

          <td colspan="9">

            ⚠️ Failed to load data

          </td>

        </tr>
      `;
    }

    finally {

      state.loading = false;
    }
  }

  /* ───────────────── POLLING ───────────────── */

  function startPolling() {

    if (pollTimer)
      clearInterval(pollTimer);

    pollTimer = setInterval(function(){

      loadDashboard(true);

    }, 10000);
  }

  /* ───────────────── FILTER BUTTONS ───────────────── */

  document
  .querySelectorAll(
    '.filter-group .pill[data-filter]'
  )

  .forEach(function(btn){

    btn.addEventListener(
      'click',

      function(){

        document

        .querySelectorAll(
          '.filter-group .pill[data-filter]'
        )

        .forEach(function(b){

          b.classList.remove(
            'active'
          );
        });

        btn.classList.add(
          'active'
        );

        state.type =
          btn.dataset.filter;

        state.page = 1;

        loadDashboard();
      }
    );
  });

  /* ───────────────── PAGINATION CLICK ───────────────── */

  paginationWrap.addEventListener(

    'click',

    function(e){

      const btn =
        e.target.closest(
          '[data-page]'
        );

      if (!btn) return;

      state.page =
        parseInt(
          btn.dataset.page
        );

      loadDashboard();
    }
  );

  /* ───────────────── PER PAGE ───────────────── */

  if (perPageSelect) {

    perPageSelect.addEventListener(

      'change',

      function(){

        state.limit =
          parseInt(this.value) || 10;

        state.page = 1;

        loadDashboard();
      }
    );
  }

  /* ───────────────── DATE FILTERS ───────────────── */

  ['startDate','endDate']

  .forEach(function(id){

    const el =
      document.getElementById(id);

    if (!el) return;

    el.addEventListener(

      'change',

      function(){

        state.page = 1;

        loadDashboard();
      }
    );
  });

  /* ───────────────── EXPORT ───────────────── */

  if (exportBtn) {

    exportBtn.addEventListener(

      'click',

      function(){

        window.location.href =

          '/activities/api/export/?export_type=client&' +

          buildQuery();
      }
    );
  }

  /* ───────────────── INITIAL LOAD ───────────────── */

  document.addEventListener(

    'DOMContentLoaded',

    function(){

      const defaultBtn =
        document.getElementById(
          'defaultFilter'
        );

      if (defaultBtn) {

        document

        .querySelectorAll(
          '.filter-group .pill'
        )

        .forEach(function(btn){

          btn.classList.remove(
            'active'
          );
        });

        defaultBtn.classList.add(
          'active'
        );
      }

      state.type = 'all';

      loadDashboard();

      startPolling();
    }
  );

})();
