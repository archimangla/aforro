from celery import shared_task
from .models import Order

@shared_task
def send_order_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Simulate async work (email / notification)
        print(f"[CELERY] Order {order.id} confirmed for store {order.store_id}")
    except Order.DoesNotExist:
        pass
