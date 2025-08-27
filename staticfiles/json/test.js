
async function fetchPopupContext(cancerType, countryName) {
  try {
    const response = await fetch('overviewPopupContext.json');
    const data = await response.json();
    
    // Check if cancerType exists and its value is not empty
    if (!data[cancerType] || Object.keys(data[cancerType]).length === 0) {
      return `No data available for cancer type: ${cancerType}`;
    }
    // Check if countryName exists under cancerType
    if (!data[cancerType][countryName]) {
      return `No data available for country: ${countryName} under cancer type: ${cancerType}`;
    }
    const popupContext = data[cancerType][countryName].popup_context;
    return popupContext || "Popup context not found";
  } catch (error) {
    console.error("Error fetching or accessing popup context:", error);
    return "Invalid cancer type or country name";
  }
}

// Example usage
fetchPopupContext("lung", "india").then(result => {
  console.log(result); // Output: strong foundations in treatment access and guidelines, but gaps remain in early detection, reimbursement, and advanced biomarker testing.
});