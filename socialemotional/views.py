from rest_framework import status, viewsets
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from loguru import logger
from django.http import JsonResponse
from .serializers import SocialMidiaUseResultSerializers, SocialMidiaUseSerializers, GetSocialMidiaUseSerializers
from rest_framework.generics import CreateAPIView, UpdateAPIView
from socialemotional.models import SocialMidiaUse
from helpers.decorators import user_is_active, log_db_queries


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
class SocialMidiaUseView(APIView):

    queryset = SocialMidiaUse.objects.all()
    serializer_class = GetSocialMidiaUseSerializers
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
        try:
            socialmidiause = SocialMidiaUse.objects.all()
            page = self.paginate_queryset(socialmidiause)
            
            if page is not None:
                serializer =  self.get_paginated_response(self.serializer_class(page, many=True).data)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.serializer_class(socialmidiause, many=True)    
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @log_db_queries
    def post(self, request, format='json'):
        data = request.data.copy()  
        data['user'] = request.user.id
        serializer = SocialMidiaUseSerializers(data=data)
        if serializer.is_valid():

            serializer.save()

            message_sucess = "Dados sobre uso de redes sociais criada com sucesso."
            logger.success(message_sucess)
            return Response({'message': message_sucess, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        message_error = "Erro ao registrar informações sobre uso de redes sociais."
        logger.error(message_error)
        return Response({'message': message_error, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SocialMidiaUseDetailView(APIView):
    def get_object(self, pk):
        try:
            return SocialMidiaUse.objects.get(pk=pk)
        except SocialMidiaUse.DoesNotExist:
            return None
        
    @user_is_active
    def get(self, request, pk, format=None):
        socialmidiause = self.get_object(pk)
        if socialmidiause is None:
            message_error = "Informação não encontrada"
            logger.error(message_error)
            return Response({'message': message_error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SocialMidiaUseSerializers(socialmidiause)
        message_sucess = "Informação encontrada com sucesso."
        logger.success(message_sucess)
        return Response({'message': message_sucess, 'data': serializer.data}, status=status.HTTP_200_OK)

    @user_is_active
    def put(self, request, pk, format=None):
        socialmidiause = self.get_object(pk)
        if socialmidiause is None:
            message_error = "Informação não encontrada"
            logger.error(message_error)
            return Response({'message': message_error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SocialMidiaUseSerializers(socialmidiause, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            message_sucess = "Informação atualizada com sucesso."
            logger.success(message_sucess)
            return Response({'message': message_sucess}, status=status.HTTP_202_ACCEPTED)
        
        message_error = "Erro ao atualizar usuário."
        logger.success(message_error)
        return Response({'message': message_error, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @user_is_active
    def delete(self, request, pk, format=None):
        socialmidiause = self.get_object(pk)
        socialmidiause.delete()
        message_sucess = "Informação deletada com sucesso"
        logger.success(message_sucess)
        return Response({'message': message_sucess}, status=status.HTTP_204_NO_CONTENT)