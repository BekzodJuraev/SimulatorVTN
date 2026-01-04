from django.urls import path,include
from . import views
urlpatterns=[
    path('api/v3/events/<uuid:ven_id>',views.Event_API.as_view()),
    path('api/v3/report',views.REPORT_API.as_view())
]