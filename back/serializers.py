from rest_framework import serializers
from .models import VEN, Event, ReportData


class VENSerializer(serializers.ModelSerializer):
    class Meta:
        model = VEN
        fields = ['id', 'name', 'ven_id', 'protocol', 'is_active', 'last_seen']


class EventSerializer(serializers.ModelSerializer):

    target_ven_id = serializers.ReadOnlyField(source='target_ven.ven_id')

    class Meta:
        model = Event
        fields = [
            'id',
            'event_id',
            'status',
            'start_time',
            'duration_minutes',
            'status',
            'signal_name',
            'payload',
            'target_ven_id'
        ]

class ReportDataSerializer(serializers.ModelSerializer):
    ven_id = serializers.SlugRelatedField(
        source='ven',
        slug_field='ven_id',
        queryset=VEN.objects.all()
    )

    class Meta:
        model = ReportData
        fields = ['ven_id', 'value', 'report_type']


