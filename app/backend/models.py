from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Settings(models.Model):
    shop_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    logo = models.ImageField(
        upload_to='settings/',
        blank=True,
        null=True
    )

    invoice_prefix = models.CharField(
        max_length=10,
        default='INV'
    )

    currency_symbol = models.CharField(
        max_length=10,
        default='₹'
    )

    def __str__(self):
        return self.shop_name


class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['category_name']

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    barcode = models.CharField(
        max_length=100,
        unique=True
    )

    product_name = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    minimum_stock = models.PositiveIntegerField(
        default=5
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def low_stock(self):
        return self.stock <= self.minimum_stock

    def save(self, *args, **kwargs):

        if self.pk:

            old_product = Product.objects.get(pk=self.pk)

            old_stock = old_product.stock
            new_stock = self.stock

            super().save(*args, **kwargs)

            if old_stock != new_stock:

                action = 'IN' if new_stock > old_stock else 'OUT'

                StockHistory.objects.create(
                    product=self,
                    action=action,
                    previous_stock=old_stock,
                    quantity=abs(new_stock - old_stock),
                    current_stock=new_stock,
                    remarks='Manual Stock Update'
                )

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

class Invoice(models.Model):

    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
    )

    invoice_no = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=200,
        blank=True
    )

    customer_mobile = models.CharField(
        max_length=15,
        blank=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='Cash'
    )

    total_qty = models.PositiveIntegerField(
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    discount_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.invoice_no:

            today = timezone.now().strftime('%Y%m%d')

            last_invoice = Invoice.objects.order_by('-id').first()

            if last_invoice:
                next_id = last_invoice.id + 1
            else:
                next_id = 1

            self.invoice_no = f'INV-{today}-{next_id:04d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    subtotal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        self.price = self.product.selling_price
        self.subtotal = self.quantity * self.price

        super().save(*args, **kwargs)

        if is_new:

            old_stock = self.product.stock

            self.product.stock = max(
                0,
                self.product.stock - self.quantity
            )
            self.product.save()

            StockHistory.objects.create(
                product=self.product,
                action='OUT',
                previous_stock=old_stock,
                quantity=self.quantity,
                current_stock=self.product.stock,
                remarks=f"Invoice {self.invoice.invoice_no}"
            )

        invoice = self.invoice

        invoice.total_qty = (
            invoice.items.aggregate(
                qty=Sum('quantity')
            )['qty'] or 0
        )

        invoice.total_amount = (
            invoice.items.aggregate(
                total=Sum('subtotal')
            )['total'] or 0
        )

        invoice.grand_total = (
            invoice.total_amount -
            invoice.discount_amount
        )

        invoice.save()

    def __str__(self):
        return f"{self.invoice.invoice_no} - {self.product.product_name}"


class StockHistory(models.Model):

    ACTION_CHOICES = (
        ('IN', 'Stock Added'),
        ('OUT', 'Stock Removed'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_history'
    )

    previous_stock = models.PositiveIntegerField()

    quantity = models.PositiveIntegerField()

    current_stock = models.PositiveIntegerField()

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES
    )

    remarks = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.product_name} - {self.action}"