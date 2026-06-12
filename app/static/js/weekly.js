/**
 * HÜrus Operacional - Quadro Semanal
 * Gerenciamento do quadro interativo
 */

// Estado global
let currentWeekId = null;
let currentBoard = null;
let changes = [];
let isSupervisor = window.IS_SUPERVISOR || false;

// InicializaÜÜo
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // Seletor de projeto
    const projectSelect = document.getElementById('projectSelect');
    if (projectSelect) {
        projectSelect.addEventListener('change', onProjectChange);
    }
    
    // BotÜo carregar
    const loadBtn = document.getElementById('loadBtn');
    if (loadBtn) {
        loadBtn.addEventListener('click', loadBoard);
    }
    
    // BotÜo salvar
    const saveBtn = document.getElementById('saveBtn');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveChanges);
    }
    
    // Gerar planejamento
    const generateSubmitBtn = document.getElementById('generateSubmitBtn');
    if (generateSubmitBtn) {
        generateSubmitBtn.addEventListener('click', generatePlanning);
    }
    
    // Aplicar feriado
    const holidaySubmitBtn = document.getElementById('holidaySubmitBtn');
    if (holidaySubmitBtn) {
        holidaySubmitBtn.addEventListener('click', applyHoliday);
    }
}

/**
 * Ao mudar projeto, carregar semanas
 */
async function onProjectChange() {
    const projectId = document.getElementById('projectSelect').value;
    const weekSelect = document.getElementById('weekSelect');
    
    if (!projectId) {
        weekSelect.innerHTML = '<option value="">Selecione uma semana</option>';
        weekSelect.disabled = true;
        document.getElementById('loadBtn').disabled = true;
        return;
    }
    
    try {
        const response = await fetch(`/weekly/api/weeks?project_id=${projectId}`);
        const weeks = await response.json();
        
        weekSelect.innerHTML = '<option value="">Selecione uma semana</option>';
        weeks.forEach(week => {
            const option = document.createElement('option');
            option.value = week.id;
            option.textContent = `${week.label} Ü ${formatDate(week.start_date)} a ${formatDate(week.end_date)}`;
            weekSelect.appendChild(option);
        });
        
        weekSelect.disabled = false;
        weekSelect.addEventListener('change', function() {
            document.getElementById('loadBtn').disabled = !this.value;
        });
        
    } catch (error) {
        console.error('Erro ao carregar semanas:', error);
        showToast('Erro ao carregar semanas', 'danger');
    }
}

/**
 * Carregar quadro semanal
 */
async function loadBoard() {
    const weekId = document.getElementById('weekSelect').value;
    
    if (!weekId) {
        showToast('Selecione uma semana', 'warning');
        return;
    }
    
    currentWeekId = weekId;
    changes = [];
    
    try {
        const response = await fetch(`/weekly/api/load?week_id=${weekId}`);
        const data = await response.json();
        
        currentBoard = data;
        renderBoard(data);
        updateMetrics(data.metrics);
        renderHolidays(data.holidays, data.week);
        
        // Mostrar seÜÜes
        document.getElementById('placeholderSection').style.display = 'none';
        document.getElementById('boardSection').style.display = 'block';
        document.getElementById('metricsSection').style.display = 'flex';
        
        // Habilitar botÜes
        if (isSupervisor) {
            document.getElementById('saveBtn').disabled = false;
        }
        
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.href = `/weekly/export/csv?week_id=${weekId}`;
            exportBtn.classList.remove('disabled');
        }
        
        showToast('Quadro carregado!', 'success');
        
    } catch (error) {
        console.error('Erro ao carregar quadro:', error);
        showToast('Erro ao carregar quadro', 'danger');
    }
}

/**
 * Renderizar quadro
 */
