// Example of dynamically calculating the carbon footprint
function calculateCarbonFootprint() {
    // For demonstration purposes, we can assume static values
    let cardboard = 0.5;  // Example value in kg CO2
    let plastic = 2.3;
    let paper = 0.8;
    let metal = 1.5;
    let waste = 0.3;

    let totalCarbonFootprint = cardboard + plastic + paper + metal + waste;
    document.getElementById("carbonResult").innerText = `Total Carbon Footprint: ${totalCarbonFootprint.toFixed(2)} kg CO2`;
}

// Initialize the carbon footprint calculation when the page loads
window.onload = calculateCarbonFootprint;