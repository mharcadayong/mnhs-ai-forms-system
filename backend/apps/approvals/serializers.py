from rest_framework import serializers
from .models import Approval, ApprovalComment, ApprovalHistory


class ApprovalCommentSerializer(serializers.ModelSerializer):
    """Serializer for approval comments"""
    
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = ApprovalComment
        fields = ['id', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class ApprovalSerializer(serializers.ModelSerializer):
    """Serializer for approvals"""
    
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    submission_number = serializers.CharField(source='submission.submission_number', read_only=True)
    comments = ApprovalCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Approval
        fields = [
            'id', 'submission', 'submission_number', 'assigned_to', 'assigned_to_name',
            'level', 'status', 'feedback', 'rejection_reason', 'comments',
            'created_at', 'completed_at', 'updated_at'
        ]
        read_only_fields = ['id', 'submission', 'level', 'created_at', 'updated_at']


class ApprovalHistorySerializer(serializers.ModelSerializer):
    """Serializer for approval history"""
    
    action_by_name = serializers.CharField(source='action_by.get_full_name', read_only=True)
    
    class Meta:
        model = ApprovalHistory
        fields = [
            'id', 'submission', 'action_by', 'action_by_name', 'action',
            'action_level', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
