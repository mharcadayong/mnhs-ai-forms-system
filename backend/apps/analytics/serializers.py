from rest_framework import serializers
from .models import FormAnalytics, SubmissionAnalytics, UserAnalytics, SystemAnalytics


class FormAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for form analytics"""
    
    form_title = serializers.CharField(source='form.title', read_only=True)
    
    class Meta:
        model = FormAnalytics
        fields = [
            'id', 'form', 'form_title', 'view_count', 'submission_count',
            'completion_rate', 'average_time_to_complete', 'approved_count',
            'rejected_count', 'pending_count', 'most_problematic_field',
            'average_approval_time', 'created_at', 'updated_at'
        ]


class SubmissionAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for submission analytics"""
    
    submission_number = serializers.CharField(source='submission.submission_number', read_only=True)
    
    class Meta:
        model = SubmissionAnalytics
        fields = [
            'id', 'submission', 'submission_number', 'creation_to_submission_time',
            'submission_to_approval_time', 'total_processing_time',
            'view_count', 'comment_count', 'revision_count',
            'field_completion_rate', 'has_missing_fields', 'has_validation_errors',
            'created_at', 'updated_at'
        ]


class UserAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for user analytics"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = UserAnalytics
        fields = [
            'id', 'user', 'user_name', 'total_forms_created', 'total_submissions',
            'total_approvals_handled', 'submission_approval_rate',
            'average_approval_rate', 'last_active', 'activity_streak',
            'average_response_time', 'rejection_rate', 'created_at', 'updated_at'
        ]


class SystemAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for system analytics"""
    
    class Meta:
        model = SystemAnalytics
        fields = [
            'id', 'total_forms', 'total_submissions', 'total_users',
            'active_users', 'average_submission_time', 'average_approval_time',
            'system_uptime', 'api_error_rate', 'created_at', 'updated_at'
        ]
