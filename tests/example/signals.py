from django.dispatch import receiver

from dmqtt.signals import connect, regex, topic


@receiver(connect)
def on_connect(sender, **kwargs):
    sender.subscribe("#")


@topic("some/mqtt/topic")
def simple_topic(sender, topic, data, **kwargs):
    print(topic)
    print(data)


@regex("^some/(?P<username>[^/]+)/(?P<device>[^/]+)$")
def regex_topic(match, data, **kwargs):
    device = match.groupdict()
    print(device["username"], device["device"])
    print(data)
