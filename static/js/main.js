/**
 * Main JavaScript utilities for AI Student Performance Prediction System
 */

document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 6000);
    });

    // Preset test scenario filler for Prediction page
    const sampleButtons = document.querySelectorAll('.btn-load-sample');
    sampleButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const type = this.getAttribute('data-sample-type');
            fillPredictionSample(type);
        });
    });
});

/**
 * Quick fill helper for testing prediction scenarios
 */
function fillPredictionSample(type) {
    const attField = document.getElementById('attendance_pct');
    const intlField = document.getElementById('internal_marks');
    const asgnField = document.getElementById('assignment_marks');
    const prevField = document.getElementById('previous_exam_marks');
    const studyField = document.getElementById('study_hours_per_day');
    const nameField = document.getElementById('student_name_input');

    if (!attField) return;

    if (type === 'high') {
        if (nameField) nameField.value = 'Aarav Sharma (High Performer)';
        attField.value = '94';
        intlField.value = '90';
        asgnField.value = '95';
        prevField.value = '88';
        studyField.value = '5.5';
    } else if (type === 'average') {
        if (nameField) nameField.value = 'Neha Verma (Average Performer)';
        attField.value = '76';
        intlField.value = '68';
        asgnField.value = '72';
        prevField.value = '65';
        studyField.value = '3.0';
    } else if (type === 'risk') {
        if (nameField) nameField.value = 'Aditya Joshi (At-Risk Alert)';
        attField.value = '48';
        intlField.value = '38';
        asgnField.value = '42';
        prevField.value = '40';
        studyField.value = '1.0';
    }
}

/**
 * Export table to CSV
 */
function exportTableToCSV(filename = 'student_records.csv') {
    const table = document.getElementById('studentsReportTable');
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    for (let i = 0; i < rows.length; i++) {
        let row = [], cols = rows[i].querySelectorAll('td, th');
        // Exclude the last "Actions" column
        for (let j = 0; j < cols.length - 1; j++) {
            let data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s+)/gm, ' ');
            data = data.replace(/"/g, '""');
            row.push('"' + data + '"');
        }
        csv.push(row.join(','));
    }

    const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Filter students table by search query and category
 */
function filterStudentTable() {
    const searchInput = document.getElementById('searchStudentInput');
    const filterSelect = document.getElementById('filterRiskSelect');
    if (!searchInput || !filterSelect) return;

    const searchTerm = searchInput.value.toLowerCase().trim();
    const filterRisk = filterSelect.value.toLowerCase().trim();

    const table = document.getElementById('studentsReportTable');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');

    let visibleCount = 0;

    rows.forEach(row => {
        const studentId = (row.dataset.studentId || '').toLowerCase();
        const studentName = (row.dataset.studentName || '').toLowerCase();
        const riskLevel = (row.dataset.riskLevel || '').toLowerCase();
        const course = (row.dataset.course || '').toLowerCase();

        const matchesSearch = studentId.includes(searchTerm) || studentName.includes(searchTerm) || course.includes(searchTerm);
        const matchesRisk = (filterRisk === 'all' || riskLevel === filterRisk);

        if (matchesSearch && matchesRisk) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    const countElem = document.getElementById('showingCount');
    if (countElem) {
        countElem.textContent = visibleCount;
    }
}
