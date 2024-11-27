from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.attendances.api.serializers.enrollment_serializer import EnrollmentSerializer, EnrollmentRetrieveSerializer

class EnrollomentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    @action(detail=False, methods=['post'],)
    def create_from_list(self, request):
        """
        Action que acepta una lista de usuarios para crear múltiples instancias.
        """
        data = request.data  # La lista de objetos JSON enviada por el cliente
        
        if not isinstance(data, list):
            return Response({"error": "Se esperaba una lista de inscripciones."}, status=status.HTTP_400_BAD_REQUEST)
        
        success = []
        errors = []

        for enrollment in data:
            enrollment_serializer = self.serializer_class(data=enrollment)
            if enrollment_serializer.is_valid():
                enrollment_serializer.save()
                success.append({
                    'message': 'inscripcion creado correctamente.',
                    'enrollment': enrollment_serializer.data
                })
            else:
                errors.append({
                    'enrollment': enrollment,
                    'errors': enrollment_serializer.errors
                })
        
        return Response({
            'success': success,
            'errors': errors
        }, status=status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED)
     
    def list(self, request):
        enrollment_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "enrollments": enrollment_serializer.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Inscripción registrada correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'Hay un error', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        enrollment = self.get_queryset(pk)
        if enrollment:
            enrollment_serializer = EnrollmentRetrieveSerializer(enrollment)
            return Response(enrollment_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Inscripción con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            enrollment_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if enrollment_serializer.is_valid():
                enrollment_serializer.save()
                return Response({'message':'Inscripción actualizada correctamente!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':enrollment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        enrollment = self.get_queryset().filter(id=pk).first() # get instance        
        if enrollment:
            enrollment.state = False
            enrollment.save()
            return Response({'message':'Inscripción eliminada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Inscripción con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)