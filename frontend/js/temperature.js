fetch('http://localhost:8000/data/temperature')
.then(response => response.json())
.then(data => {
    const ctxDaily = document.getElementById('dailyTemperatureChart').getContext('2d');
    new Chart(ctxDaily, {
        type: 'line',
        data: {
            labels: data.daily_measurements.map(d => d.date),
            datasets: [{
                label: 'Daily Temperature Conditions',
                data: data.daily_measurements.map(d => d.temperature_conditions),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {}
    });

    const ctxCorrections = document.getElementById('temperatureCorrectionsChart').getContext('2d');
    new Chart(ctxCorrections, {
        type: 'line',
        data: {
            labels: data.corrections.map(d => d.date),
            datasets: [{
                label: 'Temperature Corrections',
                data: data.corrections.map(d => d.temperature_conditions),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {}
    });
});
