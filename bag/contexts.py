from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        
       
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.ORDER_DISCOUNT_THRESHOLD:
        discount = total * Decimal(settings.ORDER_DISCOUNT_AMOUNT / 100)
        order_discount_delta = settings.ORDER_DISCOUNT_THRESHOLD - total
    else:
        discount = 10
        order_discount_delta = 10
 
    grand_total = discount + total
   
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'discount': discount,
        'order_discount_delta': order_discount_delta,
        'order_discount_threshold': settings.ORDER_DISCOUNT_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
