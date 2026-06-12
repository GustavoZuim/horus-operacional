/**
 * Hórus Operacional - JavaScript Core
 * LÜgica de cÜlculo de assiduidade
 */

// Status e suas classificações
const statuses = [
  "Presente",
  "Falta justificada",
  "Falta não justificada",
  "SaÜda antecipada",
  "Realocado",
  "Feriado",
  "Folga",
  "NÜo planejado"
];

const statusClasses = {
  "Presente": "s-presente",
  "Falta justificada": "s-falta-j",
  "Falta não justificada": "s-falta-nj",
  "SaÜda antecipada": "s-saida",
  "Realocado": "s-realocado",
  "Feriado": "s-feriado",
  "Folga": "s-folga",
  "NÜo planejado": "s-nao"
};

// Status que entram no denominador
const validDays = new Set([
  "Presente",
  "Falta justificada",
  "Falta não justificada",
  "SaÜda antecipada",
  "Realocado"
]);

// Status que contam como presenÜa
const presentDays = new Set([
  "Presente",
  "SaÜda antecipada",
  "Realocado"
]);

/**
 * Mostra toast de feedback
 */
function showToast(message, type = 'dark') {
  const toastEl = document.getElementById('toast');
  const toastText = document.getElementById('toastText');
  
  if (toastEl && toastText) {
    toastText.textContent = message;
    
    // Trocar classe de cor se necessÜrio
    toastEl.className = `toast align-items-center text-bg-${type} border-0`;
    
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }
}

/**
 * Calcula taxa de assiduidade
 */
function calculateAttendanceRate(validCount, presentCount) {
  if (validCount === 0) {
    return null; // N/A
  }
  return (presentCount / validCount) * 100;
}

/**
 * Formata taxa de assiduidade para exibição
 */
function formatRate(rate) {
  if (rate === null) {
    return 'N/A';
  }
  return rate.toFixed(2).replace('.', ',') + '%';
}

/**
 * Retorna classe de badge baseado na taxa
 */
function getRateBadgeClass(rate) {
  if (rate === null) return 'text-bg-secondary';
  if (rate >= 90) return 'text-bg-success';
  if (rate >= 75) return 'text-bg-warning';
  return 'text-bg-danger';
}
