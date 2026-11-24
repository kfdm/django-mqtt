from django.urls import include, path

urlpatterns = [
    path("mosquitto/", include("dmqtt.mosquitto")),
]
