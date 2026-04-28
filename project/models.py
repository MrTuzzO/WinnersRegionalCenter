from django.db import models

PROJECT_STATUS_CHOICES = [
    ("active", "Active"),
    ("completed", "Completed"),
]

class Project(models.Model):
    # Project identity
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    is_eb_5_enabled = models.BooleanField(default=False)

    # financial details
    total_project_value = models.DecimalField(max_digits=15, decimal_places=2)
    minimum_investment = models.DecimalField(max_digits=15, decimal_places=2)
    roi = models.CharField(max_length=16)
    job_impact = models.CharField(max_length=16)

    # Documents
    business_plan = models.FileField(upload_to='projects/business_plans/')
    financial_report = models.FileField(upload_to='projects/financial_reports/')
    legal_document = models.FileField(upload_to='projects/legal_documents/')
    agreement = models.FileField(upload_to='projects/agreements/')
    banner = models.ImageField(upload_to='projects/banners/')

    # Status and timestamps
    status = models.CharField(max_length=16, choices=PROJECT_STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state}) - {self.status}"
    
    class Meta:
        ordering = ["-created_at"]