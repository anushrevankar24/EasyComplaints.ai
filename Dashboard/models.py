from django.db import models
from login_and_signup.models import CustomUser
from django.utils import timezone

class Complaint(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    complaint=models.TextField(default='Empty Complaint')
    department = models.CharField(max_length=150,default="Unassigned Department")
    image=models.ImageField(upload_to='image_complaints/',null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=50,default="Pending")
    def set_pending(self):
        self.status = "Pending"
        self.save()

    def set_resolved(self):
        self.status = "Resolved"
        self.save()

    def set_rejected(self):
        self.status = "Rejected"
        self.save()
    def __str__(self):
      return f"Complaint ID: {self.pk} - Department: {self.department}"
