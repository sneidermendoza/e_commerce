from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializer import OrderSerializer,OrderDetailsSerializer
from .models import Orders, OrderDetails 
from rest_framework import viewsets
import random
import string

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        if queryset.exists():
            # Lista para almacenar los detalles de productos de cada orden
            orders_with_details = []
            
            for order in queryset:
                # Obtener detalles de productos para esta orden
                order_details = OrderDetails.objects.filter(order=order)
                details_serializer = OrderDetailsSerializer(order_details, many=True)
                
                # Construir la respuesta para esta orden
                order_data = {
                    'id': order.id,
                    'order_number': order.order_number,
                    'product_ids': order.product_ids,
                    'total_value': order.total_value,
                    'status': order.status,
                    'data': details_serializer.data  # Detalles de productos vendidos
                }
                orders_with_details.append(order_data)
            
            return Response(orders_with_details, status=status.HTTP_200_OK)
        
        return Response([], status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = self.get_queryset(pk)
        if order:
            # Cambiar el estado de la orden a False
            order.status = False
            order.save()

            # Cambiar el estado de los detalles de orden asociados
            OrderDetails.objects.filter(order=order).update(status=False)

            return Response('Orden eliminada exitosamente', status=status.HTTP_200_OK)
        return Response('No se encontró el registro', status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        order = self.get_queryset(pk)
        if order:
            order_serializer = self.serializer_class(order, data=request.data)
            if order_serializer.is_valid():
                order_serializer.save()
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('No se encontró el registro', status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def create_order_from_array(self, request):
        products_data = request.data.get('products', [])

        if not isinstance(products_data, list) or not all('product_id' in item and 'quantity' in item for item in products_data):
            return Response('Formato de entrada inválido', status=status.HTTP_400_BAD_REQUEST)

        total_value = 0
        product_ids = []

        for item in products_data:
            product = Orders.get_product_details(item['product_id'])
            if not product:
                return Response(f"Producto {item['product_id']} no encontrado", status=status.HTTP_400_BAD_REQUEST)
            
            if item['quantity'] > product['stock']:
                return Response(f"No hay suficiente stock para el producto {item['product_id']}", status=status.HTTP_400_BAD_REQUEST)

            total_value += product['price'] * item['quantity']
            product_ids.append(f"{item['product_id']}:{item['quantity']}")

        # Generar número de orden único
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        order_data = {
            'order_number': order_number,
            'product_ids': ','.join(product_ids),
            'total_value': str(total_value),
            'status': True
        }

        serializer = self.get_serializer(data=order_data)
        if serializer.is_valid():
            order_instance = serializer.save()
            # Crear registros en OrderDetails
            for item in products_data:
                OrderDetails.objects.create(
                    order=order_instance,
                    product_id=item['product_id'],
                    quantity=item['quantity']
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
