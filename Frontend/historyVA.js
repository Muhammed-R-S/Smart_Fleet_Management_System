function refreshData() {
    console.log('Refreshing data...');

    const tableBody = document.getElementById('historical-data-body');

    // Establish websocket connection
    const socket = new WebSocket('ws://localhost:8004');

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log('Received data:', data); // Log received data for debugging

        // Clear existing table rows
        tableBody.innerHTML = '';

        // Populate table with fetched data
        data.forEach(row => {
            const newRow = document.createElement('tr');
            Object.values(row).forEach(value => {
                const newCell = document.createElement('td');
                newCell.textContent = value;
                newRow.appendChild(newCell);
            });
            tableBody.appendChild(newRow);
        });

        // Close the websocket connection after receiving data
        socket.close();
    };

    socket.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    socket.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
    };
}

// Add event listener to refresh button
document.getElementById('refresh-btn').addEventListener('click', refreshData);

// Function to clear data (you can implement actual data clearing logic)
function clearData() {
    console.log('Clearing data...');

    const tableBody = document.getElementById('historical-data-body');
    // Clear the HTML content of the table body to remove all rows
    tableBody.innerHTML = '';
}

// Add event listener to clear button
document.getElementById('clear-btn').addEventListener('click', clearData);
