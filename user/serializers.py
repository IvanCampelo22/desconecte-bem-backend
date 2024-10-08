from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.models import User
import re
from user.models import ImagesModels


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] 
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
    

class ImageUploadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = ImagesModels
        fields = ['id', 'user', 'image', 'uploaded_at']


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=12)

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'required': True}
        }

    def create(self, validated_data):
        user = get_user_model()(**validated_data)
        user.save()
        return user
    
    def validate_password(self, value: str):
        if value == value.lower():
            raise serializers.ValidationError("A senha deve conter ao menos uma letra maíscula")
        
        if value ==  value.upper():
            raise serializers.ValidationError("A senha deve conter ao menos uma letra minúscula")
        
        if not bool(re.search("\d", value)):
            raise serializers.ValidationError("A senha deve conter ao menos um número")
        
        # Verifica o decimal ASCII da letra para verificar se é um caracter especial
        if not any((ord(x) >= 33 and ord(x)<=47) or (ord(x) >= 58 and ord(x) <= 64) or (ord(x) >= 91 and ord(x) <= 96) for x in value):
            raise serializers.ValidationError("A senha deve conter ao menos um caractér especial. Ex: !@#$%^&*")
        
        
        return value
        
    

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        return instance
    

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()