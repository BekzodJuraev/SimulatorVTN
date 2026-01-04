from django.db import models
import uuid
# Create your models here.
class VEN(models.Model):
    PROTOCOL_CHOICES = [
        ('2.0b', 'OpenADR 2.0b'),
        ('3.0', 'OpenADR 3.0'),
    ]

    name = models.CharField(max_length=250,)

    ven_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    protocol = models.CharField(max_length=10, choices=PROTOCOL_CHOICES, default='2.0b')
    is_active = models.BooleanField(default=True)

    security_token = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} [{self.protocol}]"

    class Meta:
        verbose_name = "VEN"
        verbose_name_plural = "VENs"


class Event(models.Model):
    STATUS_CHOICES = [
        ('far', 'Far'),
        ('near', 'Near'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    event_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    target_ven = models.ForeignKey(VEN, on_delete=models.CASCADE, related_name='events')


    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()


    signal_name = models.CharField(max_length=50, default="SIMPLE")
    payload = models.FloatField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='far')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.event_id} -> {self.target_ven.name}"

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class ReportData(models.Model):
    ven = models.ForeignKey(VEN, on_delete=models.CASCADE, related_name='reports')
    timestamp = models.DateTimeField(auto_now_add=True)


    report_type = models.CharField(max_length=50, default="POWER_REAL")
    value = models.FloatField()

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-timestamp']