const infra = ["Specialized_Centers", "GeneMol_Centers"];
const TRF = ["Treatment_Access", "Research_Funding", "Awareness_Campaigns"];
const SEP = ["Survival_Rates", "Early_Detection", "Palliative_Care"];
const clinical_guid = ["Clinical_Guideline", "Feasibility_Integration", "Engagement_with_Updates", "ESMO_Guidelines_Implementation"];
const reimbursemen = ["Reimbursement"];
const screenin = ["Cancer_Screening"];

const allArrays = {
  infra: infra,
  TRF: TRF,
  SEP: SEP,
  clinical_guid: clinical_guid,
  reimbursemen: reimbursemen,
  screenin: screenin
};

const cancerType = document.getElementById('cancerType').value;

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

console.log("cancer type test.js: "+cancerType);

// console.log(findStringInArrays("Survival_Rates", allArrays));
