from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
from datetime import datetime
from app import forms

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum





def validate(request):
    if request.is_anonymous:
        print(request)
        return False
    elif request:
        print(request)
        return True


############### VISTAS #####################

def index(request):
    #duplicates =  Profesional_salud.objects.values('rut_profesional').annotate(count=Count('rut_profesional')).filter(count__gt=1)
    #print(duplicates)
    if request.user.is_authenticated == True:
        user_type = str(request.user.id_tipo_user)
        print(user_type)
        usuarios = Usuario.objects.all()
        paciente = Paciente.objects.all()
        profesional = Profesional_salud.objects.all()
        pacientes=Usuario.objects.filter(id_tipo_user=3).annotate(count=Count('audioscoeficientes')).filter(count__gte=1)
        total=pacientes.aggregate(total=Sum('count'))['total']
        if request.user.is_superuser:
            print(usuarios)
            return render(request, 'app/index.html',{"user_type":user_type, "usuarios":usuarios, "paciente":paciente, "profesional":profesional,  "Audio_coeficiente": pacientes,"conteo":total} )
        elif user_type == "Fonoaudiólogo":
            try:
                data = Profesional_salud.objects.filter(rut_profesional = request.user.rut)

                id = data.values('id_profesional').first()
                id = id['id_profesional']
                pacientes = Profesional_Paciente.objects.filter(id_profesional_salud = id)
                print(pacientes)
            # id = pacientes.values('id_paciente').first()
            # print(id)
            #books = Profesional_Paciente.objects.prefetch_related('id_paciente').filter(id_profesional_salud = id )
            #pacientes = books
            except:
                pass
            d = Paciente.objects.all()
            print(d)


            return render(request, 'app/index.html',{"user_type":user_type, "pacientes":pacientes} )
    else:
        user_type = str(request.user)
    print(user_type)
    return render(request, 'app/index.html',{"user_type":user_type} )





@user_passes_test(validate)
def grbas(request):
    if request.method == 'GET':
        username = str(request.user.username)
        rut = str(request.user.rut)
        user_type = str(request.user.id_tipo_user)
        formulario = GrbasFrom(initial={'id_fonoaudilogo': username})

        data = Profesional_salud.objects.filter(rut_profesional = request.user.rut)
        data.count()
        if data.count() == 1:
            form = Grbas.objects.filter(id_fonoaudilogo = username )
            id = data.values('id_profesional').first()
            id = id['id_profesional']
            pacientes = Profesional_Paciente.objects.filter(id_profesional_salud = id)
            print(pacientes)
            return render(request, 'app/grbas.html',{"user_type":user_type, "paciente":pacientes, "form":form, "formulario":formulario})
        else:
            if request.user.is_superuser:
                form = Grbas.objects.all()
                return render(request, 'app/grbas.html',{"user_type":user_type, "form":form })
            else:
                print("no tiene pacientes")
                return render(request, 'app/grbas.html',{"user_type":user_type})

    if request.method == 'POST':
        print("GUARDADO")
        form = GrbasFrom(data=request.POST)
        if form.is_valid():
            print("GUARDADO")

            form.save()
            form.clean()
            return redirect("grbas")
        else:
            print(form.errors)




@user_passes_test(validate)
def rasati(request):

    if request.method == 'GET':


        username = str(request.user.username)
        rut = str(request.user.rut)
        user_type = str(request.user.id_tipo_user)
        formulario = RasatiFrom(initial={'id_fonoaudilogo': username})

        data = Profesional_salud.objects.filter(rut_profesional = request.user.rut)
        data.count()
        if data.count() == 1:
            form = Rasati.objects.filter(id_fonoaudilogo = username )
            id = data.values('id_profesional').first()
            id = id['id_profesional']
            pacientes = Profesional_Paciente.objects.filter(id_profesional_salud = id)

            return render(request, 'app/rasati.html',{"user_type":user_type, "paciente":pacientes, "form":form, "formulario":formulario})
        else:
            if request.user.is_superuser:
                form = Rasati.objects.all()
                return render(request, 'app/rasati.html',{"user_type":user_type, "form":form })
            else:
                print("no tiene pacientes")
                return render(request, 'app/rasati.html',{"user_type":user_type})


    if request.method == 'POST':
        print("GUARDADO")
        form = RasatiFrom(data=request.POST)
        if form.is_valid():
            print("GUARDADO")

            form.save()
            form.clean()
            print("guardadoooo")
            return redirect("rasati")
        else:
            print(form.errors)

