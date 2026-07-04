from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Form, FormField
from .serializers import (
    FormSerializer, FormCreateSerializer, FormDetailSerializer, FormFieldSerializer
)


class FormViewSet(viewsets.ModelViewSet):
    """ViewSet for managing forms"""
    
    queryset = Form.objects.filter(is_latest=True)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'form_type', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'submission_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FormCreateSerializer
        elif self.action == 'retrieve':
            return FormDetailSerializer
        return FormSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ['admin', 'principal']:
            return Form.objects.filter(is_latest=True)
        return Form.objects.filter(is_latest=True, is_public=True) | \
               Form.objects.filter(is_latest=True, created_by=user) | \
               Form.objects.filter(is_latest=True, assigned_to=user)
    
    def perform_create(self, serializer):
        """Create form with current user as creator"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a form"""
        form = self.get_object()
        if form.created_by != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to publish this form'},
                status=status.HTTP_403_FORBIDDEN
            )
        form.publish()
        return Response({'message': 'Form published successfully'})
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a form"""
        form = self.get_object()
        if form.created_by != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to archive this form'},
                status=status.HTTP_403_FORBIDDEN
            )
        form.archive()
        return Response({'message': 'Form archived successfully'})
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Create a new version of the form"""
        form = self.get_object()
        
        # Create new version
        new_form = Form.objects.create(
            title=form.title,
            description=form.description,
            form_type=form.form_type,
            category=form.category,
            created_by=request.user,
            requires_approval=form.requires_approval,
            allow_multiple_submissions=form.allow_multiple_submissions,
            submission_deadline=form.submission_deadline,
            is_public=form.is_public,
            version=form.version + 1,
            parent_form=form.parent_form or form,
            is_latest=True
        )
        
        # Mark old form as not latest
        form.is_latest = False
        form.save()
        
        # Copy fields
        for field in form.fields.all():
            FormField.objects.create(
                form=new_form,
                label=field.label,
                field_type=field.field_type,
                placeholder=field.placeholder,
                help_text=field.help_text,
                is_required=field.is_required,
                validation_regex=field.validation_regex,
                max_length=field.max_length,
                min_length=field.min_length,
                options=field.options,
                ai_suggestion_enabled=field.ai_suggestion_enabled,
                ai_suggestion_prompt=field.ai_suggestion_prompt,
                order=field.order
            )
        
        serializer = FormDetailSerializer(new_form)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """Get all versions of a form"""
        form = self.get_object()
        parent = form.parent_form or form
        versions = Form.objects.filter(
            parent_form__isnull=True,
            id=parent.id
        ) | Form.objects.filter(parent_form=parent)
        versions = versions.order_by('-version')
        serializer = FormSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_forms(self, request):
        """Get forms created by current user"""
        forms = Form.objects.filter(created_by=request.user, is_latest=True)
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def assigned_forms(self, request):
        """Get forms assigned to current user"""
        forms = Form.objects.filter(assigned_to=request.user, is_latest=True)
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)


class FormFieldViewSet(viewsets.ModelViewSet):
    """ViewSet for managing form fields"""
    
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        form_id = self.request.query_params.get('form_id')
        if form_id:
            return FormField.objects.filter(form_id=form_id)
        return FormField.objects.all()
    
    def perform_create(self, serializer):
        """Ensure user owns the form"""
        form = serializer.validated_data.get('form')
        if form.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionError("You do not have permission to edit this form")
        serializer.save()
