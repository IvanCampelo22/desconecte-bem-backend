from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from loguru import logger

from .serializers import UserSerializers, UserUpdateSerializer, ChangePasswordSerializer

from .filters import UserFilter
from user.models import User
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

class UsersView(APIView):

    queryset = User.objects.all()
    serializer_class = UserSerializers
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
        user = User.objects.all()
        page = self.paginate_queryset(user)
        
        if page is not None:
            serializer =  self.get_paginated_response(self.serializer_class(page, many=True).data)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.serializer_class(user, many=True)    
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format='json'):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()

            message_sucess = "Usuário criada com sucesso."
            logger.success(message_sucess)
            return Response({'message': message_sucess, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        message_error = "Erro ao criar usuário."
        logger.error(message_error)
        return Response({'message': message_error, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UsersDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        
    @user_is_active
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        if user is None:
            message_error = "Usuário não encontrado"
            logger.error(message_error)
            return Response({'message': message_error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializers(user)
        message_sucess = "Usuário encontrado com sucesso."
        logger.success(message_sucess)
        return Response({'message': message_sucess, 'data': serializer.data}, status=status.HTTP_200_OK)

    @user_is_active
    def put(self, request, pk, format=None):
        users = self.get_object(pk)
        if users is None:
            message_error = "Usuário não encontrado"
            logger.error(message_error)
            return Response({'message': message_error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserUpdateSerializer(users, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            message_sucess = "Usuário atualizado com sucesso."
            logger.success(message_sucess)
            return Response({'message': message_sucess}, status=status.HTTP_202_ACCEPTED)
        
        message_error = "Erro ao atualizar usuário."
        logger.success(message_error)
        return Response({'message': message_error, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @user_is_active
    def delete(self, request, pk, format=None):
        self.get_object(pk)
        User.objects.update(is_active=False)
        message_sucess = "Usuário desativado com sucesso"
        logger.success(message_sucess)
        return Response({'message': message_sucess}, status=status.HTTP_204_NO_CONTENT)
    

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserFilter