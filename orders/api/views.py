
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.response import Response
from orders.models import Order
from django.db.models import Q # Encapsulate filters as objects that can then be combined logically (using & and |)
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from orders.api.permissions import IsCustomer, IsOrderBusinessUser
from orders.api.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderCountSerializer,
    CompletedOrderCountSerializer
)





class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=self.request.user) | Q(business_user=self.request.user)
        )

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serilazier = self.get_serializer(data=request.data)
        serilazier.is_valid(raise_exception=True)
        order = serilazier.save()

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)



    def get_permissions(self):
        """Return appropriate permissions based on action."""
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomer()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOrderBusinessUser()]
        elif self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]





class OrderCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCountSerializer

    def get(self, request, business_user_id):
        count = Order.objects.filter(business_user_id=business_user_id,status='in_progress').count()
        serializer = self.get_serializer(data={'order_count': count})
        serializer.is_valid()
        return Response(serializer.data)





class OrderCountCompletedView(generics.GenericAPIView):

    serializer_class = CompletedOrderCountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        count = Order.objects.filter(business_user_id=business_user_id,status='completed').count()
        serializer = self.get_serializer(data={'completed_order_count': count})
        serializer.is_valid()
        return Response(serializer.data)