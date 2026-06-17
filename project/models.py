from django.db import models

PROJECT_STATUS_CHOICES = [
    ("pending", "Pending"),
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
    business_plan = models.FileField(upload_to='projects/business_plans/', null=True, blank=True)
    financial_report = models.FileField(upload_to='projects/financial_reports/', null=True, blank=True)
    legal_document = models.FileField(upload_to='projects/legal_documents/', null=True, blank=True)
    agreement = models.FileField(upload_to='projects/agreements/', null=True, blank=True)
    banner = models.ImageField(upload_to='projects/banners/', null=True, blank=True)

    # Status and timestamps
    status = models.CharField(max_length=16, choices=PROJECT_STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state}) - {self.status}"
    
    class Meta:
        ordering = ["-created_at"]