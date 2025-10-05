
var domain_link = window.location.protocol + "//" + window.location.host + "/"


google.charts.load('current', {
  'packages': ['geochart'],
  'mapsApiKey': 'YOUR_GOOGLE_MAPS_API_KEY'
});
google.charts.setOnLoadCallback(drawChart);

let datasets = {};
let currentCancerType = 'lung';
const baseJsonUrl = '../static/json/';


const infrastructure = ["Specialized_Centers", "GeneMol_Centers"];
const TRFA = ["Treatment_Access", "Research_Funding", "Awareness_Campaigns"];
const SEPC = ["Survival_Rates", "Early_Detection", "Palliative_Care"];
const clinical_guide = ["Clinical_Guideline", "Feasibility_Integration", "Engagement_with_Updates", "ESMO_Guidelines_Implementation"];
const reimbursement = ["Reimbursement"];
const screening = ["Cancer_Screening"];

const allArrays = {
  infrastructure: infrastructure,
  TRFA: TRFA,
  SEPC: SEPC,
  clinical_guide: clinical_guide,
  reimbursement: reimbursement,
  screening: screening
};

function getPopupContent(cancerType, country) {

}


// Fetch data from Django API
async function fetchData(cancerType) {
  try {
    const response = await fetch(`/api/cancer/${cancerType}/`);
    const result = await response.json();
    // console.log(`API Response for ${cancerType}:`, result); // Debug: API response check
    if (result.error || !result.columns || !result.data) {
      console.error(`Invalid API response for ${cancerType}:`, result);
      alert(`Error: Could not load data for ${cancerType}. Please check the server.`);
      return false; // Indicate failure
    }
    datasets[cancerType] = {
      columns: result.columns,
      data: result.data
    };
    populateColumns(cancerType);
    return true; // Indicate success
  } catch (error) {
    // console.error(`Error fetching data for ${cancerType}:`, error);
    alert(`Failed to fetch data for ${cancerType}. Please try again.`);
    return false;
  }
}

function populateColumns(cancerType) {
  const columnSelect = document.getElementById('column');
  columnSelect.innerHTML = '';
  const columns = datasets[cancerType]?.columns || [];
  if (columns.length === 0) {
    console.warn(`No columns available for ${cancerType}`);
    return;
  }
  for (let i = 1; i < columns.length; i++) { // Skip 'country' column
    const option = document.createElement('option');
    option.value = columns[i];
    option.text = columns[i].replace('_', ' ').toUpperCase();
    columnSelect.appendChild(option);
  }
}

function drawChart() {
  const cancerType = document.getElementById('cancerType').value;
  const columnSelect = document.getElementById('column');

  // Use first numerical column as fallback if none selected
  const columnName = columnSelect.value || (datasets[cancerType]?.columns ? datasets[cancerType].columns[1] : null);


  // Check if data exists
  if (!datasets[cancerType] || !datasets[cancerType].columns || !datasets[cancerType].data) {
    // console.log(`No data for ${cancerType}, fetching now...`);
    fetchData(cancerType).then(success => {
      if (success) {
        drawChart(); // Retry after fetching
      }
    });
    return;
  }

  if (!columnName) {
    // console.error(`No valid column selected for ${cancerType}`);
    alert('Please select a valid data column.');
    return;
  }

  const data = new google.visualization.DataTable();
  data.addColumn('string', 'Country');
  data.addColumn('number', columnName.replace('_', ' ').toUpperCase());

  let rowCount = 0;
  datasets[cancerType].data.forEach(row => {
    const value = parseFloat(row[columnName]);
    if (!isNaN(value) && row.country) {
      data.addRow([row.country, value]);
      rowCount++;
    }
  });

  fetchAndRenderJson(cancerType, columnSelect.value); // Fetch and render JSON data

  // console.log(`DataTable for ${cancerType} (${columnName}):`, data.toJSON()); // Debug: DataTable check
  if (rowCount === 0) {
    console.warn(`No valid data rows for ${cancerType} (${columnName})`);
    alert(`No valid data to display for ${cancerType.charAt(0).toUpperCase() + cancerType.slice(1)} Cancer yet. Check other feature or data.`);
    return;
  }

  const options = {
    responseive: true,
    maintainAspectRatio: false,
    colorAxis: { colors: ['#F6C646', '#5643D1'] },
    backgroundColor: {
      fill: 'transparent', // Ocean color
    },
    datalessRegionColor: '#ccc', // Land color for no data
    tooltip: { isHtml: true },
  };

  const chart = new google.visualization.GeoChart(document.getElementById('geochart'));
  chart.__dataTable = data; // Store DataTable
  chart.draw(data, options);

  window.addEventListener('resize', function () {
    chart.resize();
  });

  addChartClickListener(chart, cancerType, 'Cancer_Screening'); // Use 'Cancer Screening' as text column
}

