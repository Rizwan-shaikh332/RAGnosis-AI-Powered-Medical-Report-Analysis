// App-wide design tokens — matching RAGnosis dark theme
export const COLORS = {
    bg: '#0d1117',
    card: '#161b22',
    border: '#30363d',
    primary: '#7c3aed',
    primaryLight: 'rgba(124,58,237,0.15)',
    textPrimary: '#e6edf3',
    textSecond: '#8b949e',
    textMuted: '#484f58',
    green: '#10b981',
    red: '#ef4444',
    yellow: '#f59e0b',
    cyan: '#22d3ee',
};

export const STATUS_COLORS = {
    high: { bg: 'rgba(239,68,68,0.12)', text: '#ef4444', border: '#ef4444', chip: 'HIGH ↑' },
    low: { bg: 'rgba(251,191,36,0.12)', text: '#f59e0b', border: '#f59e0b', chip: 'LOW ↓' },
    normal: { bg: 'rgba(16,185,129,0.12)', text: '#10b981', border: '#10b981', chip: 'NORMAL ✓' },
};

export const METRIC_CATALOG = {
    hemoglobin: { label: 'Hemoglobin', unit: 'g/dL', lo: 12, hi: 17 },
    glucose: { label: 'Blood Glucose', unit: 'mg/dL', lo: 70, hi: 100 },
    cholesterol: { label: 'Total Cholesterol', unit: 'mg/dL', lo: 100, hi: 200 },
    triglycerides: { label: 'Triglycerides', unit: 'mg/dL', lo: 0, hi: 150 },
    hdl: { label: 'HDL (Good Chol.)', unit: 'mg/dL', lo: 60, hi: 999 },
    ldl: { label: 'LDL (Bad Chol.)', unit: 'mg/dL', lo: 0, hi: 100 },
    wbc: { label: 'WBC', unit: 'k/µL', lo: 4.5, hi: 11 },
    rbc: { label: 'RBC', unit: 'M/µL', lo: 4.0, hi: 5.5 },
    platelets: { label: 'Platelets', unit: 'k/µL', lo: 150, hi: 400 },
    creatinine: { label: 'Creatinine', unit: 'mg/dL', lo: 0.5, hi: 1.2 },
    urea: { label: 'Blood Urea (BUN)', unit: 'mg/dL', lo: 7, hi: 20 },
    sgpt: { label: 'SGPT (ALT)', unit: 'U/L', lo: 7, hi: 56 },
    sgot: { label: 'SGOT (AST)', unit: 'U/L', lo: 10, hi: 40 },
    tsh: { label: 'TSH (Thyroid)', unit: 'mIU/L', lo: 0.4, hi: 4.0 },
    systolic_bp: { label: 'Systolic BP', unit: 'mmHg', lo: 90, hi: 120 },
    diastolic_bp: { label: 'Diastolic BP', unit: 'mmHg', lo: 60, hi: 80 },
    mcv: { label: 'MCV', unit: 'fl', lo: 80, hi: 100 },
    mch: { label: 'MCH', unit: 'pg', lo: 27, hi: 33 },
    haematocrit: { label: 'Haematocrit (PCV)', unit: '%', lo: 36, hi: 48 },
};

export function getMetricStatus(key, value) {
    const m = METRIC_CATALOG[key];
    if (!m) return null;
    const status = value < m.lo ? 'low' : value > m.hi ? 'high' : 'normal';
    const dLo = m.lo - (m.hi - m.lo) * 0.4;
    const dHi = m.hi + (m.hi - m.lo) * 0.4;
    const rng = dHi - dLo;
    const pct = rng ? Math.max(0, Math.min(100, (value - dLo) / rng * 100)) : 50;
    const loPct = rng ? Math.max(0, Math.min(100, (m.lo - dLo) / rng * 100)) : 20;
    const hiPct = rng ? Math.max(0, Math.min(100, (m.hi - dLo) / rng * 100)) : 80;
    return {
        key, label: m.label, value, unit: m.unit, status,
        normal_range: `${m.lo}–${m.hi > 900 ? '∞' : m.hi} ${m.unit}`, pct, loPct, hiPct
    };
}
