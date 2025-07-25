

google.charts.load('current', {
  'packages': ['geochart'],
  'mapsApiKey': 'YOUR_GOOGLE_MAPS_API_KEY'
});
google.charts.setOnLoadCallback(drawChart);

let datasets = {};
let currentCancerType = 'lung';

// Fetch data from Django API
async function fetchData(cancerType) {
  try {
    const response = await fetch(`/api/cancer/${cancerType}/`);
    const result = await response.json();
    console.log(`API Response for ${cancerType}:`, result); // Debug: API response check
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
    console.error(`Error fetching data for ${cancerType}:`, error);
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
    console.log(`No data for ${cancerType}, fetching now...`);
    fetchData(cancerType).then(success => {
      if (success) {
        drawChart(); // Retry after fetching
      }
    });
    return;
  }

  if (!columnName) {
    console.error(`No valid column selected for ${cancerType}`);
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

  console.log(`DataTable for ${cancerType} (${columnName}):`, data.toJSON()); // Debug: DataTable check
  if (rowCount === 0) {
    console.warn(`No valid data rows for ${cancerType} (${columnName})`);
    alert(`No valid data to display for ${cancerType.charAt(0).toUpperCase() + cancerType.slice(1)} Cancer yet. Check other feature or data.`);
    return;
  }

  const options = {
    colorAxis: { colors: ['#F6C646', '#5643D1'] },
    backgroundColor: {
      fill: 'transparent', // Ocean color
      // stroke: 'yellow', // Coastline color
      // strokeWidth: 1
    },
    datalessRegionColor: '#ffffff', // Land color for no data
    tooltip: { isHtml: true },
    explorer: {
      actions: ['dragToZoom', 'rightClickToReset'],
      keepInBounds: true,
      axis: 'horizontal',
      maxZoomIn: 8,
      maxZoomOut: 1,
      zoomDelta: 2,
    },
    // legend: 'none'
  };

  const chart = new google.visualization.GeoChart(document.getElementById('geochart'));
  chart.__dataTable = data; // Store DataTable
  chart.draw(data, options);


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
    drawChart();
  }
}



// popup.js (alag file ya script tag mein)

// Show popup at mouse coordinates with text data
function showPopup(country, text, x, y) {
  const popup = document.getElementById('popup');
  if (!text || text.trim() === '') {
    popup.style.display = 'none';
    return;
  }
  popup.innerHTML = `<strong>${country}</strong><br>${text}`;
  popup.style.left = `${x + 10}px`; // 10px offset
  popup.style.top = `${y + 10}px`;
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
    console.log(`No data for ${cancerType}`);
    return null;
  }
  const row = datasets[cancerType].data.find(row => row.country === country);
  console.log(`Text data for ${country} (${textColumn}):`, row ? row[textColumn] : 'Not found');
  return row ? row[textColumn] || 'No data available' : 'No data available';
}

// Updated click event listener for GeoChart
function addChartClickListener(chart, cancerType, textColumn) {
  let lastSelectedCountry = null;

  // Handle country selection with select event
  google.visualization.events.addListener(chart, 'select', function () {
    const selection = chart.getSelection();
    if (selection.length > 0 && selection[0].row != null) {
      const dataTable = chart.__dataTable;
      lastSelectedCountry = dataTable.getValue(selection[0].row, 0); // Store selected country
    } else {
      lastSelectedCountry = null;
      hidePopup();
    }
  });

  // Handle mouse coordinates with native click event
  const chartDiv = document.getElementById('geochart');
  chartDiv.addEventListener('click', function (e) {
    if (lastSelectedCountry) {
      const text = getTextData(cancerType, lastSelectedCountry, textColumn);
      showPopup(lastSelectedCountry, text, e.clientX, e.clientY);
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