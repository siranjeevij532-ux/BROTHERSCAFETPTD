"""
Management command to repair orders where total_amount / subtotal is 0
but the order has items. Run once after deploying the fix:

    python manage.py fix_totals
"""
from django.core.management.base import BaseCommand
from restaurant.models import Order
from decimal import Decimal, ROUND_HALF_UP


class Command(BaseCommand):
    help = 'Recalculate and save subtotal/discount_amount/total_amount for all orders'

    def handle(self, *args, **options):
        orders = Order.objects.prefetch_related('items').all()
        fixed = 0
        for order in orders:
            items = list(order.items.all())
            if not items:
                continue
            subtotal = sum(i.unit_price * i.quantity for i in items)
            disc = (subtotal * order.discount_percent / 100).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            ) if order.discount_percent else Decimal('0')
            total = subtotal - disc
            if order.subtotal != subtotal or order.total_amount != total:
                Order.objects.filter(pk=order.pk).update(
                    subtotal=subtotal,
                    discount_amount=disc,
                    total_amount=total,
                )
                fixed += 1
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed} orders out of {orders.count()} total.'))
