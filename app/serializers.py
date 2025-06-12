from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class DisciplinaSerializer(serializers.ModelSerializer):
    # professor = UsuarioSerializer(read_only=True)
    professor_name = serializers.CharField(source='professor.username', read_only=True)

    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'curso', 'carga_horaria', 'desc', 'professor', 'professor_name']
    
class ReservaSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='prof_resp.username', read_only=True) #pegar um campo espeficifo
    sala_name = serializers.CharField(source='sala.nome', read_only=True)
    disciplina_name = serializers.CharField(source='disc.nome', read_only=True)
    class Meta:
        model = ReservaAmbiente
        fields = '__all__'
    
class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'
        
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # usuario é como a data será tratada no json ou request 
        data['usuario'] = {
            'id': self.user.id, 
            'username': self.user.username,
            'email': self.user.email,
            'cargo': self.user.cargo, 
        }

        return data