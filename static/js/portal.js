/**
 * Client Portal & Application Tracker Module
 */
const ClientPortal = {
  currentProject: null,

  init() {
    this.attachEvents();
    const urlParams = new URLSearchParams(window.location.search);
    const ref = urlParams.get('ref') || urlParams.get('track');
    if (ref) {
      this.trackByReference(ref);
    }
  },

  attachEvents() {
    const trackForms = document.querySelectorAll('.form-track-approval');
    trackForms.forEach(form => {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = form.querySelector('input[type="text"]');
        const ref = input ? input.value.trim() : '';
        if (ref) {
          await this.trackByReference(ref);
        }
      });
    });

    const loginForm = document.getElementById('client-login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('client-email').value;
        const pass = document.getElementById('client-password').value;
        await this.handleLogin(email, pass);
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
      showToast(`Welcome back, ${res.user.name}!`);
      closeModal('client-login-modal');
      await this.loadMyApplications();
    } catch (err) {
      alert('Login failed: ' + err.message);
    }
  },

  async loadMyApplications() {
    try {
      const res = await API.getClientProjects();
      if (res.projects && res.projects.length > 0) {
        this.renderProject(res.projects[0]);
        this.scrollToPortal();
      } else {
        alert('No active applications found for your account.');
      }
    } catch (err) {
      console.error(err);
    }
  },

  async trackByReference(refNo) {
    const portalContainer = document.getElementById('portal-live-container');
    if (!portalContainer) return;

    portalContainer.classList.remove('hidden');
    portalContainer.innerHTML = `
      <div class="p-12 text-center bg-white rounded-3xl border border-slate-200 shadow-sm">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-amber-600 mb-4"></div>
        <p class="text-slate-700 font-medium">Querying Karnataka Sakala / EoDB-OBPS Server for ${refNo}...</p>
      </div>
    `;
    this.scrollToPortal();

    try {
      const res = await API.getClientProjects(refNo);
      if (res.error || !res.projects || res.projects.length === 0) {
        portalContainer.innerHTML = `
          <div class="p-8 text-center bg-rose-50 rounded-2xl border border-rose-200">
            <div class="w-12 h-12 rounded-full bg-rose-100 text-rose-700 flex items-center justify-center mx-auto mb-3 text-xl font-bold">!</div>
            <h3 class="text-xl font-bold text-slate-900 mb-2">No Application Found</h3>
            <p class="text-sm text-slate-600 mb-4">Reference "${refNo}" not found in our database. Try sample demo reference: <strong class="text-amber-800 cursor-pointer underline font-bold" onclick="ClientPortal.trackByReference('SAKALA-GBA-2026-0894')">SAKALA-GBA-2026-0894</strong></p>
          </div>
        `;
        return;
      }

      this.currentProject = res.projects[0];
      this.renderProject(this.currentProject);
    } catch (err) {
      portalContainer.innerHTML = `<div class="p-4 text-rose-700 bg-rose-50 rounded-xl border border-rose-200">Error tracking reference: ${err.message}</div>`;
    }
  },

  scrollToPortal() {
    const section = document.getElementById('client-portal-section');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  },

  renderProject(project) {
    const container = document.getElementById('portal-live-container');
    if (!container) return;
    container.classList.remove('hidden');

    const isApproved = project.status === 'APPROVED';

    container.innerHTML = `
      <div class="glass-panel bg-white rounded-3xl border border-amber-300/80 p-6 md:p-8 space-y-8 shadow-lg">
        <!-- Application Header Bar -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-200">
          <div>
            <div class="flex items-center gap-3 mb-2 flex-wrap">
              <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full bg-amber-50 text-amber-800 border border-amber-200">
                GBA / BBMP Authority
              </span>
              <span class="text-xs text-slate-500 font-mono font-semibold">Ref: ${project.reference_no}</span>
              <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200">
                Nambike Nakshe Self-Declaration
              </span>
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-slate-900">${project.project_title}</h3>
            <p class="text-sm text-slate-600 mt-1">${project.locality} &bull; Dimensions: <span class="text-slate-900 font-medium">${project.plot_dimensions}</span></p>
          </div>

          <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-200">
            <div>
              <div class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Current Sakala Stage</div>
              <div class="text-base md:text-lg font-bold ${isApproved ? 'text-emerald-700' : 'text-amber-800'} flex items-center gap-2 mt-0.5">
                <span class="w-2.5 h-2.5 rounded-full ${isApproved ? 'bg-emerald-600' : 'bg-amber-600 animate-pulse'}"></span>
                ${project.current_stage}
              </div>
            </div>
            <div class="border-l border-slate-200 pl-4">
              <div class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Overall Progress</div>
              <div class="text-lg font-bold text-slate-900 mt-0.5">${project.progress_percent}%</div>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <div>
          <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden border border-slate-200">
            <div class="bg-gradient-to-r from-amber-500 to-emerald-500 h-3 rounded-full transition-all duration-700" style="width: ${project.progress_percent}%"></div>
          </div>
        </div>

        <!-- 4-Stage Timeline -->
        <div>
          <h4 class="text-base font-bold text-slate-900 mb-6 flex items-center gap-2">
            <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            Statutory Approval Milestones & Audit Trail
          </h4>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            ${project.timeline.map((t, idx) => {
              const isDone = t.completed;
              return `
                <div class="p-4 rounded-2xl border ${isDone ? 'bg-emerald-50/70 border-emerald-200' : 'bg-slate-50 border-slate-200 opacity-75'}">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold px-2 py-0.5 rounded ${isDone ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-700'}">
                      Step ${idx + 1}
                    </span>
                    <span class="text-xs font-mono text-slate-500">${t.date}</span>
                  </div>
                  <h5 class="text-sm font-bold text-slate-900 mb-1">${t.stage}</h5>
                  <p class="text-xs text-slate-600 leading-relaxed">${isDone ? 'Milestone Completed Successfully.' : 'Under processing with department.'}</p>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Document Downloads Vault -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Approved CAD Drawings & Sanction Orders
            </h4>
            <span class="text-xs text-slate-500">Official Digital Copies</span>
          </div>

          <div class="space-y-3">
            ${project.documents.map(doc => `
              <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-slate-50 border border-slate-200 hover:border-amber-400 transition-all gap-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-xs">
                    ${doc.name.endsWith('.dwg') ? 'CAD' : 'PDF'}
                  </div>
                  <div>
                    <div class="text-sm font-bold text-slate-900">${doc.name}</div>
                    <div class="text-xs text-slate-500 mt-0.5 font-mono">${doc.size}</div>
                  </div>
                </div>

                <button onclick="showToast('Downloading verified document: ${doc.name}')" class="btn-gold px-4 py-2 rounded-xl text-xs font-semibold inline-flex items-center gap-1.5 self-start sm:self-auto shadow-sm">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                  Download File
                </button>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }
};
