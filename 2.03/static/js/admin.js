/**
 * Admin Dashboard & CRM / CMS Management Console
 */
const AdminPanel = {
  currentTab: 'leads',

  init() {
    this.attachEvents();
  },

  attachEvents() {
    // Admin login trigger
    const adminLoginForm = document.getElementById('admin-login-form');
    if (adminLoginForm) {
      adminLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('admin-email').value;
        const pass = document.getElementById('admin-password').value;
        await this.handleLogin(email, pass);
      });
    }

    // Tab switching
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tab = e.currentTarget.dataset.tab;
        this.switchTab(tab);
      });
    });

    // Lead status filter
    const leadFilter = document.getElementById('admin-lead-filter');
    if (leadFilter) {
      leadFilter.addEventListener('change', () => this.loadLeads());
    }

    // New Project Form
    const newProjectForm = document.getElementById('admin-new-project-form');
    if (newProjectForm) {
      newProjectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleCreateProject();
      });
    }

    // New Service Form
    const newServiceForm = document.getElementById('admin-new-service-form');
    if (newServiceForm) {
      newServiceForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleCreateService();
      });
    }

    // New Blog Form
    const newBlogForm = document.getElementById('admin-new-blog-form');
    if (newBlogForm) {
      newBlogForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleCreateBlog();
      });
    }
  },

  async handleLogin(email, password) {
    try {
      const res = await API.login(email, password);
      if (res.error) {
        alert(res.error);
        return;
      }
      if (res.user.role !== 'admin' && res.user.role !== 'architect') {
        alert('Access denied: Admin privileges required.');
        return;
      }
      showToast(`Admin Console Activated: ${res.user.name}`);
      closeModal('admin-login-modal');
      this.openDashboard();
    } catch (err) {
      alert('Login failed: ' + err.message);
    }
  },

  openDashboard() {
    const modal = document.getElementById('admin-panel-modal');
    if (modal) {
      modal.classList.remove('hidden');
      this.switchTab('leads');
      this.loadMetrics();
    }
  },

  logout() {
    closeModal('admin-panel-modal');
    showToast('Logged out of Admin Console');
  },

  switchTab(tabName) {
    this.currentTab = tabName;
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
      if (btn.dataset.tab === tabName) {
        btn.classList.add('text-amber-700', 'border-b-2', 'border-amber-600');
        btn.classList.remove('text-slate-500');
      } else {
        btn.classList.remove('text-amber-700', 'border-b-2', 'border-amber-600');
        btn.classList.add('text-slate-500');
      }
    });

    document.querySelectorAll('.admin-tab-content').forEach(pane => {
      pane.classList.add('hidden');
    });
    const activePane = document.getElementById(`admin-pane-${tabName}`);
    if (activePane) activePane.classList.remove('hidden');

    if (tabName === 'leads') this.loadLeads();
    if (tabName === 'projects') this.loadProjects();
    if (tabName === 'services') this.loadServices();
    if (tabName === 'blogs') this.loadBlogs();
  },

  async loadMetrics() {
    try {
      const data = await API.getAdminMetrics();
      if (data.error) return;

      const elTotal = document.getElementById('metric-total-leads');
      const elNew = document.getElementById('metric-new-leads');
      const elActive = document.getElementById('metric-active-projects');
      const elApproved = document.getElementById('metric-approved-projects');
      if (elTotal) elTotal.textContent = data.total_leads;
      if (elNew) elNew.textContent = data.new_leads;
      if (elActive) elActive.textContent = data.active_projects;
      if (elApproved) elApproved.textContent = data.approved_projects;
    } catch (err) {
      console.error(err);
    }
  },

  // LEADS CRM
  async loadLeads() {
    const filter = document.getElementById('admin-lead-filter')?.value || '';
    const container = document.getElementById('admin-leads-list');
    if (!container) return;

    container.innerHTML = '<div class="p-8 text-center text-slate-500">Loading incoming consultations...</div>';

    try {
      const data = await API.getAdminLeads(filter);
      if (!data.leads || data.leads.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500">No leads match this criteria.</div>';
        return;
      }

      container.innerHTML = data.leads.map(lead => {
        const cleanPhone = lead.phone.replace(/[^0-9]/g, '');
        const waLink = `https://wa.me/${cleanPhone}?text=${encodeURIComponent(`Hi ${lead.full_name}, thank you for contacting our Bengaluru Building Plan Sanction desk regarding your plot at ${lead.plot_location || 'Bengaluru'}.`)}`;

        return `
          <div class="p-4 rounded-2xl bg-slate-50 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="font-bold text-slate-900">${lead.full_name}</span>
                <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-200">${lead.service_title}</span>
              </div>
              <div class="text-xs text-slate-600 font-medium">
                ${lead.phone} &bull; ${lead.email || 'No email'} &bull; Location: <strong class="text-slate-800">${lead.plot_location || 'Bengaluru'}</strong> (${lead.plot_dimensions || 'N/A'})
              </div>
              ${lead.message ? `<div class="text-xs italic text-slate-500">"${lead.message}"</div>` : ''}
            </div>

            <div class="flex items-center gap-3">
              <select onchange="AdminPanel.updateLeadStatus(${lead.id}, this.value)" class="text-xs bg-white text-slate-800 rounded-lg border border-slate-300 px-2.5 py-1.5 shadow-sm font-medium">
                <option value="new" ${lead.status === 'new' ? 'selected' : ''}>New Inquiry</option>
                <option value="contacted" ${lead.status === 'contacted' ? 'selected' : ''}>Contacted</option>
                <option value="quotation_sent" ${lead.status === 'quotation_sent' ? 'selected' : ''}>Quote Sent</option>
                <option value="converted" ${lead.status === 'converted' ? 'selected' : ''}>Converted</option>
                <option value="archived" ${lead.status === 'archived' ? 'selected' : ''}>Archived</option>
              </select>

              <a href="${waLink}" target="_blank" class="px-3.5 py-1.5 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 text-xs font-bold inline-flex items-center gap-1 shadow-sm">
                WhatsApp
              </a>
            </div>
          </div>
        `;
      }).join('');
    } catch (err) {
      container.innerHTML = `<div class="p-6 text-center text-rose-600">${err.message}</div>`;
    }
  },

  async updateLeadStatus(id, newStatus) {
    try {
      await API.updateLead(id, { status: newStatus });
      showToast('Lead status updated');
      this.loadMetrics();
    } catch (err) {
      alert(err.message);
    }
  },

  async saveLeadNote(id, notes) {
    try {
      await API.updateLead(id, { internal_notes: notes });
      showToast('Lead internal note saved');
    } catch (err) {
      console.error(err);
    }
  },

  // CLIENT APPLICATIONS TRACKER
  async loadProjects() {
    const container = document.getElementById('admin-projects-list');
    if (!container) return;

    container.innerHTML = '<div class="p-8 text-center text-slate-500">Loading active files...</div>';

    try {
      const data = await API.getAdminProjects();
      if (!data.projects || data.projects.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-slate-500">No projects found.</div>';
        return;
      }

      const stages = ['Drafting', 'PreDCR Scrutiny', 'AutoDCR Submission', 'Site Inspection', 'NOC Clearance', 'Approved'];

      container.innerHTML = data.projects.map(proj => {
        return `
          <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 font-bold border border-amber-200">${proj.authority}</span>
                  <span class="text-xs font-mono text-slate-500 font-semibold">Ref: ${proj.reference_no}</span>
                </div>
                <h4 class="text-lg font-bold text-slate-900">${proj.title}</h4>
                <p class="text-xs text-slate-600">Client: <strong class="text-slate-800">${proj.client_name}</strong> &bull; ${proj.plot_location}</p>
              </div>

              <!-- Stage Advance Selector -->
              <div class="flex items-center gap-3 bg-slate-50 p-3 rounded-xl border border-slate-200">
                <div class="text-xs text-slate-600 font-semibold">Advance Stage:</div>
                <select onchange="AdminPanel.advanceStage(${proj.id}, this.value)" class="bg-white border border-amber-500 text-amber-900 text-xs rounded-lg px-3 py-1.5 font-bold shadow-sm">
                  ${stages.map(s => `
                    <option value="${s}" ${proj.current_stage === s ? 'selected' : ''}>${s}</option>
                  `).join('')}
                </select>
                <button onclick="ClientPortal.trackByReference('${proj.reference_no}')" class="btn-outline-gold px-3 py-1.5 rounded-lg text-xs font-semibold">
                  View in Portal
                </button>
              </div>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs bg-slate-50 p-3 rounded-xl border border-slate-200">
              <div><span class="text-slate-500">Plot Area:</span> <strong class="text-slate-900">${proj.plot_area_sqft} sq.ft</strong></div>
              <div><span class="text-slate-500">Built-Up:</span> <strong class="text-slate-900">${proj.builtup_area_sqft} sq.ft</strong></div>
              <div><span class="text-slate-500">Nambike Nakshe:</span> <strong class="${proj.nambike_nakshe_eligible ? 'text-emerald-700 font-bold' : 'text-slate-500'}">${proj.nambike_nakshe_eligible ? 'Yes' : 'No'}</strong></div>
              <div><span class="text-slate-500">Progress:</span> <strong class="text-amber-800 font-bold">${proj.completion_percent}%</strong></div>
            </div>
          </div>
        `;
      }).join('');
    } catch (err) {
      container.innerHTML = `<div class="p-6 text-center text-rose-600">${err.message}</div>`;
    }
  },

  async advanceStage(projectId, newStage) {
    const remarks = prompt(`Enter progress remarks for stage "${newStage}":`, `Status updated to ${newStage} by town planning desk.`);
    if (remarks === null) return;

    try {
      const res = await API.updateProjectStage(projectId, newStage, remarks);
      showToast(res.message);
      this.loadProjects();
      this.loadMetrics();
    } catch (err) {
      alert(err.message);
    }
  },

  async handleCreateProject() {
    const clientName = document.getElementById('proj-client-name').value;
    const clientEmail = document.getElementById('proj-client-email').value;
    const title = document.getElementById('proj-title').value;
    const location = document.getElementById('proj-location').value;
    const authority = document.getElementById('proj-authority').value;
    const plotArea = parseFloat(document.getElementById('proj-plot-area').value) || 1200;
    const builtupArea = parseFloat(document.getElementById('proj-builtup-area').value) || 2400;
    const isNambike = document.getElementById('proj-nambike').checked;

    try {
      const res = await API.createAdminProject({
        client_name: clientName,
        client_email: clientEmail,
        title: title,
        plot_location: location,
        authority: authority,
        plot_area_sqft: plotArea,
        builtup_area_sqft: builtupArea,
        nambike_nakshe_eligible: isNambike
      });

      showToast(`Created application: ${res.project.reference_no}`);
      document.getElementById('admin-new-project-form').reset();
      this.loadProjects();
      this.loadMetrics();
    } catch (err) {
      alert('Error creating project: ' + err.message);
    }
  },

  // SERVICES & PRICING CMS
  async loadServices() {
    const container = document.getElementById('admin-services-list');
    if (!container) return;

    try {
      const data = await API.getAdminServices();
      container.innerHTML = data.services.map(s => {
        return `
          <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <span class="text-xs font-bold uppercase tracking-wider text-amber-800">${s.category}</span>
                <h4 class="text-lg font-bold text-slate-900">${s.title}</h4>
              </div>
              <span class="text-xs px-2.5 py-0.5 rounded-full font-semibold ${s.is_active ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-rose-100 text-rose-800 border border-rose-200'}">
                ${s.is_active ? 'Active on Website' : 'Hidden'}
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div>
                <label class="text-slate-600 block mb-1 font-medium">Base Fee (INR):</label>
                <input type="number" id="srv-base-${s.id}" value="${s.base_fee}" class="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono shadow-sm">
              </div>
              <div>
                <label class="text-slate-600 block mb-1 font-medium">Betterment Rate (₹/sq.ft):</label>
                <input type="number" id="srv-betterment-${s.id}" value="${s.betterment_rate_sqft}" class="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono shadow-sm">
              </div>
              <div>
                <label class="text-slate-600 block mb-1 font-medium">Scrutiny Rate (₹/sq.ft):</label>
                <input type="number" id="srv-scrutiny-${s.id}" value="${s.scrutiny_rate_sqft}" class="w-full bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-900 font-mono shadow-sm">
              </div>
            </div>

            <div>
              <label class="text-slate-600 text-xs block mb-1 font-medium">Short Description:</label>
              <textarea id="srv-desc-${s.id}" rows="2" class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs text-slate-800 shadow-sm">${s.short_desc}</textarea>
            </div>

            <div class="flex justify-end gap-3 pt-2">
              <button onclick="AdminPanel.saveService(${s.id})" class="btn-gold px-4 py-1.5 rounded-lg text-xs font-semibold shadow-sm">
                Save Changes to Website
              </button>
            </div>
          </div>
        `;
      }).join('');
    } catch (err) {
      container.innerHTML = `<div class="p-4 text-rose-600">${err.message}</div>`;
    }
  },

  async saveService(serviceId) {
    const baseFee = parseFloat(document.getElementById(`srv-base-${serviceId}`).value);
    const bettermentRate = parseFloat(document.getElementById(`srv-betterment-${serviceId}`).value);
    const scrutinyRate = parseFloat(document.getElementById(`srv-scrutiny-${serviceId}`).value);
    const shortDesc = document.getElementById(`srv-desc-${serviceId}`).value;

    try {
      const res = await API.updateService(serviceId, {
        base_fee: baseFee,
        betterment_rate_sqft: bettermentRate,
        scrutiny_rate_sqft: scrutinyRate,
        short_desc: shortDesc
      });
      showToast('Service & pricing updated live on website');
      if (window.loadPublicServices) window.loadPublicServices();
    } catch (err) {
      alert(err.message);
    }
  },

  async handleCreateService() {
    const title = document.getElementById('new-srv-title').value;
    const category = document.getElementById('new-srv-category').value;
    const baseFee = parseFloat(document.getElementById('new-srv-fee').value) || 15000;
    const shortDesc = document.getElementById('new-srv-desc').value;

    try {
      await API.createService({
        title,
        category,
        base_fee: baseFee,
        short_desc: shortDesc,
        full_desc: shortDesc
      });
      showToast('New service published to catalog');
      document.getElementById('admin-new-service-form').reset();
      this.loadServices();
      if (window.loadPublicServices) window.loadPublicServices();
    } catch (err) {
      alert(err.message);
    }
  },

  // BLOG CMS
  async loadBlogs() {
    const container = document.getElementById('admin-blogs-list');
    if (!container) return;

    try {
      const data = await API.getBlogs();
      container.innerHTML = data.blogs.map(b => {
        return `
          <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-xs text-amber-800 font-bold uppercase tracking-wider">${b.category}</span>
              <h5 class="text-sm font-bold text-slate-900 mt-0.5">${b.title}</h5>
              <div class="text-xs text-slate-500 mt-1">${b.author} &bull; ${b.created_at}</div>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 font-bold border border-emerald-200">Published</span>
          </div>
        `;
      }).join('');
    } catch (err) {
      container.innerHTML = `<div class="p-4 text-rose-600">${err.message}</div>`;
    }
  },

  async handleCreateBlog() {
    const title = document.getElementById('blog-title').value;
    const category = document.getElementById('blog-category').value;
    const content = document.getElementById('blog-content').value;

    try {
      await fetch('/api/admin/blogs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, category, content, excerpt: content.substring(0, 150) + '...' })
      });
      showToast('New article published to Knowledge Hub');
      document.getElementById('admin-new-blog-form').reset();
      this.loadBlogs();
      if (window.loadPublicBlogs) window.loadPublicBlogs();
    } catch (err) {
      alert(err.message);
    }
  }
};
