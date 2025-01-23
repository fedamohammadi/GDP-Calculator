
const countries = ["Afghanistan", "Albania", "Algeria", "Angola", "Argentina", "Australia", "Austria",
    "Bangladesh", "Belgium", "Bolivia", "Brazil", "Bulgaria", "Canada", "Chile", "China", "Colombia", 
    "Denmark", "Dominican Republic", "Egypt", "Ethiopia", "Finland", "France", "Germany", "Greece", 
    "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Kenya", 
    "Malaysia", "Mexico", "Morocco", "Netherlands", "New Zealand", "Nigeria", "Norway", "Pakistan", 
    "Peru", "Philippines", "Poland", "Portugal", "Romania", "Russia", "Saudi Arabia", "South Africa", 
    "South Korea", "Spain", "Sri Lanka", "Sweden", "Switzerland", "Thailand", "Turkey", "Ukraine", 
    "United Arab Emirates", "United Kingdom", "United States", "Vietnam", "Zimbabwe"];

// Populate country dropdown
const countryDropdown = document.getElementById("country");
countries.forEach(country => {
    let option = document.createElement("option");
    option.text = country;
    option.value = country;
    countryDropdown.appendChild(option);
});


const topGDPs = [
    { country: "United States", gdp: 25.43 },
    { country: "China", gdp: 14.72 },
    { country: "Japan", gdp: 4.25 },
    { country: "Germany", gdp: 3.85 },
    { country: "India", gdp: 3.41 },
    { country: "United Kingdom", gdp: 2.67 },
    { country: "France", gdp: 2.63 },
    { country: "Brazil", gdp: 2.24 },
    { country: "Canada", gdp: 2.16 },
    { country: "Russia", gdp: 2.04 },
    { country: "Italy", gdp: 1.92 },
    { country: "South Korea", gdp: 1.69 },
    { country: "Australia", gdp: 1.67 },
    { country: "Mexico", gdp: 1.46 },
    { country: "Spain", gdp: 1.41 }
];


function calculateGDP() {
    let c = parseFloat(document.getElementById("consumption").value) || 0;
    let i = parseFloat(document.getElementById("investment").value) || 0;
    let g = parseFloat(document.getElementById("government").value) || 0;
    let x = parseFloat(document.getElementById("exports").value) || 0;
    let m = parseFloat(document.getElementById("imports").value) || 0;
    let country = document.getElementById("country").value;

    if (country === "") {
        alert("Please select a country.");
        return;
    }

    // The correct GDP formula
    let gdp = c + i + g + (x - m);

    
    if (gdp < 0) {
        alert("Warning: Your country's imports exceed total economic output. GDP is negative.");
    }

    document.getElementById("result").innerText = `Overall GDP of ${country}: $${formatGDP(gdp)}`;
}

// Function to format GDP
function formatGDP(value) {
    if (value >= 1_000_000_000_000) return (value / 1_000_000_000_000).toFixed(2) + " Trillion";
    if (value >= 1_000_000_000) return (value / 1_000_000_000).toFixed(2) + " Billion";
    if (value >= 1_000_000) return (value / 1_000_000).toFixed(2) + " Million";
    return value.toFixed(2);
}

// Show Ranking
function showRanking() {
    let gdpText = document.getElementById("result").innerText;
    
    
    let gdpMatch = gdpText.replace(/[^\d.]/g, ''); 
    let gdp = parseFloat(gdpMatch) * 1_000_000_000; 
    let country = document.getElementById("country").value;

    if (gdp === 0) {
        alert("Calculate GDP first!");
        return;
    }

    document.getElementById("ranking").style.display = "block";

    
    let percentile;                     // This part still does not work fully properly as expected. 
    if (gdp >= 3_000_000_000_000) {
        percentile = "Top 1% (Highest)";
    } else if (gdp >= 1_000_000_000_000) {
        percentile = "Top 5%";
    } else if (gdp >= 500_000_000_000) {
        percentile = "Top 10%";
    } else if (gdp >= 100_000_000_000) {
        percentile = "Top 25%";
    } else if (gdp >= 10_000_000_000) {
        percentile = "Top 50%";
    } else if (gdp >= 1_000_000_000) {
        percentile = "Bottom 50%";
    } else {
        percentile = "Bottom 75%";
    }

   
    let rankingText = "<strong>Top 15 Countries with the highest GDP in 2024:</strong><br>";
    rankingText += "<pre style='text-align: left; font-family: Arial; font-size: 14px;'>";
    topGDPs.forEach((c, i) => {
        rankingText += `${(i + 1).toString().padEnd(3, " ")} ${c.country.padEnd(20, " ")}: $${c.gdp.toFixed(2)} Trillion\n`;
    });
    rankingText += "</pre>";


    document.getElementById("ranking-list").innerHTML = `${rankingText}<br><strong>${country}'s GDP is ranked:</strong> ${percentile}`;
}

// Function to reset fields (Fixed)
function resetFields() {
    document.getElementById("consumption").value = "";
    document.getElementById("investment").value = "";
    document.getElementById("government").value = "";
    document.getElementById("exports").value = "";
    document.getElementById("imports").value = "";
    document.getElementById("country").selectedIndex = 0;
    document.getElementById("result").innerText = "Overall GDP: ";
    document.getElementById("ranking").style.display = "none";
    document.getElementById("ranking-list").innerHTML = "";
}
