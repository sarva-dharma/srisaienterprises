/**
 * Client Portal & Application Tracker Module
 */
const ClientPortal = {
  currentProject: null,

  init() {
    this.attachEvents();
    // Check if initial view was requested as portal
    const urlParams = new URLSearchParams(window.location.search);
    const ref = urlParams.get('ref') || urlParams.get('track');
    if (ref) {
      this.trackByReference(ref);
    }
  },

  attachEvents() {
    // Quick Reference Search Form in Hero or Portal Section
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

    // Client Login form
    const loginForm = document.getElementById('client-login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('client-login-email').value;
        const pass = document.getElementById('client-login-password').value;
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
      <div class="p-12 text-center">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-amber-400 mb-4"></div>
        <p class="text-slate-300 font-medium">Querying Karnataka Sakala / EoDB-OBPS Server for ${refNo}...</p>
      </div>
    `;
    this.scrollToPortal();

    try {
      const res = await API.getClientProjects(refNo);
      if (res.error || !res.projects || res.projects.length === 0) {
        portalContainer.innerHTML = `
          <div class="p-8 text-center bg-rose-950/40 rounded-2xl border border-rose-500/30">
            <div class="w-12 h-12 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center mx-auto mb-3 text-xl font-bold">!</div>
            <h3 class="text-xl font-bold text-white mb-2">No Application Found</h3>
            <p class="text-sm text-slate-300 mb-4">Reference "${refNo}" not found in our database. Try sample demo reference: <strong class="text-amber-300 cursor-pointer underline" onclick="ClientPortal.trackByReference('SAKALA-GBA-2026-0894')">SAKALA-GBA-2026-0894</strong></p>
          </div>
        `;
        return;
      }

      this.currentProject = res.projects[0];
      this.renderProject(this.currentProject);
    } catch (err) {
      portalContainer.innerHTML = `<div class="p-4 text-rose-400">Error tracking reference: ${err.message}</div>`;
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

    const isApproved = project.current_stage === 'Approved';

    container.innerHTML = `
      <div class="glass-panel rounded-2xl border border-amber-500/30 p-6 md:p-8 space-y-8 shadow-2xl">
        <!-- Application Header Bar -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-white/10">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/30">
                ${project.authority}
              </span>
              <span class="text-xs text-slate-400 font-mono">Ref: ${project.reference_no}</span>
              ${project.nambike_nakshe_eligible ? `
                <span class="px-2.5 py-0.5 text-xs font-semibold rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                  Nambike Nakshe Self-Declaration
                </span>
              ` : ''}
            </div>
            <h3 class="text-2xl md:text-3xl font-bold text-white">${project.title}</h3>
            <p class="text-sm text-slate-400 mt-1">${project.plot_location} &bull; Survey: <span class="text-slate-200">${project.survey_no || 'Pending'}</span></p>
          </div>

          <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-slate-900/60 p-4 rounded-xl border border-white/5">
            <div>
              <div class="text-xs text-slate-400">Current Sakala Stage</div>
              <div class="text-lg font-bold ${isApproved ? 'text-emerald-400' : 'text-amber-400'} flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full ${isApproved ? 'bg-emerald-400' : 'bg-amber-400 animate-ping'}"></span>
                ${project.current_stage}
              </div>
            </div>
            <div class="border-l border-white/10 pl-4">
              <div class="text-xs text-slate-400">Overall Progress</div>
              <div class="text-lg font-bold text-white">${project.completion_percent}%</div>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <div>
          <div class="w-full bg-slate-800 rounded-full h-3 overflow-hidden">
            <div class="bg-gradient-to-r from-amber-500 to-emerald-400 h-3 rounded-full transition-all duration-700" style="width: ${project.completion_percent}%"></div>
          </div>
        </div>

        <!-- 6-Stage Timeline -->
        <div>
          <h4 class="text-base font-semibold text-white mb-6 flex items-center gap-2">
            <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            Statutory Approval Milestones & Audit Trail
          </h4>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            ${project.timelines.map((t, idx) => {
              const isDone = t.status === 'completed';
              const isInProg = t.status === 'in_progress';
              return `
                <div class="p-4 rounded-xl border ${isDone ? 'bg-emerald-950/20 border-emerald-500/30' : isInProg ? 'bg-amber-950/20 border-amber-500/40 ring-1 ring-amber-500/30' : 'bg-slate-900/40 border-white/5 opacity-60'}">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold px-2 py-0.5 rounded ${isDone ? 'bg-emerald-500/20 text-emerald-300' : isInProg ? 'bg-amber-500/20 text-amber-300' : 'bg-slate-800 text-slate-400'}">
                      Step ${idx + 1}
                    </span>
                    <span class="text-xs font-mono text-slate-400">${t.date_updated || 'Awaiting'}</span>
                  </div>
                  <h5 class="text-sm font-bold text-white mb-1">${t.stage_name}</h5>
                  <p class="text-xs text-slate-400 leading-relaxed">${t.remarks || 'Pending municipal action.'}</p>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Project Meta & Assigned Architect -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-xl bg-slate-900/40 border border-white/5 text-sm">
          <div>
            <span class="text-xs text-slate-400">Applicant:</span>
            <div class="font-semibold text-white mt-0.5">${project.client_name}</div>
          </div>
          <div>
            <span class="text-xs text-slate-400">Plot Area:</span>
            <div class="font-semibold text-white mt-0.5">${project.plot_area_sqft} sq.ft</div>
          </div>
          <div>
            <span class="text-xs text-slate-400">Built-Up Area:</span>
            <div class="font-semibold text-white mt-0.5">${project.builtup_area_sqft} sq.ft</div>
          </div>
          <div>
            <span class="text-xs text-slate-400">Empanelled Architect:</span>
            <div class="font-semibold text-amber-300 mt-0.5">${project.assigned_architect}</div>
          </div>
        </div>

        <!-- Document Downloads Vault -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-base font-semibold text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Approved CAD Drawings & Sanction Orders
            </h4>
            <span class="text-xs text-slate-400">Digital Copies with SHA-256 Stamp</span>
          </div>

          <div class="space-y-3">
            ${project.documents.map(doc => `
              <div class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl bg-slate-900/70 border border-white/5 hover:border-amber-500/30 transition-all gap-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-amber-400/10 text-amber-400 flex items-center justify-center font-bold text-xs uppercase">
                    ${doc.doc_type === 'CAD_DWG' ? 'CAD' : 'PDF'}
                  </div>
                  <div>
                    <div class="text-sm font-bold text-white">${doc.title}</div>
                    <div class="text-xs text-slate-400 mt-0.5 font-mono">${doc.filename} &bull; ${doc.file_size_display}</div>
                  </div>
                </div>

                <a href="/api/client/documents/${doc.id}/download" class="btn-gold px-4 py-2 rounded-lg text-xs font-semibold inline-flex items-center gap-1.5 self-start sm:self-auto shadow">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                  Download File
                </a>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }
};
