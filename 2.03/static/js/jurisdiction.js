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
        document.querySelectorAll('.btn-dimension-preset').forEach(b => {
          b.classList.remove('bg-amber-100', 'border-amber-500', 'text-amber-900', 'font-bold');
          b.classList.add('bg-slate-100', 'border-slate-200', 'text-slate-700');
        });
        e.target.classList.remove('bg-slate-100', 'border-slate-200', 'text-slate-700');
        e.target.classList.add('bg-amber-100', 'border-amber-500', 'text-amber-900', 'font-bold');
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
      <div class="p-8 text-center bg-white rounded-2xl border border-slate-200">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-amber-600 mb-3"></div>
        <p class="text-sm text-slate-600 font-medium">Scrutinizing GBA 2026 regulations, zonal maps, and Nambike Nakshe criteria...</p>
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
      resultBox.innerHTML = `<div class="p-4 text-rose-700 bg-rose-50 rounded-xl border border-rose-200">Error fetching municipal bylaws: ${err.message}</div>`;
    }
  },

  renderResults(data) {
    const resultBox = document.getElementById('jurisdiction-result-box');
    const isNambike = data.nambike_nakshe.eligible;
    const loc = data.locality || {};

    resultBox.innerHTML = `
      <div class="p-6 md:p-8 space-y-6 bg-white rounded-2xl border border-slate-200 shadow-sm">
        <!-- Top Banner / Authority -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs uppercase tracking-wider font-semibold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200">
                ${loc.zone || 'Bengaluru Urban'}
              </span>
              <span class="text-xs text-slate-500 font-medium">${loc.name || 'Selected Ward'}</span>
            </div>
            <h3 class="text-2xl font-bold text-slate-900">${loc.primary_authority || 'GBA / BBMP Planning Authority'}</h3>
            <p class="text-sm text-slate-600 mt-0.5">Zonal Office: <span class="text-slate-900 font-medium">${loc.zonal_office || 'Bengaluru Urban Zonal Office'}</span></p>
          </div>

          <!-- Nambike Nakshe Badge -->
          <div class="flex-shrink-0">
            <div class="p-4 rounded-xl border ${isNambike ? 'bg-emerald-50 border-emerald-300 text-emerald-900' : 'bg-blue-50 border-blue-300 text-blue-900'}">
              <div class="text-xs uppercase font-bold tracking-wider mb-1 flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full ${isNambike ? 'bg-emerald-600' : 'bg-blue-600'}"></span>
                Nambike Nakshe Status
              </div>
              <div class="font-bold text-base md:text-lg">${data.nambike_nakshe.status}</div>
              <div class="text-xs opacity-90 mt-1">SLA: ${data.nambike_nakshe.timeline}</div>
            </div>
          </div>
        </div>

        <!-- Explanation -->
        <p class="text-sm text-slate-700 bg-slate-50 p-3.5 rounded-xl border border-slate-200 leading-relaxed">
          ${data.nambike_nakshe.details}
        </p>

        <!-- Bylaw Specs Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Plot Area (ನಿವೇಶನ)</div>
            <div class="text-lg font-bold text-slate-900 mt-1">${data.plot_details.area_sqft} sq.ft</div>
            <div class="text-xs text-amber-700 mt-0.5 font-medium">${data.plot_details.width} x ${data.plot_details.length} ft</div>
          </div>

          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Permissible FAR (ಎಫ್‌ಎಆರ್)</div>
            <div class="text-lg font-bold text-slate-900 mt-1">${data.zoning_metrics.max_far}</div>
            <div class="text-xs text-slate-600 mt-0.5">${data.plot_details.road_width} ft Abutting Road</div>
          </div>

          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Max Built-up (ಗರಿಷ್ಠ ನಿರ್ಮಾಣ)</div>
            <div class="text-lg font-bold text-emerald-700 mt-1">${data.zoning_metrics.max_permissible_builtup_sqft} sq.ft</div>
            <div class="text-xs text-slate-600 mt-0.5">Master Plan 2031 Norms</div>
          </div>

          <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <div class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Betterment Rate (ಬೆಟರ್‌ಮೆಂಟ್)</div>
            <div class="text-lg font-bold text-amber-800 mt-1">₹${loc.typical_betterment_rate || 250}/sq.ft</div>
            <div class="text-xs text-slate-600 mt-0.5">For B-Khata Conversion</div>
          </div>
        </div>

        <!-- Setbacks Matrix -->
        <div>
          <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 mb-2.5">Statutory Setbacks for this Plot (ಕಡ್ಡಾಯ ಸೆಟ್‌ಬ್ಯಾಕ್‌ಗಳು)</h4>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-center">
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div class="text-xs text-slate-500 font-semibold">Front Setback (ಮುಂಭಾಗ)</div>
              <div class="font-bold text-slate-900 mt-1">${data.zoning_metrics.setbacks.front}</div>
            </div>
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div class="text-xs text-slate-500 font-semibold">Rear Setback (ಹಿಂಭಾಗ)</div>
              <div class="font-bold text-slate-900 mt-1">${data.zoning_metrics.setbacks.rear}</div>
            </div>
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div class="text-xs text-slate-500 font-semibold">Side Setbacks (ಪಕ್ಕದ ಅಂತರ)</div>
              <div class="font-bold text-slate-900 mt-1">${data.zoning_metrics.setbacks.sides}</div>
            </div>
          </div>
        </div>

        <!-- Mandatory Clearances -->
        <div>
          <h4 class="text-sm font-bold uppercase tracking-wider text-slate-900 mb-2.5">Mandatory Clearances for this Area (ಅಗತ್ಯವಿರುವ ಎನ್‌ಒಸಿಗಳು)</h4>
          <div class="space-y-2">
            ${data.zoning_metrics.mandatory_clearances.map(c => `
              <div class="flex items-center gap-3 p-3 rounded-xl bg-slate-50 border border-slate-200">
                <svg class="w-4 h-4 text-emerald-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="text-sm text-slate-800 font-medium">${c}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Special Guidelines & CTA -->
        <div class="pt-4 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="text-xs text-slate-500 italic">
            * Note: ${loc.guidelines || 'Strict adherence to GBA bylaws and fire buffer corridors.'}
          </div>
          <button onclick="openBookingModal('Plan Sanctions & Approvals', '${loc.name || ''}', '${data.plot_details.width}x${data.plot_details.length} ft')" class="btn-gold px-6 py-2.5 rounded-xl text-xs font-bold whitespace-nowrap shadow-md">
            Apply for ${isNambike ? 'Nambike Nakshe (ನಂಬಿಕೆ ನಕ್ಷೆ)' : 'Sanction (ನಕ್ಷೆ ಮಂಜೂರಾತಿ)'} Now
          </button>
        </div>
      </div>
    `;
  }
};
