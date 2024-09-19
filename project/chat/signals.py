from django.dispatch import receiver
from .models import Event
from django.db.models.signals import post_save
from channels.layers import get_channel_layer, channel_layers
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Event)
def broadcast_event_to_groups(sender, instance, **kwargs):
    channel_layers = get_channel_layer()
    group_uuid = str(instance.group.uuid)
    event_message = str(instance)
    async_to_sync(channel_layers.group_send)(group_uuid,
                                             {
                                                 'type': 'text_message',
                                                 'message': event_message,
                                                 'status': instance.type,
                                                 'user': str(instance.user)
                                             }
                                             )