// This is the code template for humidity.js
document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/data/humidity')
    .then(response => response.json())
    .then(data => {
        const ctxDaily = document.getElementById('dailyHumidityChart').getContext('2d');
        const dailyChart = new Chart(ctxDaily, {
            type: 'line',
            data: {
                labels: data.daily_measurements.map(d => d.date),
                datasets: [{
                    label: 'Daily Humidity',
                    data: data.daily_measurements.map(d => d.soil_moisture_content),
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {}
        });

        const ctxCorrections = document.getElementById('humidityCorrectionsChart').getContext('2d');
        const correctionsChart = new Chart(ctxCorrections, {
            type: 'line',
            data: {
                labels: data.corrections.map(d => d.date),
                datasets: [{
                    label: 'Humidity Corrections',
                    data: data.corrections.map(d => d.soil_moisture_content),
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }]
            },
            options: {}
        });
    });
});
