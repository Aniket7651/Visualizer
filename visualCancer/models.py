from django.db import models

class BreastCancer(models.Model):
    # infra..
    country = models.CharField(max_length=100)
    Specialized_Centers = models.IntegerField()
    GeneMol_Centers = models.IntegerField()
    Infra_Avg = models.FloatField()

    # treatment, funding, awareness
    Treatment_Access = models.IntegerField()
    Research_Funding = models.IntegerField()
    Awareness_Campaigns = models.IntegerField()
    Treatment_Avg = models.FloatField()

    # Survival rate, early detection, palliative care 
    Survival_Rates = models.IntegerField()
    Early_Detection = models.IntegerField()
    Palliative_Care = models.IntegerField()
    SEdPc_Avg = models.FloatField()

    # Biomarkers
    HER2 = models.IntegerField()
    ER = models.IntegerField()
    PR = models.IntegerField()
    BRAC1 = models.IntegerField()
    BRAC2 = models.IntegerField()
    Biomark_Avg = models.FloatField()

    # clinical guide
    Clinical_Guideline = models.IntegerField()
    Feasibility_Integration = models.IntegerField()
    Adopt_inti = models.IntegerField()
    Engagement_Updates = models.IntegerField()
    ESMO = models.IntegerField()
    Clinical_Avg = models.FloatField()

    # Reimbursement
    Reimbursement = models.IntegerField()
    No_cost = models.IntegerField()


    # cancer sreening
    Cancer_Screening = models.CharField(max_length=200)

    
    def __str__(self):
        return self.country
    
# TODO: add more fields to the model
class Sarcoma(models.Model):
    
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.country
