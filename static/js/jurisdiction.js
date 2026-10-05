/**
 * Interactive Bengaluru Jurisdiction & Bylaw Checker
 */
const JurisdictionChecker = {
  localities: [],

  async init() {
    try {
      const data = await API.getJurisdictions();
      this.localities = data.localities || [];
      this.populateDropdown();
      this.attachEvents();
    } catch (err) {
      console.error('Failed to load jurisdictions:', err);
    }
  },

  populateDropdown() {
    const select = document.getElementById('jurisdiction-select');
    if (!select) return;

    select.innerHTML = '<option value="">-- Select Your Bengaluru Locality / Ward --</option>';
    this.localities.forEach(loc => {
      const opt = document.createElement('option');
      opt.value = loc.id;
      opt.textContent = `${loc.name} (${loc.zone})`;
      select.appendChild(opt);
    });
  },

  attachEvents() {
    const form = document.getElementById('jurisdiction-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleCheck();
      });
    }

    // Quick dimension buttons
    document.querySelectorAll('.btn-dimension-preset').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const [w, l] = e.target.dataset.dimensions.split('x');
        document.getElementById('input-plot-width').value = w;
        document.getElementById('input-plot-length').value = l;
        document.querySelectorAll('.btn-dimension-preset').forEach(b => b.classList.remove('bg-amber-500/20', 'border-amber-400', 'text-amber-300'));
        e.target.classList.add('bg-amber-500/20', 'border-amber-400', 'text-amber-300');
        this.handleCheck();
      });
    });
  },

  async handleCheck() {
    const localityId = document.getElementById('jurisdiction-select').value;
    const width = parseFloat(document.getElementById('input-plot-width').value) || 30;
    const length = parseFloat(document.getElementById('input-plot-length').value) || 40;
    const roadWidth = parseFloat(document.getElementById('input-road-width').value) || 30;
    const buildingType = document.getElementById('input-building-type').value || 'Residential';

    if (!localityId) {
      alert('Please select a locality to check your municipal jurisdiction.');
      return;
    }

    const resultBox = document.getElementById('jurisdiction-result-box');
    resultBox.classList.remove('hidden');
    resultBox.innerHTML = `
      <div class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-400 mb-3"></div>
        <p class="text-sm text-slate-300">Scrutinizing GBA 2026 regulations, zonal maps, and Nambike Nakshe criteria...</p>
      </div>
    `;

    try {
      const data = await API.checkJurisdiction({
        locality_id: localityId,
        plot_width: width,
        plot_length: length,
        road_width: roadWidth,
        building_type: buildingType
      });

      this.renderResults(data);
    } catch (err) {
      resultBox.innerHTML = `<div class="p-4 text-rose-400 bg-rose-950/40 rounded-xl border border-rose-800/40">Error fetching municipal bylaws: ${err.message}</div>`;
    }
  },

  renderResults(data) {
    const resultBox = document.getElementById('jurisdiction-result-box');
    const isNambike = data.nambike_nakshe.eligible;

    resultBox.innerHTML = `
      <div class="p-6 md:p-8 space-y-6">
        <!-- Top Banner / Authority -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-white/10">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs uppercase tracking-wider font-semibold px-2.5 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/20">
                ${data.zone}
              </span>
              <span class="text-xs text-slate-400">${data.locality}</span>
            </div>
            <h3 class="text-2xl font-bold text-white">${data.authority}</h3>
            <p class="text-sm text-slate-400 mt-0.5">Zonal Office: <span class="text-slate-200">${data.zonal_office}</span></p>
          </div>

          <!-- Nambike Nakshe Badge -->
          <div class="flex-shrink-0">
            <div class="p-4 rounded-xl border ${isNambike ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300' : 'bg-blue-950/40 border-blue-500/40 text-blue-300'}">
              <div class="text-xs uppercase font-bold tracking-wider mb-1 flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full ${isNambike ? 'bg-emerald-400' : 'bg-blue-400'}"></span>
                Nambike Nakshe Status
              </div>
              <div class="font-bold text-base md:text-lg">${data.nambike_nakshe.status}</div>
              <div class="text-xs opacity-80 mt-1">SLA: ${data.nambike_nakshe.sla_days}</div>
            </div>
          </div>
        </div>

        <!-- Explanation -->
        <p class="text-sm text-slate-300 bg-slate-800/40 p-3.5 rounded-lg border border-slate-700/50">
          ${data.nambike_nakshe.details}
        </p>

        <!-- Bylaw Specs Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-slate-900/60 p-4 rounded-xl border border-white/5">
            <div class="text-xs text-slate-400">Plot Area</div>
            <div class="text-lg font-bold text-white mt-1">${data.plot_area_sqft} sq.ft</div>
            <div class="text-xs text-amber-400/80 mt-0.5">${data.plot_dimensions}</div>
          </div>

          <div class="bg-slate-900/60 p-4 rounded-xl border border-white/5">
            <div class="text-xs text-slate-400">Permissible FAR</div>
            <div class="text-lg font-bold text-white mt-1">${data.byelaws.permissible_far}</div>
            <div class="text-xs text-slate-400 mt-0.5">${data.road_width_ft} ft Abutting Road</div>
          </div>

          <div class="bg-slate-900/60 p-4 rounded-xl border border-white/5">
            <div class="text-xs text-slate-400">Max Permissible Built-up</div>
            <div class="text-lg font-bold text-emerald-400 mt-1">${data.byelaws.max_permissible_builtup_sqft} sq.ft</div>
            <div class="text-xs text-slate-400 mt-0.5">Under Master Plan Norms</div>
          </div>

          <div class="bg-slate-900/60 p-4 rounded-xl border border-white/5">
            <div class="text-xs text-slate-400">Betterment Rate (Est.)</div>
            <div class="text-lg font-bold text-amber-300 mt-1">₹${data.betterment_rate_per_sqft}/sq.ft</div>
            <div class="text-xs text-slate-400 mt-0.5">For Unassessed / B-Khata</div>
          </div>
        </div>

        <!-- Setbacks Matrix -->
        <div>
          <h4 class="text-sm font-semibold uppercase tracking-wider text-amber-400 mb-2.5">Statutory Setbacks for this Plot</h4>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div class="p-3 bg-slate-900/40 rounded-lg border border-white/5">
              <div class="text-xs text-slate-400">Front Setback</div>
              <div class="font-bold text-white mt-1">${data.byelaws.setbacks.front}</div>
            </div>
            <div class="p-3 bg-slate-900/40 rounded-lg border border-white/5">
              <div class="text-xs text-slate-400">Rear Setback</div>
              <div class="font-bold text-white mt-1">${data.byelaws.setbacks.rear}</div>
            </div>
            <div class="p-3 bg-slate-900/40 rounded-lg border border-white/5">
              <div class="text-xs text-slate-400">Left Side</div>
              <div class="font-bold text-white mt-1">${data.byelaws.setbacks.left}</div>
            </div>
            <div class="p-3 bg-slate-900/40 rounded-lg border border-white/5">
              <div class="text-xs text-slate-400">Right Side</div>
              <div class="font-bold text-white mt-1">${data.byelaws.setbacks.right}</div>
            </div>
          </div>
          <p class="text-xs text-slate-400 mt-2">${data.byelaws.setbacks.note}</p>
        </div>

        <!-- Mandatory NOCs -->
        <div>
          <h4 class="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-2.5">Mandatory Statutory Clearances (NOCs)</h4>
          <div class="space-y-2">
            ${data.mandatory_nocs.map(noc => `
              <div class="flex items-start justify-between p-3 rounded-lg bg-slate-900/40 border border-white/5">
                <div>
                  <div class="text-sm font-medium text-white">${noc.name}</div>
                  <div class="text-xs text-slate-400 mt-0.5">${noc.notes}</div>
                </div>
                <span class="text-xs px-2 py-0.5 rounded ${noc.mandatory ? 'bg-amber-400/10 text-amber-300 border border-amber-400/20' : 'bg-slate-700 text-slate-300'}">
                  ${noc.mandatory ? 'Mandatory' : 'Optional'}
                </span>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Special Guidelines & CTA -->
        <div class="pt-4 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="text-xs text-slate-400 italic">
            * Note: ${data.special_guidelines}
          </div>
          <button onclick="openBookingModal('Plan Sanctions & Approvals', '${data.locality}', '${data.plot_dimensions}')" class="btn-gold px-6 py-2.5 rounded-lg text-sm font-semibold whitespace-nowrap shadow-lg">
            Apply for ${isNambike ? 'Nambike Nakshe' : 'Sanction'} Now
          </button>
        </div>
      </div>
    `;
  }
};
