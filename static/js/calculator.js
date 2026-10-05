/**
 * Building Sanction Cost & Betterment Fee Estimator
 */
const FeeCalculator = {
  init() {
    this.attachEvents();
    this.calculate();
  },

  attachEvents() {
    const inputs = ['calc-width', 'calc-length', 'calc-floors', 'calc-b-khata', 'calc-locality'];
    inputs.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', () => this.calculate());
        el.addEventListener('change', () => this.calculate());
      }
    });

    // Floor quick buttons
    document.querySelectorAll('.btn-calc-floor').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.btn-calc-floor').forEach(b => b.classList.remove('bg-amber-500/20', 'border-amber-400', 'text-amber-300'));
        e.target.classList.add('bg-amber-500/20', 'border-amber-400', 'text-amber-300');
        document.getElementById('calc-floors').value = e.target.dataset.floors;
        this.calculate();
      });
    });
  },

  async calculate() {
    const width = parseFloat(document.getElementById('calc-width')?.value) || 30;
    const length = parseFloat(document.getElementById('calc-length')?.value) || 40;
    const floors = parseInt(document.getElementById('calc-floors')?.value) || 3;
    const hasBKhata = document.getElementById('calc-b-khata')?.checked || false;
    const localityId = document.getElementById('calc-locality')?.value || 'whitefield';

    // Update dimensions visual display
    const areaSqft = width * length;
    const approxBuiltup = Math.round(areaSqft * 0.75 * floors);

    const elPlotArea = document.getElementById('calc-display-plot-area');
    const elBuiltupArea = document.getElementById('calc-display-builtup-area');
    if (elPlotArea) elPlotArea.textContent = `${areaSqft.toLocaleString('en-IN')} sq.ft`;
    if (elBuiltupArea) elBuiltupArea.textContent = `${approxBuiltup.toLocaleString('en-IN')} sq.ft`;

    try {
      const data = await API.calculateEstimate({
        plot_width: width,
        plot_length: length,
        floors: floors,
        has_b_khata: hasBKhata,
        locality_id: localityId
      });

      this.renderBreakdown(data);
    } catch (err) {
      console.error('Calculation error:', err);
    }
  },

  renderBreakdown(data) {
    const b = data.breakdown;
    const formatINR = (num) => '₹' + Math.round(num).toLocaleString('en-IN');

    const elScrutiny = document.getElementById('fee-scrutiny');
    const elCess = document.getElementById('fee-cess');
    const elBetterment = document.getElementById('fee-betterment');
    const elBettermentRow = document.getElementById('row-betterment');
    const elCad = document.getElementById('fee-cad');
    const elLiaison = document.getElementById('fee-liaison');
    const elTotal = document.getElementById('fee-total');

    if (elScrutiny) elScrutiny.textContent = formatINR(b.municipal_scrutiny_fee);
    if (elCess) elCess.textContent = formatINR(b.statutory_cess_rwh);
    
    if (elBettermentRow) {
      if (b.betterment_levy > 0) {
        elBettermentRow.classList.remove('hidden');
        if (elBetterment) elBetterment.textContent = formatINR(b.betterment_levy);
      } else {
        elBettermentRow.classList.add('hidden');
      }
    }

    if (elCad) elCad.textContent = formatINR(b.autodcr_drafting_fee);
    if (elLiaison) elLiaison.textContent = formatINR(b.architect_liaisoning_fee);
    if (elTotal) elTotal.textContent = formatINR(data.total_estimated);
  }
};
