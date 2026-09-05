document.addEventListener('DOMContentLoaded', () => {
    // Global State & Baseline Dataset Metrics
    const metrics = {
        total: 10000,
        active: 7121,
        churned: 2879,
        churnRate: 28.79,
        avgCharge: 62.74,
        revRisk: 2220133.56
    };

    // Chart References
    let chartDonut, chartContract, chartTenure, chartPlan, chartTickets, chartSatisfaction, chartReasons;

    // Tab Navigation
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');

    const tabTitles = {
        'tab-overview': { title: 'Executive Churn Overview', sub: 'Real-time analysis of customer retention, contract risk, and revenue metrics' },
        'tab-drivers': { title: 'Churn Drivers & Customer Behavior', sub: 'Diagnostic investigation into support tickets, CSAT scores, and cancellation reasons' },
        'tab-retention': { title: 'Retention & Revenue at Risk', sub: 'Customer Value / Risk 4-Quadrant Matrix and prioritized retention targets' },
        'tab-insights': { title: 'Business Recommendations & Action Strategy', sub: '5 strategic interventions to reduce churn and protect recurring revenue' }
    };

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetTab = item.getAttribute('data-tab');
            
            navItems.forEach(n => n.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));

            item.classList.add('active');
            document.getElementById(targetTab).classList.add('active');

            if (tabTitles[targetTab]) {
                pageTitle.textContent = tabTitles[targetTab].title;
                pageSubtitle.textContent = tabTitles[targetTab].sub;
            }
        });
    });

    // Reset Filters Listener
    document.getElementById('reset-filters-btn').addEventListener('click', () => {
        document.getElementById('filter-contract').value = 'ALL';
        document.getElementById('filter-plan').value = 'ALL';
        document.getElementById('filter-internet').value = 'ALL';
        document.getElementById('filter-payment').value = 'ALL';
        updateDashboard();
    });

    // Filter Change Listeners
    ['filter-contract', 'filter-plan', 'filter-internet', 'filter-payment'].forEach(id => {
        document.getElementById(id).addEventListener('change', updateDashboard);
    });

    function updateDashboard() {
        const contractFilter = document.getElementById('filter-contract').value;
        const planFilter = document.getElementById('filter-plan').value;

        let multiplier = 1.0;
        if (contractFilter === 'Month-to-month') multiplier *= 1.24;
        if (contractFilter === 'Two year') multiplier *= 0.61;
        if (planFilter === 'Premium') multiplier *= 1.09;

        const currentChurnRate = Math.min(65.0, Math.max(10.0, metrics.churnRate * multiplier));
        const activeCount = Math.round(metrics.total * (1 - currentChurnRate / 100));
        const churnedCount = metrics.total - activeCount;

        document.getElementById('kpi-active-customers').textContent = activeCount.toLocaleString();
        document.getElementById('kpi-churned-customers').textContent = churnedCount.toLocaleString();
        document.getElementById('kpi-churn-rate').textContent = `${currentChurnRate.toFixed(2)}% Churn Rate`;
        document.getElementById('kpi-active-pct').textContent = `${(100 - currentChurnRate).toFixed(2)}% Retained`;

        if (chartDonut) {
            chartDonut.data.datasets[0].data = [activeCount, churnedCount];
            chartDonut.update();
        }
    }

    // Initialize Charts
    function initCharts() {
        // Chart 1: Donut Status
        const ctxDonut = document.getElementById('chart-status-donut').getContext('2d');
        chartDonut = new Chart(ctxDonut, {
            type: 'doughnut',
            data: {
                labels: ['Active Customers', 'Churned Customers'],
                datasets: [{
                    data: [7121, 2879],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderWidth: 2,
                    borderColor: '#1e293b'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#94a3b8', font: { family: 'Inter' } } }
                }
            }
        });

        // Chart 2: Contract Bar
        const ctxContract = document.getElementById('chart-contract-bar').getContext('2d');
        chartContract = new Chart(ctxContract, {
            type: 'bar',
            data: {
                labels: ['Month-to-month', 'One year', 'Two year'],
                datasets: [{
                    label: 'Churn Rate (%)',
                    data: [35.71, 22.31, 17.68],
                    backgroundColor: ['#ef4444', '#3b82f6', '#10b981'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Chart 3: Tenure Bar
        const ctxTenure = document.getElementById('chart-tenure-bar').getContext('2d');
        chartTenure = new Chart(ctxTenure, {
            type: 'bar',
            data: {
                labels: ['0–6 mos', '7–12 mos', '13–24 mos', '25–48 mos', '49+ mos'],
                datasets: [{
                    label: 'Churn Rate (%)',
                    data: [41.19, 32.15, 25.61, 22.82, 16.91],
                    backgroundColor: '#3b82f6',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Chart 4: Plan Bar
        const ctxPlan = document.getElementById('chart-plan-bar').getContext('2d');
        chartPlan = new Chart(ctxPlan, {
            type: 'bar',
            data: {
                labels: ['Basic ($37/mo)', 'Standard ($67/mo)', 'Premium ($97/mo)'],
                datasets: [{
                    label: 'Churn Rate (%)',
                    data: [27.15, 28.84, 31.55],
                    backgroundColor: ['#10b981', '#3b82f6', '#ef4444'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Chart 5: Tickets Bar
        const ctxTickets = document.getElementById('chart-tickets-bar').getContext('2d');
        chartTickets = new Chart(ctxTickets, {
            type: 'bar',
            data: {
                labels: ['0 Tickets', '1–2 Tickets', '3–5 Tickets', '6+ Tickets'],
                datasets: [{
                    label: 'Churn Rate (%)',
                    data: [28.45, 27.07, 32.09, 46.53],
                    backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Chart 6: Satisfaction Bar
        const ctxSatisfaction = document.getElementById('chart-satisfaction-bar').getContext('2d');
        chartSatisfaction = new Chart(ctxSatisfaction, {
            type: 'bar',
            data: {
                labels: ['Low (CSAT 1-4)', 'Medium (CSAT 5-7)', 'High (CSAT 8-10)'],
                datasets: [{
                    label: 'Churn Rate (%)',
                    data: [40.25, 24.05, 14.16],
                    backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // Chart 7: Reasons Bar
        const ctxReasons = document.getElementById('chart-reasons-bar').getContext('2d');
        chartReasons = new Chart(ctxReasons, {
            type: 'bar',
            indexAxis: 'y',
            data: {
                labels: [
                    'Competitor offered higher speeds',
                    'Price too high',
                    'Service dissatisfaction',
                    'Poor tech support',
                    'Customer moved',
                    'Lack of features'
                ],
                datasets: [{
                    label: 'Churned Customer Count',
                    data: [845, 680, 520, 410, 260, 164],
                    backgroundColor: '#ef4444',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                    y: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    }

    initCharts();
});
