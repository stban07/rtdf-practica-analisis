from django.urls import path
from .views import index, VocalizacionView, intensidad, save_audio, LoginView, registro, vocalizacion, preregistro, buscar_rut, preregistrados, grbas,rasati



urlpatterns = [
    path('', index, name="index"),
    path('vocalizacion/', vocalizacion, name="vocalizacion"),
    path('save_audio/', save_audio, name="save_audio"),
    path('intensidad/', intensidad, name="intensidad"),
    path('login/', LoginView.as_view(), name="login"),
    path('registro/', registro, name="registro"),
    path('preregistro/', preregistro, name="preregistro"),
    path('preregistrados/', preregistrados, name="preregistrados"),
    path('buscar_rut/', buscar_rut, name="buscar_rut"),
    path('grbas/', grbas, name="grbas"),
    path('rasati/', rasati, name="rasati"),
]
