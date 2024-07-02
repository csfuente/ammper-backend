from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import validate_email

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ocultar contraseña en respuesta
    
    

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.pop('password')
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError("Email already exists as username.")
        user = User(username=email, **validated_data)
        user.set_password(password)  # Hashear la contraseña
        user.save()
        return user