function updateChart() {
  const cancerType = document.getElementById('cancerType').value;
  if (!datasets[cancerType]) {
    fetchData(cancerType).then(success => {
      if (success) {
        drawChart();
      }
    });
  } else {
    populateColumns(cancerType);
    // fetchAndRenderJson(cancerType);
    drawChart();
  }
}





function findStringInArrays(searchString, arrays) {
  for (const arrayName in arrays) {
    if (Object.hasOwnProperty.call(arrays, arrayName)) {
      const currentArray = arrays[arrayName];
      if (Array.isArray(currentArray) && currentArray.includes(searchString)) {
        return arrayName;
      }
    }
  }
  return null;
}


function fetchAndRenderJson(cancerType, colNameFromPillar, attempt = 1, maxAttempts = 3) {

  const dataList = document.getElementById('data-list');
  const featureDetail = document.getElementById('feature-detail');

  const legendText = document.getElementById('legend-container');

  const jsonUrl = `${baseJsonUrl}${cancerType}.json`;

  fetch(jsonUrl, { cache: 'no-store' })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {

      // console.log(`Fetched ${cancerType}.json successfully:`, data); // Debugging ke liye
      dataList.innerHTML = `
            <h3>${data.title}</h3>
            <p>${data.description}</p>
            `; // Add new data
      const pillar = findStringInArrays(colNameFromPillar, allArrays);
      if (pillar !== null) {
        featureDetail.innerHTML = `<ul>${data[pillar].legends.map(legend => `<li class="legend">${legend}</li>`).join('')}</ul>`;
        
        if (data[pillar].legends[0] == "No legend available" ) {
          legendText.innerHTML = `<p class="legend-alert">No legend available for this parameter yet</p>`;
        }
        else {
          legendText.innerHTML = `
            <ul>
              ${data[pillar].legends.map(legend => `<li><h1>${legend.split("–")[0]}</h1><p>${legend.split("–")[1]}</p></li>`).join('')}
            </ul>
          `;
        }
      }
      else {
        featureDetail.innerHTML = `<ul>${data.utilization_biom.legends.map(legend => `<li class="legend">${legend}</li>`).join('')}</ul>`;

        legendText.innerHTML = `
          <ul>
            ${data.utilization_biom.legends.map(legend => `<li><h1>${legend.split("–")[0]}</h1><p>${legend.split("–")[1]}</p></li>`).join('')}
          </ul>
        `;
      }
    })
    .catch(error => {
      console.error(`Attempt ${attempt}: Error fetching ${cancerType}.json:`, error);
      if (attempt < maxAttempts) {
        console.log(`Retrying ${cancerType}.json (Attempt ${attempt + 1})`);
        setTimeout(() => fetchAndRenderJson(cancerType, colNameFromPillar, attempt + 1, maxAttempts), 1000);
      } else {
        dataList.innerHTML = `<li>Error loading ${cancerType}.json after ${maxAttempts} attempts. Check console.</li>`;
      }
    });
}



// popup.js (alag file ya script tag mein)

