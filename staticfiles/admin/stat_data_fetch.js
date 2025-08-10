
// fetch("../../../secrete.json")
// .then(data => {
//     const domain = data.domain;
// })
// .catch(error => {
//     console.error('Error fetching or parsing JSON:', error);
// });


const domain = "http://127.0.0.1:8000/"; // Update with your actual domain


async function fetchStatJSON(cancerType) {
    if (!cancerType) {
        console.error("Cancer type is required to fetch statistics.");
        fetchStatJSON('lung'); // Default to 'lung' if no type provided
        alert("No cancer type provided. Defaulting to 'lung'.");
    }

    const response = await fetch(`${domain}api/stats/${cancerType}/`);
    const data = await response.json();
    console.log(`Statistics for ${cancerType}:`, data); // Debug: API response check

    if (data) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${cancerType}Cancer_statistics.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        alert(`Statistics for ${cancerType} downloaded successfully.`);
    }
}

async function fetchDataJSON(cancerType) {
    if (!cancerType) {
        console.error("Cancer type is required to fetch statistics.");
        fetchDataJSON('lung'); // Default to 'lung' if no type provided
        alert("No cancer type provided. Defaulting to 'lung'.");
    }

    try {
        const response = await fetch(`${domain}api/cancer/${cancerType}/`);
        const result = await response.json();
        console.log(`API Response for ${cancerType}:`, result); // Debug: API response check
        if (result.error || !result.columns || !result.data) {
            console.error(`Invalid API response for ${cancerType}:`, result);
            alert(`Error: Could not load data for ${cancerType}. Please check the server.`);
            return false; // Indicate failure
        }

        else {
            const blob = new Blob([JSON.stringify(result.data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${cancerType}Cancer_data.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            alert(`Statistics for ${cancerType} downloaded successfully.`);
        }
    } catch (error) {
        console.error(`Error fetching data for ${cancerType}:`, error);
        alert(`Failed to fetch data for ${cancerType}. Please try again.`);
        return false;
    }
}


function boxDraw() {
    
}


// popup
function openPopup(popup_id) {
    document.getElementById(popup_id).style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function closePopup(popup_id) {
    document.getElementById(popup_id).style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}


