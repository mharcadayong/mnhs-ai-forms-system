from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import Approval, ApprovalComment, ApprovalHistory
from .serializers import ApprovalSerializer, ApprovalCommentSerializer, ApprovalHistorySerializer


class ApprovalViewSet(viewsets.ModelViewSet):
    """ViewSet for managing approvals"""
    
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'level', 'assigned_to']
    ordering_fields = ['created_at', 'level']
    ordering = ['level', '-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ['admin', 'principal']:
            return Approval.objects.all()
        return Approval.objects.filter(assigned_to=user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a submission"""
        approval = self.get_object()
        
        if approval.status != 'pending':
            return Response(
                {'error': 'Only pending approvals can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if approval.assigned_to != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to approve this'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        feedback = request.data.get('feedback', '')
        
        approval.status = 'approved'
        approval.feedback = feedback
        approval.completed_at = timezone.now()
        approval.save()
        
        # Create history record
        ApprovalHistory.objects.create(
            submission=approval.submission,
            action_by=request.user,
            action='approved',
            action_level=approval.level,
            notes=feedback
        )
        
        # Check if all approvals are complete
        remaining_approvals = approval.submission.approvals.filter(status='pending')
        if not remaining_approvals.exists():
            approval.submission.status = 'approved'
            approval.submission.completed_at = timezone.now()
            approval.submission.save()
        
        return Response({
            'message': 'Submission approved',
            'approval': ApprovalSerializer(approval).data
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a submission"""
        approval = self.get_object()
        
        if approval.status != 'pending':
            return Response(
                {'error': 'Only pending approvals can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if approval.assigned_to != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to reject this'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        rejection_reason = request.data.get('rejection_reason', '')
        
        approval.status = 'rejected'
        approval.rejection_reason = rejection_reason
        approval.completed_at = timezone.now()
        approval.save()
        
        # Mark submission as rejected
        approval.submission.status = 'rejected'
        approval.submission.save()
        
        # Create history record
        ApprovalHistory.objects.create(
            submission=approval.submission,
            action_by=request.user,
            action='rejected',
            action_level=approval.level,
            notes=rejection_reason
        )
        
        return Response({
            'message': 'Submission rejected',
            'approval': ApprovalSerializer(approval).data
        })
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to approval"""
        approval = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response(
                {'error': 'Comment content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = ApprovalComment.objects.create(
            approval=approval,
            author=request.user,
            content=content
        )
        
        return Response(
            ApprovalCommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending approvals for current user"""
        approvals = Approval.objects.filter(
            assigned_to=request.user,
            status='pending'
        )
        serializer = ApprovalSerializer(approvals, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get approval history for a submission"""
        approval = self.get_object()
        history = ApprovalHistory.objects.filter(submission=approval.submission)
        serializer = ApprovalHistorySerializer(history, many=True)
        return Response(serializer.data)
