fetch('http://localhost:8000/data/minerals')
.then(response => response.json())
.then(data => {
    const ctxDaily = document.getElementById('dailyMineralsChart').getContext('2d');
    new Chart(ctxDaily, {
        type: 'line',
        data: {
            labels: data.daily_measurements.map(d => d.date),
            datasets: [{
                label: 'Daily Amount of Minerals',
                data: data.daily_measurements.map(d => d.amount_of_mineral_substance),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {}
    });

    const ctxCorrections = document.getElementById('mineralsCorrectionsChart').getContext('2d');
    new Chart(ctxCorrections, {
        type: 'line',
        data: {
            labels: data.corrections.map(d => d.date),
            datasets: [{
                label: 'Minerals Corrections',
                data: data.corrections.map(d => d.amount_of_mineral_substance),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {}
    });
});