function renderBoard(data) {
    const tbody = document.getElementById('boardBody');
    tbody.innerHTML = '';
    
    // Atualizar tÜtulo
    document.getElementById('boardTitle').textContent = 
        `${data.week.project} Ü ${data.week.label}`;
    document.getElementById('boardSubtitle').textContent = 
        `${formatDate(data.week.start_date)} a ${formatDate(data.week.end_date)} Ü GestÜo por exceÜÜo`;
    
    // Atualizar headers com datas
    const startDate = new Date(data.week.start_date + 'T00:00:00');
    const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    const weekdaysPt = ['Segunda', 'TerÜa', 'Quarta', 'Quinta', 'Sexta'];
    
    weekdays.forEach((day, i) => {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);
        const dateStr = date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
        document.getElementById(`th${day}`).innerHTML = `${weekdaysPt[i]}<br><span class="fw-normal text-muted">${dateStr}</span>`;
    });
    
    // Renderizar linhas
    data.attendances.forEach(att => {
        const tr = document.createElement('tr');
        tr.dataset.id = att.id;
        
        // Calcular assiduidade individual
        const attendanceRate = att.attendance_rate || 0;
        const rateColor = attendanceRate >= 90 ? 'success' : attendanceRate >= 75 ? 'warning' : 'danger';
        
        tr.innerHTML = `
            <td>
                <div class="name">${att.professional.name}</div>
                <small class="text-muted">${attendanceRate.toFixed(1)}% assiduidade</small>
            </td>
            <td><span class="badge text-bg-light">${att.professional.registration}</span></td>
            <td>${renderDayCell('monday', att.monday, att.monday_activities, att.id)}</td>
            <td>${renderDayCell('tuesday', att.tuesday, att.tuesday_activities, att.id)}</td>
            <td>${renderDayCell('wednesday', att.wednesday, att.wednesday_activities, att.id)}</td>
            <td>${renderDayCell('thursday', att.thursday, att.thursday_activities, att.id)}</td>
            <td>${renderDayCell('friday', att.friday, att.friday_activities, att.id)}</td>
            <td>
                <input type="text" class="form-control form-control-sm" 
                       data-id="${att.id}" data-field="notes" 
                       value="${att.notes}" 
                       placeholder="Sem observaÜÜo"
                       ${!isSupervisor ? 'readonly' : ''}>
            </td>
        `;
        
        tbody.appendChild(tr);
    });
    
    // Adicionar listeners
    if (isSupervisor) {
        tbody.querySelectorAll('select, input').forEach(el => {
            el.addEventListener('change', trackChange);
        });
    }
    
    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Renderizar cÜlula de dia com status e atividades
 */
function renderDayCell(day, currentStatus, activities, attId) {
    const hasActivities = activities && activities.trim().length > 0;
    
    // Parse atividades (separadas por \n)
    const activityList = hasActivities ? activities.split('\n').filter(a => a.trim()) : [];
    
    const statuses = [
        'Presente',
        'Falta justificada',
        'Falta nÜo justificada',
        'SaÜda antecipada',
        'Realocado',
        'Feriado',
        'Folga',
        'NÜo planejado'
    ];
    
    let html = '<div class="day-cell">';
    
    // Status select ou badge
    if (!isSupervisor) {
        const statusClass = statusClasses[currentStatus] || 's-presente';
        html += `<span class="badge ${statusClass} mb-2">${currentStatus}</span>`;
    } else {
        html += `<select class="form-select form-select-sm status-select ${statusClasses[currentStatus]} mb-2" 
                        data-id="${attId}" data-field="${day}">`;
        statuses.forEach(status => {
            const selected = status === currentStatus ? 'selected' : '';
            html += `<option value="${status}" ${selected}>${status}</option>`;
        });
        html += '</select>';
    }
    
    // Cards de atividades
    if (hasActivities) {
        html += '<div class="activities-container">';
        activityList.forEach((activity, index) => {
            // Limitar exibiÜÜo a 3 atividades, resto mostra contador
            if (index < 3) {
                // Extrair categoria (antes do :)
                const parts = activity.split(':');
                const category = parts[0].trim();
                const description = parts.slice(1).join(':').trim();
                
                html += `<div class="activity-card">
                    <div class="activity-category">${category}</div>
                    <div class="activity-desc">${description.substring(0, 80)}${description.length > 80 ? '...' : ''}</div>
                </div>`;
            }
        });
        
        if (activityList.length > 3) {
            html += `<div class="activity-more">+${activityList.length - 3} atividades</div>`;
        }
        
        html += '</div>';
    } else {
        html += '<div class="no-activities">Sem atividades</div>';
    }
    
    html += '</div>';
    return html;
}

/**
 * Renderizar select de status (legado - mantido para compatibilidade)
 */
function renderStatusSelect(day, currentStatus, attId) {
    return renderDayCell(day, currentStatus, '', attId);
}

/**
 * Rastrear mudanÜa
 */
function trackChange(e) {
    const id = parseInt(e.target.dataset.id);
    const field = e.target.dataset.field;
    const value = e.target.value;
    
    // Encontrar ou criar registro de mudanÜa
    let change = changes.find(c => c.id === id);
    if (!change) {
        change = { id: id };
        changes.push(change);
    }
    
    change[field] = value;
    
    // Atualizar cor do select se for status
    if (e.target.tagName === 'SELECT') {
        Object.values(statusClasses).forEach(c => e.target.classList.remove(c));
        e.target.classList.add(statusClasses[value] || 's-presente');
    }
    
    console.log('MudanÜas pendentes:', changes.length);
}

/**
 * Salvar mudanÜas
 */