// Show popup at mouse coordinates with text data
function showPopup(country, text, overviewLink, x, y, overviewShort = null) {
  const popup = document.getElementById('popup');
  if (!text || text.trim() === '') {
    popup.style.display = 'none';
    return;
  }
  popup.innerHTML = `<strong>
                          ${country}<br><p>For more details about overview and policy paper, ${overviewLink}</p>
                          <br>Cancer Screening</strong><br>${text}<br>
                          <br>${overviewShort}<br>`;

  if (window.innerWidth <= 768) {
    popup.style.left = 'auto';
  }
  else {
    popup.style.left = `${x + 1}px`; // 10px offset
  }
  popup.style.top = `${y + 5}px`;
  popup.style.display = 'block';
}

// Hide popup
function hidePopup() {
  const popup = document.getElementById('popup');
  popup.style.display = 'none';
}

// Get text data for a country
function getTextData(cancerType, country, textColumn) {
  if (!datasets[cancerType] || !datasets[cancerType].data) {
    // console.log(`No data for ${cancerType}`);
    return null;
  }
  const row = datasets[cancerType].data.find(row => row.country === country);
  // console.log(`Text data for ${country} (${textColumn}):`, row ? row[textColumn] : 'Not found');
  return row ? row[textColumn] || 'No data available' : 'No data available';
}


async function fetchPopupContext(cancerType, countryName) {
  // Validate inputs
  if (!cancerType || !countryName) {
    return "Cancer type and country name are required";
  }

  try {
    
    // Fetch the JSON file (adjust path as needed)
    const response = await fetch(`${baseJsonUrl}overviewPopupContext.json`);
    
    // Check if response is valid
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
    }

    // Verify Content-Type is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Response is not JSON');
    }

    // Parse the JSON
    const data = await response.json();
    
    // Check if cancerType exists and is not empty
    if (!data[cancerType] || Object.keys(data[cancerType]).length === 0) {
      return `<b style="color: red;">No data available for cancer type '${cancerType}'</b>`;
    }

    // Check if countryName exists under cancerType
    if (!data[cancerType][countryName]) {
      return `<b style="color: red;">No data available for country '${countryName}'; under cancer type '${cancerType}'</b>`;
    }

    // Return popup_context
    const popupContext = data[cancerType][countryName].popup_context;
    return popupContext || "<b style=\"color: yellow;\">Popup context not found</b>";
  } catch (error) {
    console.error("Error fetching or accessing popup context:", error);
    return `<b style="color: red;">Error: ${error.message}</b>`;
  }
}



// Updated click event listener for GeoChart
function addChartClickListener(chart, cancerType, textColumn) {
  let lastSelectedCountry = null;
  let overviewLink = null;
  // Handle country selection with select event
  google.visualization.events.addListener(chart, 'select', function () {
    const selection = chart.getSelection();
    if (selection.length > 0 && selection[0].row != null) {
      const dataTable = chart.__dataTable;
      lastSelectedCountry = dataTable.getValue(selection[0].row, 0); // Store selected country
      var link = domain_link + "overview/" + encodeURIComponent(cancerType) + "/" + encodeURIComponent(lastSelectedCountry);
      var popupContent = `<a href="${link}" target="_blank">Click Here</a>`;

      overviewLink = popupContent;

    } else {
      lastSelectedCountry = null;
      hidePopup();
    }
  });

  // Handle mouse coordinates with native click event
  const chartDiv = document.getElementById('geochart');
  chartDiv.addEventListener('click', async function (e) {
    if (lastSelectedCountry) {
      const text = getTextData(cancerType, lastSelectedCountry, textColumn);
      showPopup(lastSelectedCountry, text, overviewLink, e.clientX, e.clientY, await fetchPopupContext(cancerType, lastSelectedCountry));
    } else {
      hidePopup();
    }
  });

  // Hide popup when clicking outside the chart
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#geochart') && !e.target.closest('#popup')) {
      hidePopup();
    }
  });
}



// Initial load
window.onload = () => fetchData(document.getElementById('cancerType').value);

window.addEventListener('load', () => {
  fetchAndRenderJson(document.getElementById('cancerType').value, document.getElementById('column').value);
});
