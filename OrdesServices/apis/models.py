from django.db import models
from django.db import connection

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=100)
    product_ids = models.TextField()  # Aquí se almacena la lista de productos como un string
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default = True)

    def __str__(self):
        return f'Order {self.id} - {self.order_number}'

    # Function to fetch product details from the shared database
    def get_product_details(product_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, price, stock FROM api_product WHERE id = %s AND status = True", [product_id])
            row = cursor.fetchone()
        if row:
            return {'id': row[0], 'price': row[1], 'stock': row[2]}
        return None

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, related_name='details', on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default = True)

    class Meta:
        unique_together = (('order', 'product_id'),)

    def __str__(self):
        return f'Details for Order {self.order.id}, Product {self.product_id}'