async function saveChanges() {
    if (changes.length === 0) {
        showToast('Nenhuma alteraÜÜo para salvar', 'info');
        return;
    }
    
    try {
        const response = await fetch('/weekly/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                week_id: currentWeekId,
                changes: changes
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(result.message, 'success');
            changes = [];
            // Recarregar para atualizar mÜtricas
            loadBoard();
        } else {
            showToast(result.error || 'Erro ao salvar', 'danger');
        }
        
    } catch (error) {
        console.error('Erro ao salvar:', error);
        showToast('Erro ao salvar alteraÜÜes', 'danger');
    }
}

/**
 * Gerar planejamento
 */
async function generatePlanning() {
    const projectId = document.getElementById('genProject').value;
    const label = document.getElementById('genLabel').value;
    const startDate = document.getElementById('genStartDate').value;
    const endDate = document.getElementById('genEndDate').value;
    
    if (!projectId || !label || !startDate || !endDate) {
        showToast('Preencha todos os campos', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/weekly/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: parseInt(projectId),
                week_label: label,
                start_date: startDate,
                end_date: endDate
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('generateModal')).hide();
            
            // Recarregar semanas do projeto
            document.getElementById('projectSelect').value = projectId;
            await onProjectChange();
            document.getElementById('weekSelect').value = result.week_id;
            document.getElementById('loadBtn').disabled = false;
            
        } else {
            showToast(result.error || 'Erro ao gerar planejamento', 'danger');
        }
        
    } catch (error) {
        console.error('Erro ao gerar planejamento:', error);
        showToast('Erro ao gerar planejamento', 'danger');
    }
}

/**
 * Aplicar feriado
 */
async function applyHoliday() {
    const weekday = document.getElementById('holidayWeekday').value;
    const description = document.getElementById('holidayDescription').value;
    
    if (!weekday || !description) {
        showToast('Preencha todos os campos', 'warning');
        return;
    }
    
    if (!currentWeekId) {
        showToast('Carregue um quadro primeiro', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/weekly/api/holiday/apply', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                week_id: currentWeekId,
                weekday: weekday,
                description: description
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('holidayModal')).hide();
            
            // Limpar form
            document.getElementById('holidayForm').reset();
            
            // Recarregar quadro
            loadBoard();
            
        } else {
            showToast(result.error || 'Erro ao aplicar feriado', 'danger');
        }
        
    } catch (error) {
        console.error('Erro ao aplicar feriado:', error);
        showToast('Erro ao aplicar feriado', 'danger');
    }
}

/**
 * Renderizar feriados
 */
function renderHolidays(holidays, week) {
    const container = document.getElementById('holidaysContainer');
    container.innerHTML = '';
    
    if (holidays.length === 0) return;
    
    const weekdaysPt = {
        'Monday': 'segunda-feira',
        'Tuesday': 'terÜa-feira',
        'Wednesday': 'quarta-feira',
        'Thursday': 'quinta-feira',
        'Friday': 'sexta-feira'
    };
    
    holidays.forEach(holiday => {
        const div = document.createElement('div');
        div.className = 'holiday-alert';
        div.innerHTML = `
            <i class="bi bi-sun me-2"></i>
            <strong>Feriado informado:</strong> ${weekdaysPt[holiday.weekday]}, ${formatDate(holiday.date)} Ü? ${holiday.description}
            ${isSupervisor ? `<button class="btn btn-sm btn-outline-danger float-end" onclick="removeHoliday(${holiday.id})">
                <i class="bi bi-x"></i> Remover
            </button>` : ''}
        `;
        container.appendChild(div);
    });
}

/**
 * Remover feriado
 */
async function removeHoliday(holidayId) {
    if (!confirm('Remover este feriado?')) return;
    
    try {
        const response = await fetch('/weekly/api/holiday/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ holiday_id: holidayId })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast(result.message, 'success');
            loadBoard();
        } else {
            showToast(result.error || 'Erro ao remover feriado', 'danger');
        }
        
    } catch (error) {
        console.error('Erro ao remover feriado:', error);
        showToast('Erro ao remover feriado', 'danger');
    }
}

/**
 * Atualizar mÜtricas
 */
function updateMetrics(metrics) {
    document.getElementById('metricRate').textContent = 
        metrics.rate ? `${metrics.rate}%` : 'N/A';
    document.getElementById('metricPeople').textContent = metrics.professionals;
    document.getElementById('metricFaltaJ').textContent = metrics.falta_justificada;
    document.getElementById('metricFaltaNJ').textContent = metrics.falta_nao_justificada;
    document.getElementById('metricRealoc').textContent = metrics.realocacoes;
    document.getElementById('metricFeriados').textContent = metrics.feriados;
}

/**
 * Formatar data
 */
function formatDate(dateStr) {
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
}
