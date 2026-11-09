/**
 * Interactive Document Readiness Checklist for Bengaluru Plot Owners
 * Sri Sai Enterprises (Since 1989)
 */
const DocumentChecklist = {
  DOCUMENTS: [
    {
      id: "doc_sale_deed",
      name: "Registered Sale Deed / Mother Deed",
      name_kn: "ನೋಂದಾಯಿತ ಖರೀದಿ ಪತ್ರ / ಮೂಲ ಪತ್ರ",
      category: "title",
      mandatory: true,
      description: "Registered deed showing absolute title and ownership chain.",
      description_kn: "ನಿವೇಶನದ ಮೂಲ ಮಾಲೀಕತ್ವ ಹಾಗೂ ನೋಂದಾಯಿತ ಕ್ರಯಪತ್ರ."
    },
    {
      id: "doc_link_deeds",
      name: "30-Year Prior Title Deeds Chain",
      name_kn: "ಹಿಂದಿನ 30 ವರ್ಷಗಳ ಲಿಂಕ್ ದಾಖಲೆಗಳು",
      category: "title",
      mandatory: true,
      description: "Unbroken sequence of past transactions and parent documents.",
      description_kn: "ಖರೀದಿಗೆ ಮುನ್ನ ಇದ್ದ ಮಾಲೀಕರ 30 ವರ್ಷಗಳ ಹಿಂಬರಹ ದಾಖಲೆಗಳು."
    },
    {
      id: "doc_possession",
      name: "Possession Certificate / Allotment Letter",
      name_kn: "ಸ್ವಾಧೀನ ಪ್ರಮಾಣಪತ್ರ / ಹಂಚಿಕೆ ಪತ್ರ",
      category: "title",
      mandatory: false,
      description: "Issued by BDA, KHB, or registered Housing Societies (if applicable).",
      description_kn: "ಬಿಡಿಎ, ಕೆಎಚ್‌ಬಿ ಅಥವಾ ಹೌಸಿಂಗ್ ಸೊಸೈಟಿ ನೀಡಿದ ಸ್ವಾಧೀನ ಪತ್ರ."
    },
    {
      id: "doc_ekhata",
      name: "Digital e-Khata Certificate (e-Aasthi Form 3)",
      name_kn: "ಡಿಜಿಟಲ್ ಇ-ಖಾತಾ / ಇ-ಆಸ್ತಿ ನಮೂನೆ 3",
      category: "tax",
      mandatory: true,
      description: "BBMP / Urban Development digitized property record with QR code.",
      description_kn: "ಬಿಬಿಎಂಪಿ ಕ್ಯೂಆರ್ ಕೋಡ್ ಸಹಿತ ನೂತನ ಡಿಜಿಟಲ್ ಇ-ಖಾತಾ ಪ್ರಮಾಣಪತ್ರ."
    },
    {
      id: "doc_tax_receipt",
      name: "Latest Property Tax Paid SAS Challan & Receipt",
      name_kn: "ಚಾಲ್ತಿ ಸಾಲಿನ ಆಸ್ತಿ ತೆರಿಗೆ ಪಾವತಿ ರಸೀದಿ (SAS)",
      category: "tax",
      mandatory: true,
      description: "Current financial year BBMP SAS property tax receipt with zero arrears.",
      description_kn: "ಪ್ರಸ್ತುತ ವರ್ಷದ ಬಿಬಿಎಂಪಿ ಆಸ್ತಿ ತೆರಿಗೆ ಪಾವತಿಸಿದ ಅಧಿಕೃತ ರಸೀದಿ."
    },
    {
      id: "doc_ec",
      name: "Encumbrance Certificate (EC Form 15) for 15-30 Yrs",
      name_kn: "ಹೊಣೆಗಾರಿಕೆ ಇಲ್ಲದಿರುವ ಪ್ರಮಾಣ ಪತ್ರ (EC ಫಾರ್ಮ್ 15)",
      category: "tax",
      mandatory: true,
      description: "Sub-registrar certified EC confirming zero legal mortgages or claims.",
      description_kn: "ಉಪನೋಂದಣಾಧಿಕಾರಿಗಳಿಂದ ಪಡೆದ ಸಾಲ-ಭಾರವಿಲ್ಲದ ನಿರಾಕ್ಷೇಪಣಾ ಪ್ರಮಾಣಪತ್ರ."
    },
    {
      id: "doc_survey",
      name: "Certified Survey Sketch / Mojini 11E / Tippani",
      name_kn: "ಮೋಜಣಿ 11ಇ / ಸರ್ವೆ ಸ್ಕೆಚ್ / ಟಿಪ್ಪಣಿ ನಕ್ಷೆ",
      category: "tech",
      mandatory: false,
      description: "Mojini certified sketch showing exact boundaries and road frontages.",
      description_kn: "ಸರ್ಕಾರಿ ಸರ್ವೇಯರ್ ಸಿದ್ಧಪಡಿಸಿದ ಅಧಿಕೃತ ಜಮೀನು ಅಳತೆ ನಕ್ಷೆ."
    },
    {
      id: "doc_dc_conversion",
      name: "DC Conversion Order & Betterment Challan",
      name_kn: "ಡಿಸಿ ಭೂಪರಿವರ್ತನಾ ಆದೇಶ & ಬೆಟರ್‌ಮೆಂಟ್ ರಸೀದಿ",
      category: "tech",
      mandatory: false,
      description: "Required if plot originates from agricultural revenue land conversion.",
      description_kn: "ಕೃಷಿಯೇತರ ಉದ್ದೇಶಕ್ಕೆ ಭೂಪರಿವರ್ತನೆಗೊಂಡ ಅಧಿಕೃತ ಜಿಲ್ಲಾಧಿಕಾರಿ ಆದೇಶ."
    },
    {
      id: "doc_layout_approval",
      name: "Approved Layout Plan Copy (BDA / BIAAPA / BMRDA)",
      name_kn: "ಅನುಮೋದಿತ ಬಡಾವಣೆ ನಕ್ಷೆ (BDA / BIAAPA)",
      category: "tech",
      mandatory: false,
      description: "Town planning sanctioned layout map indicating site demarcations.",
      description_kn: "ನಗರ ಯೋಜನಾ ಪ್ರಾಧಿಕಾರದಿಂದ ಅಂಗೀಕೃತಗೊಂಡ ಬಡಾವಣೆ ನಕ್ಷೆ ಪ್ರತಿ."
    },
    {
      id: "doc_prior_sanction",
      name: "Existing Building Sanction Plan (If Alteration)",
      name_kn: "ಹಿಂದಿನ ಮಂಜೂರಾದ ಕಟ್ಟಡ ನಕ್ಷೆ (ಮಾರ್ಪಾಡಾಗಿದ್ದರೆ)",
      category: "tech",
      mandatory: false,
      description: "Previously approved municipal blueprint (if modifying existing structure).",
      description_kn: "ಹಳೆಯ ಕಟ್ಟಡ ಮಾರ್ಪಾಡು ಅಥವಾ ಹೆಚ್ಚುವರಿ ಮಹಡಿ ನಿರ್ಮಾಣಕ್ಕಿದ್ದಲ್ಲಿ."
    }
  ],

  checkedIds: new Set(),

  init() {
    this.loadState();
    this.renderCheckboxes();
    this.updateMetrics();
    this.attachEvents();
  },

  loadState() {
    try {
      const stored = localStorage.getItem('sse_doc_checklist');
      if (stored) {
        const arr = JSON.parse(stored);
        if (Array.isArray(arr)) {
          this.checkedIds = new Set(arr);
        }
      }
    } catch (e) {}
  },

  saveState() {
    try {
      localStorage.setItem('sse_doc_checklist', JSON.stringify([...this.checkedIds]));
    } catch (e) {}
  },

  toggle(docId) {
    if (this.checkedIds.has(docId)) {
      this.checkedIds.delete(docId);
    } else {
      this.checkedIds.add(docId);
    }
    this.saveState();
    this.updateMetrics();
    this.refreshClasses(docId);
  },

  refreshClasses(docId) {
    const isChecked = this.checkedIds.has(docId);
    const label = document.querySelector(`label[for="${docId}"]`);
    if (label) {
      if (isChecked) {
        label.classList.add('bg-amber-50/80', 'border-amber-400', 'shadow-sm');
        label.classList.remove('bg-white', 'border-slate-200');
      } else {
        label.classList.remove('bg-amber-50/80', 'border-amber-400', 'shadow-sm');
        label.classList.add('bg-white', 'border-slate-200');
      }
    }
  },

  reset() {
    this.checkedIds.clear();
    this.saveState();
    this.renderCheckboxes();
    this.updateMetrics();
    if (window.showToast) window.showToast('Checklist reset to blank');
  },

  calculateReadiness() {
    const total = this.DOCUMENTS.length;
    const checkedCount = this.checkedIds.size;
    const mandatoryTotal = this.DOCUMENTS.filter(d => d.mandatory).length;
    const mandatoryChecked = this.DOCUMENTS.filter(d => d.mandatory && this.checkedIds.has(d.id)).length;

    // Weighting: Mandatory docs account for 75%, supplemental for 25%
    const mandatoryScore = (mandatoryChecked / mandatoryTotal) * 75;
    const supplementalScore = ((checkedCount - mandatoryChecked) / (total - mandatoryTotal)) * 25;
    const score = Math.round(mandatoryScore + supplementalScore);

    return {
      score,
      checkedCount,
      total,
      mandatoryChecked,
      mandatoryTotal,
      allMandatoryReady: mandatoryChecked === mandatoryTotal
    };
  },

  updateMetrics() {
    const { score, checkedCount, total, mandatoryChecked, mandatoryTotal, allMandatoryReady } = this.calculateReadiness();

    const bar = document.getElementById('checklist-progress-bar');
    const text = document.getElementById('checklist-progress-text');
    const badge = document.getElementById('checklist-status-badge');
    const countEl = document.getElementById('checklist-count-display');

    if (bar) bar.style.width = `${score}%`;
    if (text) text.textContent = `${score}%`;
    if (countEl) countEl.textContent = `${checkedCount} of ${total} Documents Ready (${mandatoryChecked}/${mandatoryTotal} Mandatory)`;

    if (badge) {
      if (score >= 90 && allMandatoryReady) {
        badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300";
        badge.textContent = "100% Ready for BBMP BPAS Submission • ಸಂಪೂರ್ಣ ಸಿದ್ಧ";
      } else if (score >= 60) {
        badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-sky-100 text-sky-800 border border-sky-300";
        badge.textContent = "Near Complete • ಬಹುತೇಕ ಸಿದ್ಧವಾಗಿದೆ (Few items pending)";
      } else if (score >= 25) {
        badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300";
        badge.textContent = "Partially Ready • ಕೆಲವು ಮುಖ್ಯ ದಾಖಲೆಗಳು ಬಾಕಿ ಇವೆ";
      } else {
        badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800 border border-red-300";
        badge.textContent = "Initial Stage • ಆರಂಭಿಕ ಹಂತ";
      }
    }
  },

  renderCheckboxes() {
    const catTitle = document.getElementById('checklist-container-title');
    const catTax = document.getElementById('checklist-container-tax');
    const catTech = document.getElementById('checklist-container-tech');

    if (!catTitle || !catTax || !catTech) return;

    const renderCard = (doc) => {
      const isChecked = this.checkedIds.has(doc.id);
      return `
        <label for="${doc.id}" class="cursor-pointer block p-3.5 sm:p-4 rounded-xl border ${isChecked ? 'bg-amber-50/80 border-amber-400 shadow-sm' : 'bg-white border-slate-200 hover:border-amber-300'} transition-all select-none">
          <div class="flex items-start gap-3">
            <input type="checkbox" id="${doc.id}" ${isChecked ? 'checked' : ''} onchange="DocumentChecklist.toggle('${doc.id}')" class="w-4 h-4 sm:w-5 sm:h-5 rounded text-red-700 focus:ring-red-500 border-slate-300 mt-0.5 flex-shrink-0 cursor-pointer">
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-xs sm:text-sm font-bold text-slate-900">${doc.name}</span>
                ${doc.mandatory ? '<span class="px-1.5 py-0.5 rounded text-[9px] font-extrabold bg-red-100 text-red-800 uppercase tracking-wider">Mandatory / ಕಡ್ಡಾಯ</span>' : '<span class="px-1.5 py-0.5 rounded text-[9px] font-semibold bg-slate-100 text-slate-600">Supplemental</span>'}
              </div>
              <div class="text-[11px] text-red-800 font-kannada font-bold mt-0.5">${doc.name_kn}</div>
              <p class="text-[11px] text-slate-500 mt-1 leading-snug">${doc.description}</p>
            </div>
          </div>
        </label>
      `;
    };

    catTitle.innerHTML = this.DOCUMENTS.filter(d => d.category === 'title').map(renderCard).join('');
    catTax.innerHTML = this.DOCUMENTS.filter(d => d.category === 'tax').map(renderCard).join('');
    catTech.innerHTML = this.DOCUMENTS.filter(d => d.category === 'tech').map(renderCard).join('');
  },

  attachEvents() {
    const waBtn = document.getElementById('checklist-whatsapp-btn');
    if (waBtn) {
      waBtn.addEventListener('click', () => this.sendToWhatsApp());
    }

    const bookBtn = document.getElementById('checklist-booking-btn');
    if (bookBtn) {
      bookBtn.addEventListener('click', () => this.bookWithChecklist());
    }

    const printBtn = document.getElementById('checklist-print-btn');
    if (printBtn) {
      printBtn.addEventListener('click', () => window.print());
    }

    const resetBtn = document.getElementById('checklist-reset-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => this.reset());
    }
  },

  generateSummaryText() {
    const { score, checkedCount, total } = this.calculateReadiness();
    const readyList = this.DOCUMENTS.filter(d => this.checkedIds.has(d.id)).map(d => `✅ ${d.name}`);
    const pendingList = this.DOCUMENTS.filter(d => !this.checkedIds.has(d.id)).map(d => `❌ ${d.name} (${d.name_kn})`);

    let text = `*Sri Sai Enterprises - Plot Sanction Document Readiness*\n`;
    text += `*Readiness Score:* ${score}% (${checkedCount}/${total} Documents Ready)\n\n`;
    text += `*Ready Documents:*\n${readyList.length > 0 ? readyList.join('\n') : 'None yet'}\n\n`;
    text += `*Pending / Need Advice:*\n${pendingList.length > 0 ? pendingList.join('\n') : 'None! 100% Complete'}\n\n`;
    text += `Please review my document status and advise on municipal sanction filing.`;
    return text;
  },

  sendToWhatsApp() {
    const summary = this.generateSummaryText();
    const url = `https://wa.me/919448054185?text=${encodeURIComponent(summary)}`;
    window.open(url, '_blank');
  },

  bookWithChecklist() {
    const summary = this.generateSummaryText();
    if (window.openBookingModal) {
      openBookingModal('Plan Sanctions & Approvals');
    }
    const msgBox = document.getElementById('lead-message');
    if (msgBox) {
      msgBox.value = summary;
    }
  }
};
