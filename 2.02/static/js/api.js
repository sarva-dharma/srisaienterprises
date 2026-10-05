/**
 * Bengaluru Sanctions API Client
 */
const API = {
  // Public
  async getServices() {
    const res = await fetch('/api/services');
    return res.json();
  },

  async getJurisdictions() {
    const res = await fetch('/api/jurisdictions');
    return res.json();
  },

  async checkJurisdiction(payload) {
    const res = await fetch('/api/jurisdictions/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async calculateEstimate(payload) {
    const res = await fetch('/api/calculator/estimate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async submitLead(payload) {
    const res = await fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async getBlogs() {
    const res = await fetch('/api/blogs');
    return res.json();
  },

  // Auth
  async login(email, password) {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    return res.json();
  },

  async register(payload) {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async checkMe() {
    const res = await fetch('/api/auth/me');
    return res.json();
  },

  async logout() {
    const res = await fetch('/api/auth/logout', { method: 'POST' });
    return res.json();
  },

  // Client Portal
  async getClientProjects(referenceNo = '') {
    const url = referenceNo ? `/api/client/projects?reference_no=${encodeURIComponent(referenceNo)}` : '/api/client/projects';
    const res = await fetch(url);
    return res.json();
  },

  // Admin CRM & CMS
  async getAdminMetrics() {
    const res = await fetch('/api/admin/metrics');
    return res.json();
  },

  async getAdminLeads(status = '') {
    const url = status ? `/api/admin/leads?status=${encodeURIComponent(status)}` : '/api/admin/leads';
    const res = await fetch(url);
    return res.json();
  },

  async updateLead(leadId, payload) {
    const res = await fetch(`/api/admin/leads/${leadId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async getAdminProjects() {
    const res = await fetch('/api/admin/projects');
    return res.json();
  },

  async createAdminProject(payload) {
    const res = await fetch('/api/admin/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async updateProjectStage(projectId, stage, remarks) {
    const res = await fetch(`/api/admin/projects/${projectId}/stage`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stage, remarks })
    });
    return res.json();
  },

  async getAdminServices() {
    const res = await fetch('/api/admin/services');
    return res.json();
  },

  async updateService(serviceId, payload) {
    const res = await fetch(`/api/admin/services/${serviceId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async createService(payload) {
    const res = await fetch('/api/admin/services', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  }
};
