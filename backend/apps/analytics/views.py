from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import FormAnalytics, SubmissionAnalytics, UserAnalytics, SystemAnalytics
from .serializers import (
    FormAnalyticsSerializer, SubmissionAnalyticsSerializer,
    UserAnalyticsSerializer, SystemAnalyticsSerializer
)


class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for analytics data"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def form_analytics(self, request):
        """Get analytics for forms"""
        from apps.forms.models import Form
        
        # Overall metrics
        forms = Form.objects.filter(is_latest=True)
        total_forms = forms.count()
        total_submissions = sum(f.submission_count for f in forms)
        
        # By type
        by_type = {}
        for form_type, label in Form._meta.get_field('form_type').choices:
            count = forms.filter(form_type=form_type).count()
            by_type[form_type] = count
        
        # Top forms
        top_forms = forms.order_by('-submission_count')[:5]
        top_forms_data = [{
            'id': f.id,
            'title': f.title,
            'submissions': f.submission_count,
            'views': f.view_count
        } for f in top_forms]
        
        return Response({
            'total_forms': total_forms,
            'total_submissions': total_submissions,
            'forms_by_type': by_type,
            'top_forms': top_forms_data
        })
    
    @action(detail=False, methods=['get'])
    def submission_analytics(self, request):
        """Get submission analytics"""
        from apps.submissions.models import Submission
        
        # Overall metrics
        submissions = Submission.objects.all()
        total_submissions = submissions.count()
        
        # By status
        by_status = {}
        for status_choice, label in Submission._meta.get_field('status').choices:
            count = submissions.filter(status=status_choice).count()
            by_status[status_choice] = count
        
        # Approval rate
        approved = submissions.filter(status='approved').count()
        rejected = submissions.filter(status='rejected').count()
        approval_rate = (approved / total_submissions * 100) if total_submissions > 0 else 0
        
        # Time metrics (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        submissions_7d = submissions.filter(created_at__gte=week_ago)
        
        return Response({
            'total_submissions': total_submissions,
            'by_status': by_status,
            'approval_rate': round(approval_rate, 2),
            'rejected_count': rejected,
            'last_7_days': submissions_7d.count()
        })
    
    @action(detail=False, methods=['get'])
    def user_analytics(self, request):
        """Get user analytics"""
        from django.contrib.auth import get_user_model
        from apps.submissions.models import Submission
        
        User = get_user_model()
        
        # User counts
        total_users = User.objects.count()
        by_role = {}
        for role, label in User._meta.get_field('role').choices:
            count = User.objects.filter(role=role).count()
            by_role[role] = count
        
        # Active users (submitted in last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        active_users = User.objects.filter(
            submissions__submitted_at__gte=week_ago
        ).distinct().count()
        
        # Top submitters
        top_submitters = User.objects.annotate(
            submission_count=Count('submissions')
        ).order_by('-submission_count')[:5]
        
        top_submitters_data = [{
            'id': u.id,
            'name': u.get_full_name(),
            'submissions': u.submission_count
        } for u in top_submitters]
        
        return Response({
            'total_users': total_users,
            'by_role': by_role,
            'active_users_7d': active_users,
            'top_submitters': top_submitters_data
        })
    
    @action(detail=False, methods=['get'])
    def system_analytics(self, request):
        """Get system-wide analytics"""
        from apps.forms.models import Form
        from apps.submissions.models import Submission
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        total_forms = Form.objects.filter(is_latest=True).count()
        total_submissions = Submission.objects.count()
        total_users = User.objects.count()
        
        # Submissions trend (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        submissions_30d = Submission.objects.filter(
            created_at__gte=thirty_days_ago
        )
        
        # Daily breakdown
        daily_data = {}
        for i in range(30):
            date = (timezone.now() - timedelta(days=i)).date()
            count = submissions_30d.filter(created_at__date=date).count()
            daily_data[str(date)] = count
        
        return Response({
            'total_forms': total_forms,
            'total_submissions': total_submissions,
            'total_users': total_users,
            'submissions_last_30_days': submissions_30d.count(),
            'daily_submissions': daily_data
        })
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get comprehensive dashboard data"""
        return Response({
            'forms': self.form_analytics(request).data,
            'submissions': self.submission_analytics(request).data,
            'users': self.user_analytics(request).data,
            'system': self.system_analytics(request).data
        })
