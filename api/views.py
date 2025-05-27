from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Doctor, Patient, HealthRecord, DoctorAnnotation, DoctorNotification
from .serializers import (
    DoctorSerializer, PatientSerializer, HealthRecordSerializer,
    DoctorAnnotationSerializer, DoctorNotificationSerializer
)
from rest_framework.permissions import AllowAny
from rest_framework import serializers

# Create your views here.

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def patients(self, request, pk=None):
        doctor = self.get_object()
        patients = doctor.patients.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def notifications(self, request, pk=None):
        doctor = self.get_object()
        notifications = doctor.notifications.filter(is_read=False).order_by('-created_at')
        serializer = DoctorNotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_notification_read(self, request, pk=None):
        notification_id = request.data.get('notification_id')
        notification = get_object_or_404(DoctorNotification, id=notification_id, doctor=self.get_object())
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=True, methods=['post'])
    def annotate_record(self, request, pk=None):
        doctor = self.get_object()
        record_id = request.data.get('record_id')
        comment = request.data.get('comment')
        
        record = get_object_or_404(HealthRecord, id=record_id)
        if record.patient not in doctor.patients.all():
            return Response(
                {"error": "You are not authorized to annotate this record"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        annotation = DoctorAnnotation.objects.create(
            health_record=record,
            doctor=doctor,
            comment=comment
        )
        serializer = DoctorAnnotationSerializer(annotation)
        return Response(serializer.data)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        try:
            patient = serializer.save()
            # Create notifications for assigned doctors
            for doctor in patient.assigned_doctors.all():
                DoctorNotification.objects.create(
                    doctor=doctor,
                    patient=patient,
                    is_new_patient=True
                )
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return user.doctor.patients.all()
        elif hasattr(user, 'patient'):
            return Patient.objects.filter(id=user.patient.id)
        return Patient.objects.none()

    @action(detail=True, methods=['get'])
    def records(self, request, pk=None):
        patient = self.get_object()
        if request.user.patient != patient and not request.user.doctor.patients.filter(id=patient.id).exists():
            return Response(
                {"error": "You are not authorized to view these records"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        records = patient.health_records.all()
        serializer = HealthRecordSerializer(records, many=True)
        return Response(serializer.data)

class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient'):
            return user.patient.health_records.all()
        elif hasattr(user, 'doctor'):
            return HealthRecord.objects.filter(patient__in=user.doctor.patients.all())
        return HealthRecord.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'doctor'):
            # If user is a doctor, get patient from request data
            patient_id = self.request.data.get('patient')
            if not patient_id:
                raise serializers.ValidationError({"patient": "Patient ID is required for doctors"})
            
            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                raise serializers.ValidationError({"patient": f"Patient with ID {patient_id} does not exist"})
            
            # Verify doctor has access to this patient
            if patient not in user.doctor.patients.all():
                raise permissions.PermissionDenied("You don't have permission to create records for this patient")
            
            serializer.save(patient=patient)
        elif hasattr(user, 'patient'):
            # If user is a patient, use their own patient record
            serializer.save(patient=user.patient)
        else:
            raise permissions.PermissionDenied("You don't have permission to create health records")

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
