from django.db import models

# python manage.py makemigrations visualCancer
# python manage.py migrate --run-syncdb

class BreastCancerData(models.Model):
    # infra..
    country = models.CharField(max_length=100)
    Specialized_Centers = models.IntegerField()
    GeneMol_Centers = models.IntegerField()

    # treatment, funding, awareness
    Treatment_Access = models.IntegerField()
    Research_Funding = models.IntegerField()
    Awareness_Campaigns = models.IntegerField()

    # Survival rate, early detection, palliative care 
    Survival_Rates = models.IntegerField()
    Early_Detection = models.IntegerField()
    Palliative_Care = models.IntegerField()

    # Biomarkers
    HER2 = models.IntegerField()
    ER = models.IntegerField()
    PR = models.IntegerField()
    BRAC1 = models.IntegerField()
    BRAC2 = models.IntegerField()

    # clinical guide
    Clinical_Guideline = models.IntegerField()
    Feasibility_Integration = models.IntegerField()
    Adoption_of_Intl_Guidelines = models.IntegerField()
    Engagement_with_Updates = models.IntegerField()
    ESMO_Guidelines_Implementation = models.IntegerField()

    # Reimbursement
    Reimbursement = models.IntegerField()
    No_cost = models.IntegerField()


    # cancer sreening
    Cancer_Screening = models.CharField(max_length=200)

    
    def __str__(self):
        return self.country
    
# TODO: add more fields to the model
class LungCancerData(models.Model):
    
    country = models.CharField(max_length=100)
    Specialized_Centers = models.IntegerField()
    GeneMol_Centers = models.IntegerField()

    # treatment, funding, awareness
    Treatment_Access = models.IntegerField()
    Research_Funding = models.IntegerField()
    Awareness_Campaigns = models.IntegerField()

    # Survival rate, early detection, palliative care 
    Survival_Rates = models.IntegerField()
    Early_Detection = models.IntegerField()
    Palliative_Care = models.IntegerField()

    # Biomarkers
    EGFR = models.IntegerField()
    ALK = models.IntegerField()
    PD_L1 = models.IntegerField()
    MET = models.IntegerField()
    ROS1 = models.IntegerField()
    BRAF = models.IntegerField()
    KRAS = models.IntegerField()

    # clinical guide
    Clinical_Guideline = models.IntegerField()
    Feasibility_Integration = models.IntegerField()
    Adoption_of_Intl_Guidelines = models.IntegerField()
    Engagement_with_Updates = models.IntegerField()
    ESMO_Guidelines_Implementation = models.IntegerField()

    # Reimbursement
    Reimbursement = models.IntegerField()
    No_cost = models.IntegerField()

    # cancer sreening
    Cancer_Screening = models.CharField(max_length=200)

    def __str__(self):
        return self.country


class ColorectalCancerData(models.Model):
    
    country = models.CharField(max_length=100)
    Specialized_Centers = models.IntegerField()
    GeneMol_Centers = models.IntegerField()

    # treatment, funding, awareness
    Treatment_Access = models.IntegerField()
    Research_Funding = models.IntegerField()
    Awareness_Campaigns = models.IntegerField()

    # Survival rate, early detection, palliative care 
    Survival_Rates = models.IntegerField()
    Early_Detection = models.IntegerField()
    Palliative_Care = models.IntegerField()


    # Biomarkers
    KRAS_MUT = models.IntegerField()
    NRAS_MUT = models.IntegerField()
    BRAF_MUT = models.IntegerField()
    MSI_dMMR = models.IntegerField()
    PIK3CA_MUT = models.IntegerField()

    # clinical guide
    Clinical_Guideline = models.IntegerField()
    Feasibility_Integration = models.IntegerField()
    Adoption_of_Intl_Guidelines = models.IntegerField()
    Engagement_with_Updates = models.IntegerField()
    ESMO_Guidelines_Implementation = models.IntegerField()

    # Reimbursement
    Reimbursement = models.IntegerField()
    No_cost = models.IntegerField()

    # cancer sreening
    Cancer_Screening = models.CharField(max_length=200)


    def __str__(self):
        return self.country


class ProstateCancerData(models.Model):
    
    country = models.CharField(max_length=100)
    Specialized_Centers = models.IntegerField()
    GeneMol_Centers = models.IntegerField()

    # treatment, funding, awareness
    Treatment_Access = models.IntegerField()
    Research_Funding = models.IntegerField()
    Awareness_Campaigns = models.IntegerField()

    # Survival rate, early detection, palliative care 
    Survival_Rates = models.IntegerField()
    Early_Detection = models.IntegerField()
    Palliative_Care = models.IntegerField()

    # Biomarkers
    PSA = models.IntegerField()
    TMPRSS2_ERG = models.IntegerField()
    PTEN = models.IntegerField()
    UNKNOWN = models.IntegerField()

    # clinical guide
    Clinical_Guideline = models.IntegerField()
    Feasibility_Integration = models.IntegerField()
    Adoption_of_Intl_Guidelines = models.IntegerField()
    Engagement_with_Updates = models.IntegerField()
    ESMO_Guidelines_Implementation = models.IntegerField()

    # Reimbursement
    Reimbursement = models.IntegerField()
    No_cost = models.IntegerField()

    # cancer screening
    Cancer_Screening = models.CharField(max_length=200)
    

    def __str__(self):
        return self.country
    

class GastricCancerData(models.Model):
    
    country = models.CharField(max_length=100)
    Specialized_Centers = models.IntegerField()
    GeneMol_Centers = models.IntegerField()

    # treatment, funding, awareness
    Treatment_Access = models.IntegerField()
    Research_Funding = models.IntegerField()
    Awareness_Campaigns = models.IntegerField()

    # Survival rate, early detection, palliative care 
    Survival_Rates = models.IntegerField()
    Early_Detection = models.IntegerField()
    Palliative_Care = models.IntegerField()

    # Biomarkers
    HER2 = models.IntegerField()
    MSI_H = models.IntegerField()
    PD_L1 = models.IntegerField()
    CLDN18_2 = models.IntegerField()
    FGFR2b = models.IntegerField()

    # clinical guide
    Clinical_Guideline = models.IntegerField()
    Feasibility_Integration = models.IntegerField()
    Adoption_of_Intl_Guidelines = models.IntegerField()
    Engagement_with_Updates = models.IntegerField()
    ESMO_Guidelines_Implementation = models.IntegerField()

    # Reimbursement
    Reimbursement = models.IntegerField()
    No_cost = models.IntegerField()

    # cancer sreening
    Cancer_Screening = models.CharField(max_length=200)

    def __str__(self):
        return self.country
    

# average values for each cancer type

class AverageValues(models.Model):
    cancer_type = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    average_infra = models.FloatField()
    average_treatment = models.FloatField()
    average_se_dpc = models.FloatField()
    average_biomarkers = models.FloatField()

    def __str__(self):
        return self.cancer_type