#vista principal para agregar audios de manera manual
#contenedor de informacion se actualiza por medio de js
#con peticion ajax para tener lista de pacientes y formulario de coeficientes
@user_passes_test(validate)
def audios_pacientes(request):
    user_type = str(request.user.id_tipo_user)
    return render(request,'app/audios-pacientes.html',{"user_type":user_type})

@user_passes_test(validate)
def lista_pacientes(request):
    if request.method == 'GET':
        user_type = str(request.user.id_tipo_user)
        if user_type == 'Fonoaudiólogo':
            #si el usuario es fonoaudiologo buscara todas sus entradas en Profesional_Paciente
            #luego filtrara los usuarios que sean llave foranea Rpaciente en esta lista
            #finalmente contara los audios que contienen en audioscoeficientes y mostrara aquellos con al menos un audio analizado
            try:
                pacientes_medico=Profesional_Paciente.objects.filter(id_profesional_salud=request.user)
                pacientes=Usuario.objects.filter(Rpaciente__in=pacientes_medico)
                pacientes=pacientes.annotate(count=Count('audioscoeficientes')).filter(count__gte=1)

            except Exception as e:
                return render(request, 'app/lista-pacientes.html',{'pacientes':{}})
            return render(request, 'app/lista-pacientes.html',{'pacientes':pacientes})
        if request.user.is_superuser:
            pacientes=Usuario.objects.filter(id_tipo_user=3).annotate(count=Count('audioscoeficientes')).filter(count__gte=1)
            return render(request, 'app/lista-pacientes.html',{'pacientes':pacientes})
        return render(request, 'app/lista-pacientes.html',{'pacientes':{}})


