from django.urls import path
from .views import ExampleModelList, ExampleModelDetail, Profesional_saludList, AudioList, botonesApiView, audioList_View, audioIntensidad_View, audioVocalizacion_View



urlpatterns = [
    path('', ExampleModelList.as_view(), name='examplemodel-list'),
    path('detalle/<int:pk>/', ExampleModelDetail.as_view(), name='examplemodel-detail'),
    path('profesional/', Profesional_saludList.as_view(), name='profesional-list'),
    path('audios/', AudioList.as_view(), name='audio-list'),
    path('botonesApi/', botonesApiView, name='botonesApi'),
    path('audiolist/', audioList_View, name='audiolist'),
    path('audiosVocalizacion/', audioVocalizacion_View, name='audiosVocalizacion'),
    path('audiosIntensidad/', audioIntensidad_View, name='audiosIntensidad'),   

]

