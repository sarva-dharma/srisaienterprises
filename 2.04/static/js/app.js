/**
 * Sri Sai Enterprises (ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್) - Version 2.04
 * Clean, lightweight, interactable JavaScript logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initSearchAndFilter();
  initEnquiryForm();
});

/**
 * 1. TAB ROUTING & NAVIGATION
 */
function initTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  function switchTab(targetId, updateHash = true) {
    if (!targetId) targetId = 'services';
    targetId = targetId.replace('#', '');

    const targetSection = document.getElementById(targetId);
    if (!targetSection) return;

    // Update tab buttons
    tabButtons.forEach(btn => {
      const btnTarget = btn.getAttribute('data-tab');
      if (btnTarget === targetId) {
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
      }
    });

    // Update content visibility
    tabContents.forEach(section => {
      if (section.id === targetId) {
        section.classList.add('active');
      } else {
        section.classList.remove('active');
      }
    });

    // Update browser URL hash without jump
    if (updateHash && window.location.hash !== `#${targetId}`) {
      history.pushState(null, '', `#${targetId}`);
    }

    // Scroll to top of main content on tab change
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Attach click listener to tab buttons
  tabButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const target = btn.getAttribute('data-tab');
      switchTab(target);
    });
  });

  // Handle browser back/forward or deep links
  window.addEventListener('hashchange', () => {
    const hash = window.location.hash || '#services';
    switchTab(hash, false);
  });

  // Initial tab based on URL hash
  const initialHash = window.location.hash || '#services';
  switchTab(initialHash, false);

  // Expose switchTab globally for inline tile buttons
  window.switchTab = switchTab;
}

/**
 * 2. SERVICE SEARCH & CATEGORY FILTERING
 */
function initSearchAndFilter() {
  const searchInput = document.getElementById('service-search');
  const filterChips = document.querySelectorAll('.filter-chip');
  const serviceTiles = document.querySelectorAll('.service-tile');
  const noResultsBox = document.getElementById('no-services-match');

  let activeCategory = 'all';
  let searchQuery = '';

  function applyFilters() {
    let visibleCount = 0;

    serviceTiles.forEach(tile => {
      const tileCategory = tile.getAttribute('data-category') || '';
      const tileSearchText = (tile.getAttribute('data-keywords') + ' ' + tile.innerText).toLowerCase();

      const matchesCategory = (activeCategory === 'all' || tileCategory.includes(activeCategory));
      const matchesSearch = (!searchQuery || tileSearchText.includes(searchQuery.toLowerCase().trim()));

      if (matchesCategory && matchesSearch) {
        tile.style.display = 'flex';
        visibleCount++;
      } else {
        tile.style.display = 'none';
      }
    });

    if (noResultsBox) {
      noResultsBox.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      applyFilters();
    });
  }

  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.getAttribute('data-filter') || 'all';
      applyFilters();
    });
  });

  // Expose scenario selection helper
  window.selectCustomerScenario = function(serviceName) {
    if (window.switchTab) {
      window.switchTab('services');
    }

    // Reset search and filters to ensure tile is visible
    const searchInput = document.getElementById('service-search');
    if (searchInput) {
      searchInput.value = '';
    }
    const filterChips = document.querySelectorAll('.filter-chip');
    filterChips.forEach(c => {
      if (c.getAttribute('data-filter') === 'all') {
        c.classList.add('active');
      } else {
        c.classList.remove('active');
      }
    });
    activeCategory = 'all';
    searchQuery = '';
    applyFilters();

    // Scroll to and highlight tile
    setTimeout(() => {
      const enquireBtn = document.querySelector(`.btn-tile-enquire[data-service="${serviceName}"]`);
      if (enquireBtn) {
        const tile = enquireBtn.closest('.service-tile');
        if (tile) {
          tile.scrollIntoView({ behavior: 'smooth', block: 'center' });
          tile.style.transition = 'all 0.3s ease';
          tile.style.boxShadow = '0 0 0 3px #b91c1c, 0 10px 25px rgba(185, 28, 28, 0.25)';
          tile.style.transform = 'translateY(-6px)';
          setTimeout(() => {
            tile.style.boxShadow = '';
            tile.style.transform = '';
          }, 3000);
          showToast(`Showing: ${serviceName}`);
        }
      }
    }, 150);
  };
}

/**
 * 3. INTERACTIVE ENQUIRY FORM & PRE-FILL
 */
