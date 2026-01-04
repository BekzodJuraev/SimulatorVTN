from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from .models import Event,VEN,ReportData
from django.shortcuts import get_object_or_404
from .serializers import (
VENSerializer,
EventSerializer,
ReportDataSerializer
)
class Event_API(APIView):
    serializer_class = EventSerializer

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: EventSerializer()}
    )
    def get(self, request,ven_id):
        ven=Event.objects.filter(target_ven__ven_id=ven_id)
        serializer = self.serializer_class(ven,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class REPORT_API(APIView):
    serializer_class = ReportDataSerializer

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ReportDataSerializer()}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




