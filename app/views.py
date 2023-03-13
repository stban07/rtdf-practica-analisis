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


from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count





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
        if request.user.is_superuser:
            print(usuarios)
            return render(request, 'app/index.html',{"user_type":user_type, "usuarios":usuarios, "paciente":paciente, "profesional":profesional} )
        elif user_type == "Fonoaudilogo":

            data = Profesional_salud.objects.filter(rut_profesional = request.user.rut)

            id = data.values('id_profesional').first()
            id = id['id_profesional']
            pacientes = Profesional_Paciente.objects.filter(id_profesional_salud = id)
            print(pacientes)
            # id = pacientes.values('id_paciente').first()
            # print(id)



            books = Profesional_Paciente.objects.prefetch_related('id_paciente').filter(id_profesional_salud = id )
            pacientes = books

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

