from rest_framework import serializers
from .models import ExampleModel

from app.models import Profesional_salud, Usuario, TipoUsuario, Audio
# from app.models import Profesional_salud, Usuario, TipoUsuario, Audio, AudiosCoeficientes

class ExampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleModel
        fields = '__all__'


class Profesional_saludSerializer(serializers.ModelSerializer):
    institucion_id = serializers.CharField(source='institucion_id.nombre_institucion')
    id_usuario = serializers.CharField(source='id_usuario.id_tipo_user.nombre_tipo_usuario')
    class Meta:
        model = Profesional_salud
        fields = ('id_profesional', 'id_usuario', 'rut_profesional', 'institucion_id')


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

