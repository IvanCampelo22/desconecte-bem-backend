from django.shortcuts import render
from .serializers import NotificationSerializer
from .models import Notification
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from helpers.decorators import log_db_queries
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from loguru import logger
# Create your views here.


class BasicPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        if not hasattr(self, 'page'):
            raise AttributeError("Paginação não inicializada corretamente.")

        total_items = self.page.paginator.count
        total_pages = self.page.paginator.num_pages

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': total_pages,
            'count': total_items,
            'results': data
        })

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class NotificationView(APIView):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = BasicPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator    
    
    def paginate_queryset(self, queryset):
        
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)    
    
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    @log_db_queries
    def get(self, request, format=None):
        notification = Notification.objects.all()
        page = self.paginate_queryset(notification)
        
        if page is not None:
            serializer =  self.get_paginated_response(self.serializer_class(page, many=True).data)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.serializer_class(notification, many=True)    
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class NotificationDetailView(APIView):
    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        notification = self.get_object(pk)
        if notification is None:
            message_error = "Notificação não encontrada"
            logger.error(message_error)
            return Response({'message': message_error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NotificationSerializer(notification)
        message_sucess = "Notificação encontrada com sucesso."
        logger.success(message_sucess)
        return Response({'message': message_sucess, 'data': serializer.data}, status=status.HTTP_200_OK)