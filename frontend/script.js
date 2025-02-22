document.addEventListener("DOMContentLoaded", function () {
    function fetchData(apiUrl, callback) {
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(callback)
            .catch(error => console.error("Error loading data:", error));
    }

    // **1️⃣ Total Oil Production Over Time**
    fetchData("http://127.0.0.1:5000/api/trends", data => {
        const ctx = document.getElementById("trendChart").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.map(entry => entry.year),
                datasets: [{
                    label: "Total Oil Production (Barrels)",
                    data: data.map(entry => entry.total_oil_production),
                    borderColor: "#FFD700",
                    backgroundColor: "rgba(255, 215, 0, 0.2)",
                    pointBackgroundColor: "#FFFFFF",
                    pointBorderColor: "#FFD700",
                    pointRadius: 4,
                    fill: true
                }]
            },
            options: { responsive: true }
        });
    });

    // **2️⃣ Wells Per State**
    fetchData("http://127.0.0.1:5000/api/wells-per-state", data => {
        const ctx = document.getElementById("wellsPerStateChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.map(entry => entry.state),
                datasets: [{
                    label: "Total Wells",
                    data: data.map(entry => entry.total_wells),
                    backgroundColor: "#00FF7F",
                    borderColor: "#FFFFFF",
                    borderWidth: 1
                }]
            },
            options: { responsive: true }
        });
    });

    // **3️⃣ Most & Least Producing States**
    fetchData("http://127.0.0.1:5000/api/most-least-producing", data => {
        const ctx1 = document.getElementById("mostProducingChart").getContext("2d");
        new Chart(ctx1, {
            type: "bar",
            data: {
                labels: data.most_producing.map(entry => entry[0]),
                datasets: [{
                    label: "Most Producing (Barrels)",
                    data: data.most_producing.map(entry => entry[1]),
                    backgroundColor: "#FF4500"
                }]
            }
        });

        const ctx2 = document.getElementById("leastProducingChart").getContext("2d");
        new Chart(ctx2, {
            type: "bar",
            data: {
                labels: data.least_producing.map(entry => entry[0]),
                datasets: [{
                    label: "Least Producing (Barrels)",
                    data: data.least_producing.map(entry => entry[1]),
                    backgroundColor: "#FF6347"
                }]
            }
        });
    });

    // **4️⃣ Interactive Map Implementation (Independent Functionality)**
    let mapInitialized = false;
    let map;

    document.getElementById("toggleMapBtn").addEventListener("click", function () {
        const mapContainer = document.getElementById("mapContainer");
    
        // Toggle visibility
        if (mapContainer.style.visibility === "hidden") {
            mapContainer.style.visibility = "visible";
        } else {
            mapContainer.style.visibility = "hidden";
            return; // Don't reload the map if hiding
        }
    
        // Initialize map only once
        if (!mapInitialized) {
            fetchData("http://127.0.0.1:5000/api/map-data", data => {
                if (!Array.isArray(data) || data.length === 0) {
                    console.error("Invalid API response format or empty data:", data);
                    return;
                }
    
                // Create map instance
                map = L.map('map').setView([37.8, -96], 4);
    
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 10,
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
    
                // Add markers for each state
                data.forEach(state => {
                    if (!state.lat || !state.lon) {
                        console.warn(`Missing coordinates for ${state.state}`);
                        return;
                    }
                    const marker = L.marker([state.lat, state.lon]).addTo(map);
                    marker.bindPopup(`<b>${state.state}</b><br>Total Wells: ${state.total_wells}<br>Avg Barrels/Year: ${state.avg_production}`);
                });
    
                mapInitialized = true;
            });
        }
    });
    
});
