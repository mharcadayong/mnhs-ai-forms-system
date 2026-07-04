from django.db import models
from django.contrib.auth import get_user_model
from apps.forms.models import Form
from apps.submissions.models import Submission

User = get_user_model()


class FormAnalytics(models.Model):
    """Analytics for forms"""
    
    form = models.OneToOneField(Form, on_delete=models.CASCADE, related_name='analytics')
    
    # Metrics
    view_count = models.IntegerField(default=0)
    submission_count = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0, help_text="Percentage of submitted forms")
    average_time_to_complete = models.IntegerField(default=0, help_text="Average time in minutes")
    
    # Status breakdown
    approved_count = models.IntegerField(default=0)
    rejected_count = models.IntegerField(default=0)
    pending_count = models.IntegerField(default=0)
    
    # Field metrics
    most_problematic_field = models.CharField(max_length=255, blank=True)
    field_error_rate = models.JSONField(default=dict)  # Field-wise error rates
    
    # Approval metrics
    average_approval_time = models.IntegerField(default=0, help_text="Average time in hours")
    average_rejections = models.FloatField(default=0.0)
    
    # Trends
    weekly_submissions = models.JSONField(default=dict)
    monthly_submissions = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.form.title}"


class SubmissionAnalytics(models.Model):
    """Analytics for submissions"""
    
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='analytics')
    
    # Timestamps
    creation_to_submission_time = models.IntegerField(default=0, help_text="Minutes")
    submission_to_approval_time = models.IntegerField(default=0, help_text="Hours")
    total_processing_time = models.IntegerField(default=0, help_text="Hours")
    
    # Interactions
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    revision_count = models.IntegerField(default=0)
    
    # Quality
    field_completion_rate = models.FloatField(default=0.0)
    has_missing_fields = models.BooleanField(default=False)
    has_validation_errors = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.submission.submission_number}"


class UserAnalytics(models.Model):
    """Analytics for user activities"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    
    # Activity metrics
    total_forms_created = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    total_approvals_handled = models.IntegerField(default=0)
    
    # Success metrics
    submission_approval_rate = models.FloatField(default=0.0)
    average_approval_rate = models.FloatField(default=0.0)
    
    # Engagement
    last_active = models.DateTimeField(null=True, blank=True)
    activity_streak = models.IntegerField(default=0, help_text="Days of consecutive activity")
    
    # Performance
    average_response_time = models.IntegerField(default=0, help_text="Hours for approvals")
    rejection_rate = models.FloatField(default=0.0)
    
    # Trends
    monthly_activity = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.user.username}"


class SystemAnalytics(models.Model):
    """System-wide analytics"""
    
    # Counts
    total_forms = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    
    # Performance
    average_submission_time = models.IntegerField(default=0, help_text="Minutes")
    average_approval_time = models.IntegerField(default=0, help_text="Hours")
    
    # Trends
    weekly_submissions = models.JSONField(default=dict)
    monthly_submissions = models.JSONField(default=dict)
    
    # Health
    system_uptime = models.FloatField(default=99.9, help_text="Percentage")
    api_error_rate = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "System Analytics"
    
    def __str__(self):
        return f"System Analytics - {self.updated_at.date()}"