function initEnquiryForm() {
  const form = document.getElementById('enquiry-form');
  const serviceDropdown = document.getElementById('enquiry-service');
  const nameInput = document.getElementById('enquiry-name');
  const phoneInput = document.getElementById('enquiry-phone');
  const areaInput = document.getElementById('enquiry-area');
  const plotInput = document.getElementById('enquiry-plot');
  const notesInput = document.getElementById('enquiry-notes');

  const btnSubmitMail = document.getElementById('btn-submit-mail');
  const btnCopyDetails = document.getElementById('btn-copy-details');

  // Service selection from Service Tiles
  const tileEnquireButtons = document.querySelectorAll('.btn-tile-enquire');
  tileEnquireButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const serviceValue = btn.getAttribute('data-service');
      
      // Switch to enquiry tab
      if (window.switchTab) {
        window.switchTab('enquiry');
      }

      // Pre-select service in dropdown
      if (serviceDropdown && serviceValue) {
        serviceDropdown.value = serviceValue;
      }

      // Highlight & focus on form
      setTimeout(() => {
        if (nameInput) {
          nameInput.focus();
        }
      }, 300);
    });
  });

  // Helper to compile enquiry summary
  function getEnquiryDetails() {
    const name = nameInput ? nameInput.value.trim() : '';
    const phone = phoneInput ? phoneInput.value.trim() : '';
    const service = serviceDropdown ? serviceDropdown.options[serviceDropdown.selectedIndex].text : '';
    const area = areaInput ? areaInput.value.trim() : 'Bengaluru';
    const plot = plotInput ? plotInput.value.trim() : 'Not specified';
    const notes = notesInput ? notesInput.value.trim() : '';

    return { name, phone, service, area, plot, notes };
  }

  // Action 1: Send via Email Client (mailto)
  if (btnSubmitMail) {
    btnSubmitMail.addEventListener('click', (e) => {
      e.preventDefault();
      const data = getEnquiryDetails();

      if (!data.name) {
        alert('Please enter your Name before sending.');
        if (nameInput) nameInput.focus();
        return;
      }

      if (!data.phone || data.phone.length < 10) {
        alert('Please enter a valid 10-digit Phone Number so we can reach you.');
        if (phoneInput) phoneInput.focus();
        return;
      }

      const subject = encodeURIComponent(`Service Enquiry: ${data.service} - Sri Sai Enterprises`);
      const body = encodeURIComponent(
`Hello Sri Sai Enterprises,

I would like to enquire about your civil drafting & architectural services in Bengaluru.

Details:
------------------------------------------
• Name: ${data.name}
• Phone: ${data.phone}
• Required Service: ${data.service}
• Property Location: ${data.area}
• Plot / Building Size: ${data.plot}
• Additional Requirements / Notes: 
${data.notes || 'None'}
------------------------------------------

Kindly review and let me know the required documents and next steps.

Thank you,
${data.name}
Phone: ${data.phone}`
      );

      // Open email client
      window.location.href = `mailto:smthyagaraj@gmail.com?subject=${subject}&body=${body}`;
      showToast('Opening your email app to send enquiry...');
    });
  }

  // Action 2: Copy Summary to Clipboard
  if (btnCopyDetails) {
    btnCopyDetails.addEventListener('click', (e) => {
      e.preventDefault();
      const data = getEnquiryDetails();

      if (!data.name && !data.phone) {
        alert('Please fill at least your Name and Phone before copying.');
        return;
      }

      const summaryText = 
`--- SRI SAI ENTERPRISES ENQUIRY ---
Name: ${data.name || 'Not provided'}
Phone: ${data.phone || 'Not provided'}
Service: ${data.service}
Location: ${data.area}
Plot Size: ${data.plot}
Notes: ${data.notes || 'None'}
Office Contact: 94480 54185 / 080 23325509 (Gayathrinagar, Bangalore)`;

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(summaryText)
          .then(() => {
            showToast('✅ Enquiry details copied to clipboard!');
          })
          .catch(() => {
            fallbackCopy(summaryText);
          });
      } else {
        fallbackCopy(summaryText);
      }
    });
  }
}

/**
 * 4. TOAST NOTIFICATION HELPER
 */
function showToast(message) {
  let toast = document.getElementById('toast-notice');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast-notice';
    toast.className = 'toast-notice';
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 4000);
}

function fallbackCopy(text) {
  const tempInput = document.createElement('textarea');
  tempInput.value = text;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);
  showToast('✅ Enquiry details copied to clipboard!');
}
