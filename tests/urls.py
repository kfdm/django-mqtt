from django.urls import path, include

urlpatterns = [
    path("mosquitto/", include("dmqtt.mosquitto")),
]
