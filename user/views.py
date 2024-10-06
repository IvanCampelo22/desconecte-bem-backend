from rest_framework import status, viewsets
from django_filters import rest_framework as filters
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from loguru import logger
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from .serializers import UserSerializers, UserUpdateSerializer, ChangePasswordSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, ImageUploadSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .filters import UserFilter
from user.models import User, ImagesModels
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from helpers.decorators import user_is_active, log_db_queries
from django.urls import reverse
from supabase import create_client, Client
import os
from django.http import HttpResponse


def get_supabase_client() -> Client:
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    return create_client(url, key)


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


class PasswordResetRequestView(CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        reset_link = request.build_absolute_uri(reset_link)

        send_mail(
            'Password Reset',
            f'Clique no link a seguir para redefinir sua senha: {reset_link}',
            'noreply@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response({'message': 'E-mail de redefinição de senha enviado'}, status=status.HTTP_200_OK)


class PasswordResetView(UpdateAPIView):
    serializer_class = PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Redefinição de senha com sucesso'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
    

class ImageUploadViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user']
            image = serializer.validated_data['image']
            image_name = image.name

            supabase_client = get_supabase_client()
            image_content = image.read()
            image_response = None

            if image:
                image_response = supabase_client.storage.from_('files').upload(image_name, image_content)

            if image_response.status_code == 200:
                try:
                    user_instance = User.objects.get(id=user_id.id)
                except User.DoesNotExist:
                    return Response({'error': 'Invalid User ID'}, status=status.HTTP_400_BAD_REQUEST)
                
                ImagesModels.objects.update_or_create(user=user_instance, image=image_name)
                return Response({'message': 'File uploaded successfully!'}, status=status.HTTP_201_CREATED)
            
            else:
                return Response({'error': 'Failed to upload file to Supabase', 'data': serializer.data}, status=status.HTTP_400_BAD_REQUEST)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None):
        supabase_client = get_supabase_client()
        try:
            image = ImagesModels.objects.get(id=pk)
        except ImagesModels.DoesNotExist:
            return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_name = image.image
        if not image_name.endswith('.png'):
            image_name += '.png'
        
        try:
            projects_image_file = supabase_client.storage.from_('files').download(image_name)
            if projects_image_file:
                response = HttpResponse(projects_image_file, content_type='image/png')
                response['Content-Disposition'] = f'attachment; filename="{image_name}"'
                return response
            else:
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)