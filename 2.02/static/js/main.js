/**
 * Main Application Orchestration & Dynamic UI Rendering
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize Modules
  if (window.JurisdictionChecker) JurisdictionChecker.init();
  if (window.FeeCalculator) FeeCalculator.init();
  if (window.ClientPortal) ClientPortal.init();
  if (window.AdminPanel) AdminPanel.init();

  // Load Dynamic Catalog & Blogs from Backend
  loadPublicServices();
  loadPublicBlogs();

  // Attach Consultation Booking Form
  const bookingForm = document.getElementById('consultation-booking-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = bookingForm.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.innerHTML = '<span class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-slate-900 border-t-transparent mr-2"></span> Submitting...';

      const payload = {
        full_name: document.getElementById('lead-name').value,
        phone: document.getElementById('lead-phone').value,
        email: document.getElementById('lead-email').value,
        plot_location: document.getElementById('lead-location').value,
        plot_dimensions: document.getElementById('lead-dimensions').value,
        service_title: document.getElementById('lead-service').value,
        message: document.getElementById('lead-message').value
      };

      try {
        const res = await API.submitLead(payload);
        if (res.error) {
          alert(res.error);
        } else {
          showToast('Consultation Booked! Our liaison architect will call you shortly.');
          bookingForm.reset();
          closeModal('booking-modal');
        }
      } catch (err) {
        alert('Submission failed: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = 'Confirm Free Consultation';
      }
    });
  }

  // Mobile navigation hamburger toggle
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }
});

// Dynamic Services Renderer
window.loadPublicServices = async function() {
  const container = document.getElementById('dynamic-services-grid');
  if (!container) return;

  try {
    const data = await API.getServices();
    if (!data.services || data.services.length === 0) return;

    const iconSvgs = {
      'building': '<svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>',
      'file-text': '<svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>',
      'compass': '<svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>',
      'home': '<svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>',
      'shield-check': '<svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>'
    };

    container.innerHTML = data.services.map(s => {
      const icon = iconSvgs[s.icon] || iconSvgs['building'];
      const basePrice = s.base_fee > 0 ? `From ₹${Math.round(s.base_fee).toLocaleString('en-IN')}` : 'Custom Scope';

      return `
        <div class="glass-panel card-hover-gold p-6 md:p-8 rounded-2xl flex flex-col justify-between relative overflow-hidden group">
          <div class="absolute top-0 right-0 w-24 h-24 bg-amber-400/5 rounded-bl-full pointer-events-none group-hover:bg-amber-400/10 transition-all"></div>
          
          <div>
            <div class="flex items-center justify-between mb-4">
              <div class="w-12 h-12 rounded-xl bg-amber-400/10 border border-amber-400/20 flex items-center justify-center">
                ${icon}
              </div>
              <span class="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 font-semibold border border-white/5">
                ${s.turnaround_days}
              </span>
            </div>

            <span class="text-xs font-bold uppercase tracking-wider text-amber-400">${s.category}</span>
            <h3 class="text-xl font-bold text-white mt-1 mb-2.5">${s.title}</h3>
            <p class="text-sm text-slate-400 leading-relaxed mb-6">${s.short_desc}</p>

            ${s.features && s.features.length > 0 ? `
              <ul class="space-y-2 mb-6 text-xs text-slate-300">
                ${s.features.slice(0, 3).map(f => `
                  <li class="flex items-start gap-2">
                    <svg class="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    <span>${f}</span>
                  </li>
                `).join('')}
              </ul>
            ` : ''}
          </div>

          <div class="pt-4 border-t border-white/5 flex items-center justify-between">
            <div>
              <div class="text-[11px] text-slate-500 uppercase tracking-wider">Starting At</div>
              <div class="text-lg font-bold text-white font-mono">${basePrice}</div>
            </div>

            <button onclick="openBookingModal('${s.title}')" class="btn-outline-gold px-4 py-2 rounded-lg text-xs font-semibold">
              Get Quote
            </button>
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading services:', err);
  }
};

// Dynamic Blogs Renderer
window.loadPublicBlogs = async function() {
  const container = document.getElementById('dynamic-blogs-grid');
  if (!container) return;

  try {
    const data = await API.getBlogs();
    if (!data.blogs || data.blogs.length === 0) return;

    container.innerHTML = data.blogs.slice(0, 3).map(b => {
      return `
        <article class="glass-panel p-6 rounded-2xl border border-white/5 hover:border-amber-500/30 transition-all flex flex-col justify-between">
          <div>
            <div class="flex items-center gap-2 mb-3">
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-400/10 text-amber-300 font-semibold border border-amber-400/20">
                ${b.category}
              </span>
              <span class="text-xs text-slate-400">${b.read_time}</span>
            </div>
            <h4 class="text-lg font-bold text-white mb-2 leading-snug">${b.title}</h4>
            <p class="text-sm text-slate-400 leading-relaxed mb-4">${b.excerpt}</p>
          </div>
          <div class="pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
            <span>By ${b.author}</span>
            <span>${b.created_at}</span>
          </div>
        </article>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading blogs:', err);
  }
};

// Modal Controls
window.openModal = function(modalId) {
  const m = document.getElementById(modalId);
  if (m) {
    m.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
};

window.closeModal = function(modalId) {
  const m = document.getElementById(modalId);
  if (m) {
    m.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
};

window.openBookingModal = function(serviceTitle = '', locality = '', dimensions = '') {
  const modal = document.getElementById('booking-modal');
  if (modal) {
    if (serviceTitle) document.getElementById('lead-service').value = serviceTitle;
    if (locality) document.getElementById('lead-location').value = locality;
    if (dimensions) document.getElementById('lead-dimensions').value = dimensions;
    openModal('booking-modal');
  }
};

// Toast notification helper
window.showToast = function(msg) {
  const toast = document.createElement('div');
  toast.className = 'fixed top-6 right-6 z-50 bg-slate-900 border border-amber-400/50 text-white text-sm px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 animate-fade-in';
  toast.innerHTML = `
    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
    <span>${msg}</span>
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 4000);
};