#vista de form para añadir coeficientes a un audio
#requiere recibir por medio de un get un id de audio
#en caso de no tenerlo vuelve a pacientes_audios
#posteriormente verificar que el fonoaudiologo tiene acceso a ese audio (por medio del paciente)
@user_passes_test(validate)
def form_coeficientes(request):
    user_type = str(request.user.id_tipo_user)
    if request.method == 'GET':
        paciente=int(request.GET['paciente'])
        first_time=True;
        #buscamos los audios del paciente, revisamos cual tiene la id indicada y en caso contrario tomamos el primer elemento
        #mismo funcionamiento que en analisis
        try:
            coef_id = int(request.GET["id"])
            audios_coef=AudiosCoeficientes.objects.filter(idusuario=paciente,id=coef_id).values().first()
            first_time=False;

        except:
            audios_coef=AudiosCoeficientes.objects.filter(idusuario=paciente).values()
            if audios_coef:
                audios_coef=audios_coef.last()
            else:
                return
        #quitar los valores innecesarios para mostrar, como datos para el servidor (dejar solo valores de coeficientes)
        audio_name=audios_coef.pop('nombre_archivo')
        timestamp=audios_coef.pop('timestamp')
        audios_coef.pop('idusuario_id')
        audios_coef.pop('id')
        #una vez tenemos el audio seleccionado revisamos en la tabla AudiosCoeficientes_Fono si ya existe la entrada para ese audio
        #en caso de existir mostramos la comparacion con la tabla AudiosCoeficientes
        #de no existir mostramos el formulario
        try:
            print(audio_name)
            coef_fono=AudiosCoeficientes_Fono.objects.filter(nombre_archivo=audio_name).values().first()
            print("existe")
            keys=list(audios_coef.keys())
            #hacemos un nuevo diccionario que contiene los valores de ambos conjuntos para compararlos
            #solo deben quedar coeficientes, por lo que podemos operarlos para mostrar la diferencia
            comparative_table={k:{"fono":coef_fono[k],"auto":audios_coef[k],"dif":abs(float(coef_fono[k])-(float(audios_coef[k])))} for k in keys}
            return render(request,'app/coeficientes-manual.html',{
                "user_type":user_type,
                "paciente": Usuario.objects.get(id=paciente),
                "audio_list":AudiosCoeficientes.objects.filter(idusuario=paciente).order_by('-id'),
                "comparative_table":comparative_table,
                "audio": '/media/'+audio_name,
                "first_time":first_time, #first_time hace que se renderice la lista de audios, en false no se actualiza
                "manual_exist":True      #manual_exist avisa cuando ya encuentra una entrada del fonoaudiologo
                })
        except Exception as e:
            print(e)
            form_coef=CoeficientesForm(initial={"idusuario":paciente,"nombre_archivo":audio_name,"timestamp":timestamp})
            return render(request,'app/coeficientes-manual.html',{
                "user_type":user_type,
                "paciente": Usuario.objects.get(id=paciente),
                "audio_list":AudiosCoeficientes.objects.filter(idusuario=paciente).order_by('-id'),
                "form":form_coef,
                "audio": '/media/'+audio_name,
                "first_time":first_time,
                "manual_exist":False
                })
    if request.method == 'POST':
        #recibe los parametros y los guarda en la tabla audioscoeficientes_fono
        #probablemente renderice la misma pestaña que el get, con un mensaje extra de guardado
        print("GUARDADO")
        data=request.POST
        print(data)
        print("="*50)
        form = CoeficientesForm(data=request.POST)
        if form.is_valid():

            form.save()
            form.clean()

            return redirect('audio_pacientes')

        return render(request,'app/coeficientes-manual.html',{"user_type":user_type})













@user_passes_test(validate)
def vocalizacion(request):
    #DESCOMENTAR ESTO ES PARA OBTENER LOS DATOS DEL PACIENTE, PARAMETROS Y MOSTRAR EN EL FRONT SE NECESITA EL ID PARA BUSCAR
    # # obj = Parametros.objects.get()
    # # pac = Paciente.objects.get()
    # # {"parametros":obj,"paciente":pac}
    user_type = str(request.user.id_tipo_user)
    return render(request, 'app/vocalizacion.html',{"user_type":user_type})


@user_passes_test(validate)
def intensidad(request):
    user_type = str(request.user.id_tipo_user)
    return render(request, 'app/intensidad.html',{"user_type":user_type})

############### INTENSIDAD #####################


class IntensidadView(View):
    def post(self, request, *args, **kwargs):
        return render(request, 'app/intensidad.html')















def registro(request):
    dato = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        print("re")
        formulario = CustomUserCreationForm(data=request.POST)
        print(formulario.data)
        if formulario.is_valid():
            formulario.save()
            print("registro")
            # user = authenticate(username = formulario.cleaned_data["username"], password= formulario.cleaned_data["password1"])
            # login(request, user)
            messages.success(request,"te has registrado correctamente")
        return redirect('login')
    return render(request, 'registration/registro.html', dato)


# ###################### PreRegistro #######################
@csrf_exempt
def preregistro(request):

    if request.method == 'POST':
        print("ssss")
        form = PreRegistroFrom(data=request.POST)

        if form.is_valid():
            print("ss3ss")
            rut = form.cleaned_data['rut']
            tipouser = form.cleaned_data['tipo_user']
            form.save()
            print(tipouser)
            if tipouser == 'FonoAudiologo':
                obj = Fonoaudilogos.objects.get(rut=rut)
                obj.preregistrado = 1
                obj.save()
            else:
                form.save()
            return render(request, 'app/preregistro.html', {"form":form})
        else:
            print(form.errors)
    else:
        print("ss32221ss")
        form = PreRegistroFrom()
        return render(request, 'app/preregistro.html', {"form":form})

    if request.method == 'GET':
        form = PreRegistroFrom()
        return render(request, 'app/preregistro.html', {"form":form})




