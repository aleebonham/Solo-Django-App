document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('salesChart').getContext('2d');
    var data = JSON.parse('{{ data | safe }}');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Orders per Day',
                data: data.values
            }]
        }
    });
});