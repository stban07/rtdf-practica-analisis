from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields =  ('email','username', 'first_name', 'last_name', 'id_tipo_user', 'password1', 'password2','rut')







class PreRegistroFrom(forms.ModelForm):
    class Meta():
        model = PreRegistro
        fields = ('rut','nombre', 'apellido'  , 'email', 'telefono','tipo_user')


class GrbasFrom(forms.ModelForm):
    class Meta():
        model = Grbas
        fields = ('id_fonoaudilogo','id_paciente','G','R','B','A','S','Comentario')




class RasatiFrom(forms.ModelForm):
    class Meta():
        model = Rasati
        fields = ('id_fonoaudilogo','id_paciente','R','A','S','A','T','I','Comentario')

class CoeficientesForm(forms.ModelForm):
    class Meta():
        model = AudiosCoeficientes_Fono
        fields= ("idusuario","nombre_archivo", "timestamp","Intensidad","F0","F1","F2","F3","F4","Intensidad","HNR","Local_Jitter","Local_Absolute_Jitter","Rap_Jitter","ppq5_Jitter","ddp_Jitter","Local_Shimmer","Local_db_Shimmer","apq3_Shimmer","aqpq5_Shimmer","apq11_Shimmer")


# class MemoriceForm(forms.ModelForm):
#     acierto = forms.CharField(label='Cantidad de aciertos', widget=forms.TextInput(
#         attrs={

#             'placeholder': 'Ingresa cantidad de aciertos',
#             'id': 'total_acierto'
#         }))

#     tiempo = forms.CharField(label='Cantidad de tiempo', widget=forms.TextInput(
#         attrs={

#             'placeholder': 'Ingresa cantidad de tiempo',
#             'id': 'total_tiempo'
#         }))

#     movimientos = forms.CharField(label='Cantidad de movimientos', widget=forms.TextInput(
#         attrs={

#             'placeholder': 'Ingresa cantidad de movimientos',
#             'id': 'total_movimientos'
#         }))

#     class Meta:
#         model = Memorice
#         fields = 'acierto', 'tiempo', 'movimientos'

# # EJERCICIO PALABRAS


# class VocalPalabras(forms.ModelForm):
#     class Meta:
#         model = VocalPalabras
#         fields = '__all__'

# # LECTURA DE TEXTO


# class VocalTexto(forms.ModelForm):
#     class Meta:
#         model = VocalTexto
#         fields = '__all__'