@csrf_exempt
def preregistrados(request):


    data = PreRegistro.objects.all()


    if request.method == 'POST':

        formulario = CustomUserCreationForm(request.POST)
        print("post")
        if formulario.is_valid():
            formulario.save()
            formulario.clean()
            print("sqave")
            return render(request, 'app/preregistrados.html', {"data":data,'form': CustomUserCreationForm()})
        else:
            print(formulario.errors)
            # user = authenticate(username = formulario.cleaned_data["username"], password= formulario.cleaned_data["password1"])
            # login(request, user)
        formulario.clean()
        return render(request, 'app/preregistrados.html', {"data":data,'form': CustomUserCreationForm()})


    if request.method == 'GET':
        print("registro1")
        form = PreRegistroFrom()




    return render(request, 'app/preregistrados.html', {"data":data,'form': CustomUserCreationForm()})







@csrf_exempt
def buscar_rut(request, *args, **kwargs):
    if request.method == 'POST':
        rutFono = request.POST.get('rut')
        print(rutFono)
        objetos = Fonoaudilogos.objects.filter(rut=rutFono).filter(preregistrado=0)
        obj = Fonoaudilogos.objects.filter(rut=rutFono)
        print(obj.count())
        print(objetos.count())
        if objetos.count() == 1:
            datos = Fonoaudilogos.objects.get(rut=rutFono)
            # tipoUser = TipoUsuario.objects.get(nombre_tipo_usuario="Paciente")
            fono = {'Nombre': datos.NombreCompleto, 'rut': datos.rut}
            return JsonResponse(fono)
        elif objetos.count() == 0 and obj.count() == 0:
            pre = PreRegistro.objects.filter(rut=rutFono)
            if pre.count() == 1:
                fono = {'STOP':'STOP'}
                print("YA ESTA PREREGISTRADO")
                return JsonResponse(fono)
            else:
                fono = {'SI':'SI'}
                print("SIN REGISTRO EN BD")
                return JsonResponse(fono)


        elif objetos.count() == 0:
            print("FONOAUDILOGO PREREGISTRADO")
            fono = {'NO':'NO'}
            return JsonResponse(fono)









# ###################### LOGICA PARA GUARDAR AUDIO #######################
@csrf_exempt
def save_audio(request, *args, **kwargs):

    if request.method == 'POST':
        #generamos token para evitar que se sobre escriba MODIFICAR
        print(request.user.username)
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        hms = now.strftime("%H-%M-%S")
        token = get_random_string(length=2)
        nombre = request.POST.get('string')
        archivo = f"{token}_{hms}_{nombre}.wav"
        audio_file = request.FILES.get('file')
        #Guarda el archivo
        arc = default_storage.save(archivo,audio_file)

        document = Audio.objects.create(url_audio=arc,timestamp=current_time,idusuario=request.user)
        document.save()
        return HttpResponse("200")


    return render(request, 'app/vocalizacion.html')

########################## VOCALIZACION ################################
############## CONFIGURAR CORRECTAMENTE PARA GUARDAR#####################










class VocalizacionView(View):
    def post(self, request):
        return render(request, 'app/vocalizacion.html')







class LoginView(View):
    def get(self, request, *args, **kwargs):
        print("HOLA")
        return render(request, 'app/login.html')

    def post(self, request):
        if request.method == 'POST':
            print(request.POST)
            formulario = CustomUserCreationForm(data=request.POST)
            print(formulario)
            if formulario.is_valid():
                print("postttt")
                user = authenticate(username = formulario.cleaned_data["username"], password= formulario.cleaned_data["password"])
                login(request, user)
                messages.success(request,"te has registrado correctamente")
                return redirect(to='app/index.html')
        return render(request, 'app/login.html')

