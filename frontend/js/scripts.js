document.getElementById('add-plant-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const jsonData = JSON.stringify(Object.fromEntries(formData));

    fetch('http://localhost:8000/add-plant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: jsonData
    })
    .then(response => response.json().then(data => {
        if (!response.ok) {
            throw new Error(data.detail);
        }
        return data;
    }))
    .then(data => {
        event.target.reset();
        alert('Plant added successfully!');
    })
    .catch(error => {
        alert('Error adding plant: ' + error.message);
    });
});

document.getElementById('daily-plant-data-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    formData.append('date', new Date().toISOString().split('T')[0]);
    const jsonData = JSON.stringify(Object.fromEntries(formData));

    fetch('http://localhost:8000/daily-plant-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: jsonData
    })
    .then(response => response.json().then(data => {
        if (!response.ok) {
            throw new Error(data.detail);
        }
        return data;
    }))
    .then(data => {
        event.target.reset();
        alert('Daily data added successfully!');
    })
    .catch(error => {
        alert('Error adding daily data: ' + error.message);
    });
});
