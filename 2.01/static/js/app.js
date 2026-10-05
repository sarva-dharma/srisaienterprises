/**
 * TaskFlow Studio 2.0 - Management Controller
 * Kanban Drag-and-Drop, Data Table, Analytics, Checklists, Bulk Actions, and Theme Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- Application State ---
    const state = {
        currentView: 'board', // 'board', 'table', 'analytics'
        tasks: [],
        stats: {},
        filters: {
            search: '',
            category: 'All',
            priority: 'All',
            assignee: 'All',
            overdueOnly: false,
            sort: 'created_at_desc'
        },
        selectedTaskIds: new Set(),
        modalChecklist: [],
        editingTaskId: null,
        theme: localStorage.getItem('taskflow_theme') || 'dark'
    };

    // --- DOM Cache ---
    const el = {
        html: document.documentElement,
        themeToggleBtn: document.getElementById('themeToggleBtn'),

        // Nav & Dropdown
        dataDropdownBtn: document.getElementById('dataDropdownBtn'),
        dataDropdownMenu: document.getElementById('dataDropdownMenu'),
        triggerImportBtn: document.getElementById('triggerImportBtn'),
        importFileInput: document.getElementById('importFileInput'),
        resetDataBtn: document.getElementById('resetDataBtn'),
        openCreateModalBtn: document.getElementById('openCreateModalBtn'),

        // View Tabs
        tabBoard: document.getElementById('tabBoard'),
        tabTable: document.getElementById('tabTable'),
        tabAnalytics: document.getElementById('tabAnalytics'),
        boardView: document.getElementById('boardView'),
        tableView: document.getElementById('tableView'),
        analyticsView: document.getElementById('analyticsView'),
        pageTitle: document.getElementById('pageTitle'),
        pageSubtitle: document.getElementById('pageSubtitle'),

        // KPIs
        kpiTotal: document.getElementById('kpiTotal'),
        kpiInProgress: document.getElementById('kpiInProgress'),
        kpiReview: document.getElementById('kpiReview'),
        kpiCompleted: document.getElementById('kpiCompleted'),
        kpiOverdue: document.getElementById('kpiOverdue'),
        kpiOverduePill: document.getElementById('kpiOverduePill'),

        // Quick Add
        quickAddForm: document.getElementById('quickAddForm'),
        quickAddInput: document.getElementById('quickAddInput'),

        // Filters
        searchInput: document.getElementById('searchInput'),
        clearSearchBtn: document.getElementById('clearSearchBtn'),
        categoryFilter: document.getElementById('categoryFilter'),
        priorityFilter: document.getElementById('priorityFilter'),
        assigneeFilter: document.getElementById('assigneeFilter'),
        overdueFilterBtn: document.getElementById('overdueFilterBtn'),
        sortBySelect: document.getElementById('sortBySelect'),

        // Kanban Board Columns
        cardsPending: document.getElementById('cardsPending'),
        cardsInProgress: document.getElementById('cardsInProgress'),
        cardsReview: document.getElementById('cardsReview'),
        cardsCompleted: document.getElementById('cardsCompleted'),
        countPending: document.getElementById('countPending'),
        countInProgress: document.getElementById('countInProgress'),
        countReview: document.getElementById('countReview'),
        countCompleted: document.getElementById('countCompleted'),

        // Data Table
        tableTasksBody: document.getElementById('tableTasksBody'),
        selectAllCheckbox: document.getElementById('selectAllCheckbox'),
        bulkToolbar: document.getElementById('bulkToolbar'),
        bulkCountBadge: document.getElementById('bulkCountBadge'),
        bulkStatusSelect: document.getElementById('bulkStatusSelect'),
        bulkDeleteBtn: document.getElementById('bulkDeleteBtn'),
        bulkDeselectBtn: document.getElementById('bulkDeselectBtn'),

        // Analytics
        analyticsRateVal: document.getElementById('analyticsRateVal'),
        anaCompletedCount: document.getElementById('anaCompletedCount'),
        anaActiveCount: document.getElementById('anaActiveCount'),
        anaOverdueCount: document.getElementById('anaOverdueCount'),
        statusChartList: document.getElementById('statusChartList'),
        priorityChartList: document.getElementById('priorityChartList'),
        assigneeWorkloadList: document.getElementById('assigneeWorkloadList'),
        attentionCard: document.getElementById('attentionCard'),
        attentionTasksList: document.getElementById('attentionTasksList'),

        // Global Empty State
        emptyState: document.getElementById('emptyState'),
        emptyStateCreateBtn: document.getElementById('emptyStateCreateBtn'),

        // Modal
        modalOverlay: document.getElementById('taskModalOverlay'),
        modalTitle: document.getElementById('modalTitle'),
        taskForm: document.getElementById('taskForm'),
        taskIdInput: document.getElementById('taskIdInput'),
        taskTitleInput: document.getElementById('taskTitleInput'),
        taskCategoryInput: document.getElementById('taskCategoryInput'),
        taskAssigneeInput: document.getElementById('taskAssigneeInput'),
        taskPriorityInput: document.getElementById('taskPriorityInput'),
        taskStatusInput: document.getElementById('taskStatusInput'),
        taskDueDateInput: document.getElementById('taskDueDateInput'),
        taskDescInput: document.getElementById('taskDescInput'),
        modalChecklistItems: document.getElementById('modalChecklistItems'),
        modalChecklistHint: document.getElementById('modalChecklistHint'),
        newChecklistItemInput: document.getElementById('newChecklistItemInput'),
        addChecklistItemBtn: document.getElementById('addChecklistItemBtn'),
        closeModalBtn: document.getElementById('closeModalBtn'),
        cancelModalBtn: document.getElementById('cancelModalBtn'),

        // Toast Container
        toastContainer: document.getElementById('toastContainer')
    };

    // --- Helpers ---
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function getInitials(name) {
        if (!name || name === 'Unassigned') return 'UA';
        const parts = name.trim().split(' ');
        if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    function formatDueDate(dateStr) {
        if (!dateStr) return { text: 'No deadline', className: '' };
        const due = new Date(dateStr + 'T00:00:00');
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const diffTime = due - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays < 0) {
            return { text: `Overdue ${Math.abs(diffDays)}d (${dateStr})`, className: 'overdue' };
        } else if (diffDays === 0) {
            return { text: 'Due Today', className: 'today' };
        } else if (diffDays === 1) {
            return { text: 'Due Tomorrow', className: '' };
        } else {
            return { text: `Due in ${diffDays}d`, className: '' };
        }
    }

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-message">${escapeHtml(message)}</span>
            <button class="toast-close" aria-label="Dismiss">&times;</button>
        `;

        el.toastContainer.appendChild(toast);

        const dismiss = () => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 250);
        };

        toast.querySelector('.toast-close').addEventListener('click', dismiss);
        setTimeout(dismiss, 3500);
    }

    // --- Theme Controller ---
    function applyTheme(theme) {
        state.theme = theme;
        el.html.setAttribute('data-theme', theme);
        localStorage.setItem('taskflow_theme', theme);
    }

    el.themeToggleBtn.addEventListener('click', () => {
        const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
        showToast(`Switched to ${nextTheme} theme`, 'info');
    });

    applyTheme(state.theme);

    // --- Backend API Service ---
    const api = {
        async fetchTasks() {
            const params = new URLSearchParams({
                search: state.filters.search,
                category: state.filters.category,
                priority: state.filters.priority,
                assignee: state.filters.assignee,
                overdue: state.filters.overdueOnly ? 'true' : 'false',
                sort: state.filters.sort
            });

            try {
                const res = await fetch(`/api/tasks?${params.toString()}`);
                if (!res.ok) throw new Error('Could not retrieve tasks');
                const data = await res.json();
                state.tasks = data.tasks;
                renderActiveView();
            } catch (err) {
                console.error(err);
                showToast('Failed to connect to backend server', 'error');
            }
        },

        async fetchStats() {
            try {
                const res = await fetch('/api/stats');
                if (!res.ok) throw new Error('Could not retrieve stats');
                const data = await res.json();
                state.stats = data.stats;
                renderKPIs();
                updateFilterDropdowns();
                if (state.currentView === 'analytics') {
                    renderAnalytics();
                }
            } catch (err) {
                console.error(err);
            }
        },

        async createTask(payload) {
            try {
                const res = await fetch('/api/tasks', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Creation failed');
                showToast('Task added successfully', 'success');
                closeModal();
                await Promise.all([api.fetchTasks(), api.fetchStats()]);
            } catch (err) {
                showToast(err.message, 'error');
            }
        },

        async updateTask(id, payload, silent = false) {
            try {
                const res = await fetch(`/api/tasks/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Update failed');
                if (!silent) showToast('Task updated', 'success');
                closeModal();
                await Promise.all([api.fetchTasks(), api.fetchStats()]);
            } catch (err) {
                showToast(err.message, 'error');
            }
        },

        async deleteTask(id, title) {
            if (!confirm(`Delete task "${title}" permanently?`)) return;
            try {
                const res = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Delete failed');
                showToast('Task removed', 'success');
                state.selectedTaskIds.delete(id);
                updateBulkToolbar();
                await Promise.all([api.fetchTasks(), api.fetchStats()]);
            } catch (err) {
                showToast(err.message, 'error');
            }
        },

        async toggleChecklistItem(taskId, itemId) {
            try {
                const res = await fetch(`/api/tasks/${taskId}/checklist/toggle`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ itemId })
                });
                if (!res.ok) throw new Error('Checklist update failed');
                await Promise.all([api.fetchTasks(), api.fetchStats()]);
            } catch (err) {
                showToast(err.message, 'error');
            }
        },

        async bulkAction(action, extraPayload = {}) {
            const ids = Array.from(state.selectedTaskIds);
            if (ids.length === 0) return;

            try {
                const res = await fetch('/api/tasks/bulk', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action, ids, ...extraPayload })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Bulk operation failed');
                showToast(data.message, 'success');
                state.selectedTaskIds.clear();
                updateBulkToolbar();
                await Promise.all([api.fetchTasks(), api.fetchStats()]);
            } catch (err) {
                showToast(err.message, 'error');
            }
        }
    };

    // --- KPI Rendering ---
    function renderKPIs() {
        const s = state.stats;
        el.kpiTotal.textContent = s.total ?? 0;
        el.kpiInProgress.textContent = s.in_progress ?? 0;
        el.kpiReview.textContent = s.review ?? 0;
        el.kpiCompleted.textContent = s.completed ?? 0;

        const overdueCount = s.overdue ?? 0;
        el.kpiOverdue.textContent = overdueCount;
        if (overdueCount > 0) {
            el.kpiOverduePill.style.display = 'flex';
        } else {
            el.kpiOverduePill.style.display = 'none';
        }
    }

    function updateFilterDropdowns() {
        const s = state.stats;
        // Categories
        const currentCat = el.categoryFilter.value;
        let catHtml = '<option value="All">All Categories</option>';
        (s.categories || []).forEach(c => {
            const sel = c.name === currentCat ? 'selected' : '';
            catHtml += `<option value="${escapeHtml(c.name)}" ${sel}>${escapeHtml(c.name)} (${c.count})</option>`;
        });
        el.categoryFilter.innerHTML = catHtml;

        // Assignees
        const currentAss = el.assigneeFilter.value;
        let assHtml = '<option value="All">All Assignees</option>';
        (s.assignees || []).forEach(a => {
            const sel = a.name === currentAss ? 'selected' : '';
            assHtml += `<option value="${escapeHtml(a.name)}" ${sel}>${escapeHtml(a.name)} (${a.count})</option>`;
        });
        el.assigneeFilter.innerHTML = assHtml;
    }

    // --- View Switching Engine ---
    function switchView(viewName) {
        state.currentView = viewName;

        el.tabBoard.classList.toggle('active', viewName === 'board');
        el.tabTable.classList.toggle('active', viewName === 'table');
        el.tabAnalytics.classList.toggle('active', viewName === 'analytics');

        el.boardView.style.display = viewName === 'board' ? 'block' : 'none';
        el.tableView.style.display = viewName === 'table' ? 'block' : 'none';
        el.analyticsView.style.display = viewName === 'analytics' ? 'block' : 'none';

        if (viewName === 'board') {
            el.pageTitle.textContent = 'Kanban Board';
            el.pageSubtitle.textContent = 'Organize, prioritize, and drag tasks across workflow stages.';
        } else if (viewName === 'table') {
            el.pageTitle.textContent = 'Data Table & Batch Operations';
            el.pageSubtitle.textContent = 'High-density view with multi-select, bulk status changes, and sorting.';
        } else {
            el.pageTitle.textContent = 'Executive Analytics & Insights';
            el.pageSubtitle.textContent = 'Real-time velocity, stage distribution, and workload breakdown.';
        }

        renderActiveView();
    }

    el.tabBoard.addEventListener('click', () => switchView('board'));
    el.tabTable.addEventListener('click', () => switchView('table'));
    el.tabAnalytics.addEventListener('click', () => switchView('analytics'));

    function renderActiveView() {
        if (state.tasks.length === 0 && !state.filters.search && state.filters.category === 'All') {
            el.emptyState.style.display = 'block';
        } else {
            el.emptyState.style.display = 'none';
        }

        if (state.currentView === 'board') {
            renderKanbanBoard();
        } else if (state.currentView === 'table') {
            renderDataTable();
        } else if (state.currentView === 'analytics') {
            renderAnalytics();
        }
    }

    // ================= VIEW 1: KANBAN BOARD =================
    function renderKanbanBoard() {
        const columns = {
            pending: [],
            in_progress: [],
            review: [],
            completed: []
        };

        state.tasks.forEach(task => {
            const st = columns[task.status] ? task.status : 'pending';
            columns[st].push(task);
        });

        el.countPending.textContent = columns.pending.length;
        el.countInProgress.textContent = columns.in_progress.length;
        el.countReview.textContent = columns.review.length;
        el.countCompleted.textContent = columns.completed.length;

        el.cardsPending.innerHTML = renderColumnCards(columns.pending, 'pending');
        el.cardsInProgress.innerHTML = renderColumnCards(columns.in_progress, 'in_progress');
        el.cardsReview.innerHTML = renderColumnCards(columns.review, 'review');
        el.cardsCompleted.innerHTML = renderColumnCards(columns.completed, 'completed');

        attachCardEvents();
    }

    function renderColumnCards(taskList, columnStatus) {
        if (taskList.length === 0) {
            return `<div class="empty-column-hint" style="text-align:center; padding: 2rem 1rem; color: var(--text-muted); font-size: 0.8rem;">No tasks in this stage</div>`;
        }

        const stages = ['pending', 'in_progress', 'review', 'completed'];
        const currentIndex = stages.indexOf(columnStatus);

        return taskList.map(task => {
            const dueInfo = formatDueDate(task.due_date);
            const summary = task.checklist_summary || { total: 0, done: 0, percent: 0 };
            const initials = getInitials(task.assignee);

            const prevDisabled = currentIndex <= 0 ? 'disabled' : '';
            const nextDisabled = currentIndex >= stages.length - 1 ? 'disabled' : '';

            let checklistHtml = '';
            if (summary.total > 0) {
                checklistHtml = `
                    <div class="card-checklist-meter">
                        <div class="checklist-info-row">
                            <span>Subtasks</span>
                            <span>${summary.done}/${summary.total} (${summary.percent}%)</span>
                        </div>
                        <div class="checklist-bar">
                            <div class="checklist-fill" style="width: ${summary.percent}%"></div>
                        </div>
                    </div>
                `;
            }

            return `
                <div class="kanban-card" draggable="true" data-id="${task.id}" data-status="${task.status}">
                    <div class="card-tag-row">
                        <div class="tag-badges-left">
                            <span class="badge badge-subtle">${escapeHtml(task.category)}</span>
                            <span class="badge badge-priority-${escapeHtml(task.priority)}">${escapeHtml(task.priority)}</span>
                        </div>
                        <span class="badge-due ${dueInfo.className}">
                            ${escapeHtml(dueInfo.text)}
                        </span>
                    </div>

                    <h4 class="card-title">${escapeHtml(task.title)}</h4>
                    ${task.description ? `<p class="card-desc">${escapeHtml(task.description)}</p>` : ''}

                    ${checklistHtml}

                    <div class="card-meta-row">
                        <div class="assignee-avatar-wrap" title="${escapeHtml(task.assignee)}">
                            <span class="avatar-circle">${escapeHtml(initials)}</span>
                            <span>${escapeHtml(task.assignee)}</span>
                        </div>

                        <div class="card-footer-actions">
                            <button class="btn-move btn-move-left" data-id="${task.id}" data-dir="-1" ${prevDisabled} title="Move left">◀</button>
                            <button class="btn-move btn-move-right" data-id="${task.id}" data-dir="1" ${nextDisabled} title="Move right">▶</button>
                            <button class="btn btn-icon btn-sm edit-task-btn" data-id="${task.id}" title="Edit task">
                                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </button>
                            <button class="btn btn-icon btn-sm btn-icon-danger delete-task-btn" data-id="${task.id}" data-title="${escapeHtml(task.title)}" title="Delete task">
                                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    function attachCardEvents() {
        // Drag and Drop
        const cards = document.querySelectorAll('.kanban-card');
        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', card.dataset.id);
                card.classList.add('is-dragging');
            });
            card.addEventListener('dragend', () => {
                card.classList.remove('is-dragging');
            });
        });

        // Quick Stage Move Buttons
        const stages = ['pending', 'in_progress', 'review', 'completed'];
        document.querySelectorAll('.btn-move').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = parseInt(btn.dataset.id, 10);
                const dir = parseInt(btn.dataset.dir, 10);
                const task = state.tasks.find(t => t.id === id);
                if (!task) return;

                const currentIndex = stages.indexOf(task.status);
                const newIndex = currentIndex + dir;
                if (newIndex >= 0 && newIndex < stages.length) {
                    api.updateTask(id, { status: stages[newIndex] }, true);
                }
            });
        });

        // Edit Task
        document.querySelectorAll('.edit-task-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                openEditModal(parseInt(btn.dataset.id, 10));
            });
        });

        // Delete Task
        document.querySelectorAll('.delete-task-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                api.deleteTask(parseInt(btn.dataset.id, 10), btn.dataset.title);
            });
        });
    }

    // Setup Dropzones
    const dropzones = [el.cardsPending, el.cardsInProgress, el.cardsReview, el.cardsCompleted];
    dropzones.forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });
        zone.addEventListener('dragleave', () => {
            zone.classList.remove('drag-over');
        });
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');
            const taskId = parseInt(e.dataTransfer.getData('text/plain'), 10);
            const targetStatus = zone.dataset.status;
            const task = state.tasks.find(t => t.id === taskId);
            if (task && task.status !== targetStatus) {
                api.updateTask(taskId, { status: targetStatus }, true);
            }
        });
    });

    // Column "+ Add" buttons
    document.querySelectorAll('.col-add-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            openCreateModal(btn.dataset.status);
        });
    });

    // ================= VIEW 2: DATA TABLE =================
    function renderDataTable() {
        if (state.tasks.length === 0) {
            el.tableTasksBody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 2rem; color: var(--text-muted);">No tasks match the active filters</td></tr>`;
            return;
        }

        const stages = { pending: 'Backlog', in_progress: 'In Progress', review: 'In Review', completed: 'Completed' };

        el.tableTasksBody.innerHTML = state.tasks.map(task => {
            const isSelected = state.selectedTaskIds.has(task.id);
            const dueInfo = formatDueDate(task.due_date);
            const summary = task.checklist_summary || { total: 0, done: 0 };
            const initials = getInitials(task.assignee);

            return `
                <tr class="${isSelected ? 'row-selected' : ''}" data-id="${task.id}">
                    <td class="th-checkbox">
                        <input type="checkbox" class="row-checkbox" data-id="${task.id}" ${isSelected ? 'checked' : ''}>
                    </td>
                    <td>
                        <span class="badge badge-status-${escapeHtml(task.status)}">${escapeHtml(stages[task.status] || task.status)}</span>
                    </td>
                    <td>
                        <strong style="color: var(--text-primary); cursor: pointer;" class="table-task-title" data-id="${task.id}">${escapeHtml(task.title)}</strong>
                    </td>
                    <td><span class="badge badge-subtle">${escapeHtml(task.category)}</span></td>
                    <td><span class="badge badge-priority-${escapeHtml(task.priority)}">${escapeHtml(task.priority)}</span></td>
                    <td>
                        <div class="assignee-avatar-wrap">
                            <span class="avatar-circle">${escapeHtml(initials)}</span>
                            <span>${escapeHtml(task.assignee)}</span>
                        </div>
                    </td>
                    <td>
                        <span class="badge-due ${dueInfo.className}">${escapeHtml(dueInfo.text)}</span>
                    </td>
                    <td>
                        <span style="font-size: 0.78rem; color: var(--text-secondary);">${summary.total > 0 ? `${summary.done}/${summary.total} done` : '—'}</span>
                    </td>
                    <td class="th-actions">
                        <button class="btn btn-icon btn-sm edit-task-btn" data-id="${task.id}" title="Edit">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                        </button>
                        <button class="btn btn-icon btn-sm btn-icon-danger delete-task-btn" data-id="${task.id}" data-title="${escapeHtml(task.title)}" title="Delete">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        attachTableEvents();
        updateBulkToolbar();
    }

    function attachTableEvents() {
        // Individual Checkboxes
        document.querySelectorAll('.row-checkbox').forEach(box => {
            box.addEventListener('change', (e) => {
                const id = parseInt(box.dataset.id, 10);
                if (box.checked) {
                    state.selectedTaskIds.add(id);
                } else {
                    state.selectedTaskIds.delete(id);
                }
                updateBulkToolbar();
                box.closest('tr').classList.toggle('row-selected', box.checked);
            });
        });

        // Title click to edit
        document.querySelectorAll('.table-task-title').forEach(t => {
            t.addEventListener('click', () => openEditModal(parseInt(t.dataset.id, 10)));
        });

        // Edit and delete buttons in table
        el.tableTasksBody.querySelectorAll('.edit-task-btn').forEach(btn => {
            btn.addEventListener('click', () => openEditModal(parseInt(btn.dataset.id, 10)));
        });

        el.tableTasksBody.querySelectorAll('.delete-task-btn').forEach(btn => {
            btn.addEventListener('click', () => api.deleteTask(parseInt(btn.dataset.id, 10), btn.dataset.title));
        });
    }

    // Select All Checkbox
    el.selectAllCheckbox.addEventListener('change', () => {
        const checked = el.selectAllCheckbox.checked;
        state.tasks.forEach(t => {
            if (checked) state.selectedTaskIds.add(t.id);
            else state.selectedTaskIds.delete(t.id);
        });
        renderDataTable();
    });

    function updateBulkToolbar() {
        const count = state.selectedTaskIds.size;
        if (count > 0) {
            el.bulkToolbar.style.display = 'flex';
            el.bulkCountBadge.textContent = `${count} task${count === 1 ? '' : 's'} selected`;
        } else {
            el.bulkToolbar.style.display = 'none';
            el.selectAllCheckbox.checked = false;
        }
    }

    el.bulkStatusSelect.addEventListener('change', () => {
        const newStatus = el.bulkStatusSelect.value;
        if (newStatus) {
            api.bulkAction('update_status', { status: newStatus });
            el.bulkStatusSelect.value = '';
        }
    });

    el.bulkDeleteBtn.addEventListener('click', () => {
        const count = state.selectedTaskIds.size;
        if (confirm(`Are you sure you want to delete ${count} selected tasks?`)) {
            api.bulkAction('delete');
        }
    });

    el.bulkDeselectBtn.addEventListener('click', () => {
        state.selectedTaskIds.clear();
        updateBulkToolbar();
        renderDataTable();
    });

    // ================= VIEW 3: ANALYTICS DASHBOARD =================
    function renderAnalytics() {
        const s = state.stats;
        const rate = s.completion_rate || 0;
        el.analyticsRateVal.textContent = `${rate}%`;

        // Update conic gradient ring
        const ring = document.querySelector('.progress-ring-container');
        if (ring) {
            ring.style.background = `conic-gradient(var(--completed-color) ${rate}%, var(--bg-input) ${rate}% 100%)`;
        }

        el.anaCompletedCount.textContent = s.completed || 0;
        el.anaActiveCount.textContent = (s.in_progress || 0) + (s.review || 0);
        el.anaOverdueCount.textContent = s.overdue || 0;

        // Stage Distribution
        const stagesMap = [
            { label: 'Backlog / Pending', count: s.pending || 0, color: 'var(--pending-color)' },
            { label: 'In Progress', count: s.in_progress || 0, color: 'var(--in_progress-color)' },
            { label: 'In Review', count: s.review || 0, color: 'var(--review-color)' },
            { label: 'Completed', count: s.completed || 0, color: 'var(--completed-color)' }
        ];

        const total = s.total || 1;
        el.statusChartList.innerHTML = stagesMap.map(st => {
            const pct = Math.round((st.count / total) * 100);
            return `
                <div class="chart-bar-item">
                    <div class="chart-bar-header">
                        <span>${st.label}</span>
                        <span>${st.count} (${pct}%)</span>
                    </div>
                    <div class="chart-bar-track">
                        <div class="chart-bar-fill" style="width: ${pct}%; background-color: ${st.color};"></div>
                    </div>
                </div>
            `;
        }).join('');

        // Priority Breakdown
        const prioritiesMap = [
            { label: 'Urgent', color: 'var(--urgent-color)' },
            { label: 'High', color: 'var(--high-color)' },
            { label: 'Medium', color: 'var(--medium-color)' },
            { label: 'Low', color: 'var(--low-color)' }
        ];

        const pData = s.priorities || [];
        el.priorityChartList.innerHTML = prioritiesMap.map(p => {
            const found = pData.find(item => item.name === p.label);
            const count = found ? found.count : 0;
            const pct = Math.round((count / total) * 100);
            return `
                <div class="chart-bar-item">
                    <div class="chart-bar-header">
                        <span>${p.label} Priority</span>
                        <span>${count} (${pct}%)</span>
                    </div>
                    <div class="chart-bar-track">
                        <div class="chart-bar-fill" style="width: ${pct}%; background-color: ${p.color};"></div>
                    </div>
                </div>
            `;
        }).join('');

        // Assignee Workload
        const assignees = s.assignees || [];
        el.assigneeWorkloadList.innerHTML = assignees.map(a => {
            const inits = getInitials(a.name);
            return `
                <div class="workload-item">
                    <div class="workload-user">
                        <span class="avatar-circle">${escapeHtml(inits)}</span>
                        <span>${escapeHtml(a.name)}</span>
                    </div>
                    <span class="workload-count">${a.count} task${a.count === 1 ? '' : 's'}</span>
                </div>
            `;
        }).join('');

        // Overdue & Urgent Action Items
        const urgentOrOverdue = state.tasks.filter(t => {
            if (t.status === 'completed') return false;
            const dueInfo = formatDueDate(t.due_date);
            return t.priority === 'Urgent' || dueInfo.className === 'overdue';
        });

        if (urgentOrOverdue.length > 0) {
            el.attentionCard.style.display = 'block';
            el.attentionTasksList.innerHTML = urgentOrOverdue.map(t => {
                const dueInfo = formatDueDate(t.due_date);
                return `
                    <div class="attention-task-row">
                        <div>
                            <strong style="color: var(--text-primary);">${escapeHtml(t.title)}</strong>
                            <span class="badge badge-priority-${escapeHtml(t.priority)}" style="margin-left: 0.5rem;">${escapeHtml(t.priority)}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span class="badge-due ${dueInfo.className}">${escapeHtml(dueInfo.text)}</span>
                            <button class="btn btn-sm btn-secondary" onclick="document.dispatchEvent(new CustomEvent('editTask', { detail: ${t.id} }))">View</button>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            el.attentionCard.style.display = 'none';
        }
    }

    document.addEventListener('editTask', (e) => openEditModal(e.detail));

    // ================= FRICTIONLESS QUICK ADD =================
    el.quickAddForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = el.quickAddInput.value.trim();
        if (!title) return;

        api.createTask({
            title,
            category: state.filters.category !== 'All' ? state.filters.category : 'General',
            priority: 'Medium',
            status: 'pending'
        });

        el.quickAddInput.value = '';
    });

    // ================= MODAL & CHECKLIST BUILDER =================
    function openCreateModal(initialStatus = 'pending') {
        state.editingTaskId = null;
        state.modalChecklist = [];
        el.modalTitle.textContent = 'Create New Task';
        el.taskForm.reset();
        el.taskIdInput.value = '';
        el.taskPriorityInput.value = 'Medium';
        el.taskStatusInput.value = initialStatus;
        el.taskAssigneeInput.value = 'Unassigned';
        renderModalChecklist();
        el.modalOverlay.classList.add('active');
        el.modalOverlay.setAttribute('aria-hidden', 'false');
        setTimeout(() => el.taskTitleInput.focus(), 100);
    }

    function openEditModal(taskId) {
        const task = state.tasks.find(t => t.id === taskId);
        if (!task) return;

        state.editingTaskId = taskId;
        state.modalChecklist = JSON.parse(JSON.stringify(task.checklist || []));
        el.modalTitle.textContent = `Edit Task #${taskId}`;
        el.taskIdInput.value = task.id;
        el.taskTitleInput.value = task.title;
        el.taskCategoryInput.value = task.category;
        el.taskAssigneeInput.value = task.assignee;
        el.taskPriorityInput.value = task.priority;
        el.taskStatusInput.value = task.status;
        el.taskDueDateInput.value = task.due_date || '';
        el.taskDescInput.value = task.description || '';

        renderModalChecklist();
        el.modalOverlay.classList.add('active');
        el.modalOverlay.setAttribute('aria-hidden', 'false');
        setTimeout(() => el.taskTitleInput.focus(), 100);
    }

    function closeModal() {
        el.modalOverlay.classList.remove('active');
        el.modalOverlay.setAttribute('aria-hidden', 'true');
        state.editingTaskId = null;
        state.modalChecklist = [];
    }

    function renderModalChecklist() {
        const items = state.modalChecklist;
        const total = items.length;
        const done = items.filter(i => i.done).length;
        el.modalChecklistHint.textContent = `${done}/${total} completed`;

        el.modalChecklistItems.innerHTML = items.map((item, idx) => `
            <div class="checklist-item-row ${item.done ? 'is-done' : ''}">
                <input type="checkbox" data-idx="${idx}" ${item.done ? 'checked' : ''}>
                <span>${escapeHtml(item.text)}</span>
                <button type="button" class="btn-delete-check" data-idx="${idx}">&times;</button>
            </div>
        `).join('');

        // Checklist item events
        el.modalChecklistItems.querySelectorAll('input[type="checkbox"]').forEach(box => {
            box.addEventListener('change', () => {
                const idx = parseInt(box.dataset.idx, 10);
                items[idx].done = box.checked;
                renderModalChecklist();
            });
        });

        el.modalChecklistItems.querySelectorAll('.btn-delete-check').forEach(btn => {
            btn.addEventListener('click', () => {
                const idx = parseInt(btn.dataset.idx, 10);
                items.splice(idx, 1);
                renderModalChecklist();
            });
        });
    }

    function addModalChecklistItem() {
        const text = el.newChecklistItemInput.value.trim();
        if (!text) return;
        const newId = state.modalChecklist.length > 0 ? Math.max(...state.modalChecklist.map(i => i.id || 0)) + 1 : 1;
        state.modalChecklist.push({ id: newId, text, done: false });
        el.newChecklistItemInput.value = '';
        renderModalChecklist();
    }

    el.addChecklistItemBtn.addEventListener('click', addModalChecklistItem);
    el.newChecklistItemInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addModalChecklistItem();
        }
    });

    el.taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = el.taskTitleInput.value.trim();
        if (!title) {
            showToast('Task title is required', 'error');
            return;
        }

        const payload = {
            title,
            category: el.taskCategoryInput.value.trim() || 'General',
            assignee: el.taskAssigneeInput.value.trim() || 'Unassigned',
            priority: el.taskPriorityInput.value,
            status: el.taskStatusInput.value,
            due_date: el.taskDueDateInput.value || null,
            description: el.taskDescInput.value.trim(),
            checklist: state.modalChecklist
        };

        if (state.editingTaskId) {
            api.updateTask(state.editingTaskId, payload);
        } else {
            api.createTask(payload);
        }
    });

    el.openCreateModalBtn.addEventListener('click', () => openCreateModal());
    el.emptyStateCreateBtn.addEventListener('click', () => openCreateModal());
    el.closeModalBtn.addEventListener('click', closeModal);
    el.cancelModalBtn.addEventListener('click', closeModal);

    el.modalOverlay.addEventListener('click', (e) => {
        if (e.target === el.modalOverlay) closeModal();
    });

    // ================= CONTROLS & FILTERING =================
    let searchTimer = null;
    el.searchInput.addEventListener('input', (e) => {
        const val = e.target.value.trim();
        state.filters.search = val;
        el.clearSearchBtn.style.display = val ? 'block' : 'none';
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => api.fetchTasks(), 250);
    });

    el.clearSearchBtn.addEventListener('click', () => {
        el.searchInput.value = '';
        el.clearSearchBtn.style.display = 'none';
        state.filters.search = '';
        api.fetchTasks();
    });

    el.categoryFilter.addEventListener('change', (e) => {
        state.filters.category = e.target.value;
        api.fetchTasks();
    });

    el.priorityFilter.addEventListener('change', (e) => {
        state.filters.priority = e.target.value;
        api.fetchTasks();
    });

    el.assigneeFilter.addEventListener('change', (e) => {
        state.filters.assignee = e.target.value;
        api.fetchTasks();
    });

    el.overdueFilterBtn.addEventListener('click', () => {
        state.filters.overdueOnly = !state.filters.overdueOnly;
        el.overdueFilterBtn.classList.toggle('btn-primary', state.filters.overdueOnly);
        el.overdueFilterBtn.classList.toggle('btn-secondary', !state.filters.overdueOnly);
        api.fetchTasks();
    });

    el.sortBySelect.addEventListener('change', (e) => {
        state.filters.sort = e.target.value;
        api.fetchTasks();
    });

    // ================= DATA DROPDOWN & EXPORT / IMPORT =================
    el.dataDropdownBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        el.dataDropdownMenu.classList.toggle('active');
    });

    document.addEventListener('click', () => {
        el.dataDropdownMenu.classList.remove('active');
    });

    el.triggerImportBtn.addEventListener('click', () => {
        el.importFileInput.click();
    });

    el.importFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async (evt) => {
            try {
                const parsed = JSON.parse(evt.target.result);
                if (!Array.isArray(parsed)) throw new Error('File must contain a JSON array of tasks');

                const res = await fetch('/api/tasks/import', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(parsed)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Import failed');
                showToast(data.message, 'success');
                await Promise.all([api.fetchTasks(), api.fetchStats()]);
            } catch (err) {
                showToast(`Import error: ${err.message}`, 'error');
            } finally {
                el.importFileInput.value = '';
            }
        };
        reader.readAsText(file);
    });

    el.resetDataBtn.addEventListener('click', async () => {
        if (!confirm('Reset all tasks to fresh demo management data? Any custom tasks will be overwritten.')) return;
        try {
            const res = await fetch('/api/reset-data', { method: 'POST' });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Reset failed');
            showToast(data.message, 'info');
            await Promise.all([api.fetchTasks(), api.fetchStats()]);
        } catch (err) {
            showToast(err.message, 'error');
        }
    });

    // ================= KEYBOARD SHORTCUTS =================
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (el.modalOverlay.classList.contains('active')) closeModal();
            if (state.selectedTaskIds.size > 0) {
                state.selectedTaskIds.clear();
                updateBulkToolbar();
                renderDataTable();
            }
        } else if (e.key === '/' && document.activeElement !== el.searchInput && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            el.searchInput.focus();
        } else if (e.key === 'n' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            openCreateModal();
        }
    });

    // Initial Load
    api.fetchStats();
    api.fetchTasks();
});
