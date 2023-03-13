from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
from django.shortcuts import redirect
import analisis.scripts as scripts
import os
import csv
import pandas as pd
from datetime import datetime
import plotly.express as px
from plotly.offline import plot
import urllib.request, json
from mysite.settings import BASE_DIR,MEDIA_ROOT

from app.models import Audio, AudiosCoeficientes, Usuario

def validate(request):
    if not (request.is_anonymous):
        if request.is_superuser:
            return True
    return False

@user_passes_test(validate)
def update_csv_view(request):
    if request.method == 'GET':
        #With this we render the page with an undetermined number of optional audio file inputs
        return render(request,"analisis/update_csv.html",{
            "title":"Actualizar CSV histórico"})

    if request.method == 'POST':
        #Getting the list of audio data from the URL
        #with urllib.request.urlopen("Api/audios/") as url:
        #    audio_list = json.load(url)
        audio_list = Audio.objects.all()

        #We read the historical CSV to get all id_audio and make a list with that
        with default_storage.open('historical.csv','r') as csvfile:
            csvreader = csv.reader(csvfile)
            #We use next to ignore the header
            next(csvreader)
            #Here we'll store the data that we need for the graph (username, date and the value that we want to show)
            id_list = []
            for row in csvreader:
                #This column has the already analyzed id_audio
                id_list.append(int(row[1]))
            csvfile.close()

        for audio_data in audio_list:

            url_audio = audio_data.url_audio
            #With this we ignore already analyzed audios
            is_calc=AudiosCoeficientes.objects.filter(nombre_archivo=str(url_audio))
            if not is_calc.exists():
                #Getting data from the JSON
                username = str(audio_data.idusuario)
                #add more if need
                date_formats=['%d-%m-%Y %H:%M:%S','%d-%m-%Y %H:%M.%S']
                for date in date_formats:
                    try:
                        timestamp = datetime.strptime(audio_data.timestamp, date)
                        break
                    except:
                        pass
                url_audio = str(audio_data.url_audio)

                audio_name = url_audio.split('/')[-1]

                #Opening the URL that has the audio
                #g = urllib.request.urlopen(url_audio)

                #Creating directory and CSV file in case we have a new user
                if not default_storage.exists('audios_api/'+username):
                    os.makedirs(os.path.join(MEDIA_ROOT,'audios_api/'+username))

                    with open(os.path.join(MEDIA_ROOT,'audios_api/'+username+'/audio_list.csv'), 'w', newline='') as csvfile:
                        fieldnames = ["id_audio","Nombre archivo","Timestamp","Fecha de calculo","F0","F1","F2","F3","F4","Intensidad","HNR","Local Jitter","Local Absolute Jitter", "Rap Jitter", "ppq5 Jitter","ddp Jitter","Local Shimmer","Local db Shimmer","apq3 Shimmer","aqpq5 Shimmer","apq11 Shimmer","dda Shimmer"]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        csvfile.close()

                #Storing the audio
                #with open('audios_api/'+username+'/'+audio_name, 'wb') as f:
                #    f.write(g.read())
                #    f.close()

                try:
                    #Now we also pass timestamp
                    print(audio_name)
                    print('*'*20)
                    res = scripts.audio_analysis(audio_name, audio_name, timestamp)
                    is_coefs=AudiosCoeficientes.objects.all().filter(nombre_archivo=audio_name)
                    id_user=int(username.split(' ')[0])
                    if not is_coefs.exists():
                        print('analizando')
                        coefs=AudiosCoeficientes.objects.create(
                            idusuario= Usuario.objects.get(id=id_user),
                            nombre_archivo = audio_name,
                            timestamp = timestamp,
                            F0  = res['f0'],
                            F1  = res['f1'],
                            F2  = res['f2'],
                            F3  = res['f3'],
                            F4  = res['f4'],
                            Intensidad  = res['Intensity'],
                            HNR  = res['HNR'],
                            Local_Jitter  = res['localJitter'],
                            Local_Absolute_Jitter  = res['localabsoluteJitter'],
                            Rap_Jitter  = res['rapJitter'],
                            ppq5_Jitter  = res['ppq5Jitter'],
                            ddp_Jitter = res['ddpJitter'],
                            Local_Shimmer = res['localShimmer'],
                            Local_db_Shimmer = res['localdbShimmer'],
                            apq3_Shimmer = res['apq3Shimmer'],
                            aqpq5_Shimmer = res['aqpq5Shimmer'],
                            apq11_Shimmer = res['apq11Shimmer']
                        )
                        coefs.save()
                        print('analizado')
                    #Writing the data on CSV files (now we also pass the audio's ID)
                    scripts.write_csv(res, username, 'audios_api/'+username+"/audio_list.csv",id_audio)
                    scripts.write_csv(res, username, "historical.csv",id_audio)
                except:
                    #In case there's an error with analyzing the audio file we write on the log
                    with open(os.path.join(MEDIA_ROOT,'log.txt'), 'a') as f:
                        f.write('[{0}] Hubo un error al analizar el archivo {1} del usuario {2}\n'.format(datetime.today().strftime('%Y-%m-%d %H:%M'), audio_name, username))
                        f.close()
                    #If the analysis fails we remove the file
                    #os.remove('audios_api/'+username+'/'+audio_name)

        #Finally redirect to the now updated CSV
        return redirect('/admin-analisis/historical/')

@user_passes_test(validate)
def upload_audio_view(request):
    if request.method == 'GET':
        #With this we render the page with an undetermined number of optional audio file inputs
        return render(request,"analisis/upload_audio.html",{
            "title":"Subir archivos",
            "range":range(2,6)})

    if request.method == 'POST':
        username = request.POST['username']

        #Checking if a user is uploading for the first time (to create folder and CSV file)
        #We now store stuff on the web folder
        new_user = not os.path.isdir('web/'+username)

        #Saving and analyzing the received audios (the directory is created here in case we have a new user)
        audio_list = request.FILES.getlist('audio')
        for audio in audio_list:
            audio_name = default_storage.save('web/'+username+'/'+audio.name, audio)
            try:
                res = scripts.audio_analysis(audio_name, audio.name)

                #Creating CSV file in case we have a new user
                if new_user:
                    with open(os.path.join(MEDIA_ROOT,'web/'+username+'/audio_list.csv'), 'w', newline='') as csvfile:
                        fieldnames = ["Nombre archivo","Timestamp","Fecha de calculo", "F0","F1","F2","F3","F4","Intensidad","HNR","Local Jitter","Local Absolute Jitter", "Rap Jitter", "ppq5 Jitter","ddp Jitter","Local Shimmer","Local db Shimmer","apq3 Shimmer","aqpq5 Shimmer","apq11 Shimmer","dda Shimmer"]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        new_user = False
                        csvfile.close()

                #Writing the data on CSV files
                scripts.write_web_csv(res, username, 'web/'+username+"/audio_list.csv")
                scripts.write_web_csv(res, username, "web_historical.csv")
            except:
                pass

        #Displays a table with all the audios uploaded by this user (including previously uploaded ones in case they exist)
        return HttpResponseRedirect('/admin-analisis/show_audio/?username=web/'+username)

@user_passes_test(validate)
def show_audio_view(request):
    username = request.GET["username"]
    #Reads the CSV and puts its information in an array
    with default_storage.open(username+'/audio_list.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)
        csv_list = []
        for row in csvreader:
            csv_list += [row]
        csvfile.close()
    #We render the page with the information we got
    return render(request,"analisis/table_display.html", {
        "title":"Audios de {0}".format(username.split('/')[-1]),
        "args":csv_list[0],
        "audios":csv_list[1:],
        "filename":username+'/audio_list.csv'})

@user_passes_test(validate)
def historical_csv_view(request):
    #Reads the CSV and puts its information in an array
    list_coef=AudiosCoeficientes.objects.all().values()
    vals=[]
    for row in list_coef:
        vals+=[row.values()]
    #We render the page with the information we got
    return render(request,"analisis/table_display.html", {
        "title":"coeficientes histórico",
        "args":list_coef[0].keys(),
        "audios":vals,
        "filename":"historical.csv"})

#Identical to the previous one, but for web upload
@user_passes_test(validate)
def web_historical_csv_view(request):
    #Reads the CSV and puts its information in an array
    with default_storage.open('web_historical.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)
        csv_list = []
        for row in csvreader:
            csv_list += [row]
        csvfile.close()
    #We render the page with the information we got
    return render(request,"analisis/table_display.html", {
        "title":"CSV Web",
        "args":csv_list[0],
        "audios":csv_list[1:],
        "filename":"web_historical.csv"})

@user_passes_test(validate)
def download_file(request):
    filename = request.GET["filename"]
    #This gives us the path without the extension
    path = filename[:len(filename)-4]

    #If we don't get a file named log means we have to generate an Excel to download
    if path != 'log':
        #We create an Excel file from our CSV file and save it alongside it
        read_file = pd.read_csv(filename, delimiter=",")
        new_file = pd.ExcelWriter(path+".xlsx")
        read_file.to_excel(new_file, index = False)
        new_file.save()

        #With this we trigger the file download
        with default_storage.open(path+".xlsx", 'rb') as xlsx_file:
            response = HttpResponse(xlsx_file, content_type='application/vnd.openxmlformatsofficedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(path+".xlsx")
            return response
    else:
        #With this we trigger the download of log.txt
        with default_storage.open("log.txt", 'rb') as log_file:
            response = HttpResponse(log_file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=log.txt'
            return response

@user_passes_test(validate)
def hourly_graph_view(request):
    #Renders the selector after selecting graph type
    return render(request, "analisis/graph_hourly.html",{
        "title":"Selección de coeficiente",
        "format":"hourly",
        "args":["F0","F1","F2","F3","F4","Intensidad","HNR","Local Jitter","Local Absolute Jitter", "Rap Jitter", "ppq5 Jitter","ddp Jitter","Local Shimmer","Local db Shimmer","apq3 Shimmer","aqpq5 Shimmer","apq11 Shimmer","dda Shimmer"]
    })

@user_passes_test(validate)
def historical_graph_view(request):
    #Renders the selector after selecting graph type
    return render(request, "analisis/graph_historical.html",{
        "title":"Selección de coeficiente",
        "format":"historical",
        "args":["F0","F1","F2","F3","F4","Intensidad","HNR","Local Jitter","Local Absolute Jitter", "Rap Jitter", "ppq5 Jitter","ddp Jitter","Local Shimmer","Local db Shimmer","apq3 Shimmer","aqpq5 Shimmer","apq11 Shimmer","dda Shimmer"]
    })

@user_passes_test(validate)
def display_hourly_graph_view(request):
    #This index that represents the value we have to display
    index = request.GET["index"]
    queryvals=AudiosCoeficientes.objects.all().values()
    #Here we'll store the data that we need for the graph (username, date and the value that we want to show)
    user_list = []
    date_list = []
    arg_list = []
    arg_name=''
    for row in queryvals:

        id_usuario=list(row.values())[1]
        user_list.append(Usuario.objects.get(id=id_usuario))
        date_list.append(str(list(row.values())[3]))
        #To get the desired value, we have to add 4 to the index received (id,idusuario,nombre_archivo,timestamp,data...)
        arg_list.append(list(row.values())[int(index)+4])
        if arg_name=='':
            arg_name=list(row.keys())[int(index)+4]

    #Since we want to show only based on the hour, we set all dates to the same year, month and day, so that hour and minutes are the only difference (the date was picked arbitrarily)
    #The data in the CSV is stored as strings, so we change it to the correct type
    date_list=[datetime.strptime(x, '%Y-%m-%d %H:%M:%S').replace(year=2010,month=1,day=1) for x in date_list]
    arg_list=[float(d) for d in arg_list]

    #The first element of each list is the label, and the rest are the values
    df = pd.DataFrame(data={"Usuario":user_list,"Timestamp":date_list,arg_name:arg_list})
    fig = px.scatter(df, x="Timestamp", y=arg_name, color="Usuario", template='plotly_dark')
    #If we don't change the format, it'll show that all files were uploaded on the same day, which is not ideal
    fig.update_xaxes(tickformat="%H:%M")
    div = plot(fig, auto_open=False, output_type='div')
    return render(request,"analisis/display_graph.html", {
        "title":"Análisis de {0} por hora del día".format(arg_name),
        "graph":div})

@user_passes_test(validate)
def display_historical_graph_view(request):
    #This index that represents the value we have to display
    index = request.GET["index"]
    queryvals=AudiosCoeficientes.objects.all().values()
    #Here we'll store the data that we need for the graph (username, date and the value that we want to show)
    user_list = []
    date_list = []
    arg_list = []
    arg_name=''
    for row in queryvals:
        id_usuario=list(row.values())[1]
        user_list.append(Usuario.objects.get(id=id_usuario))#row.idusuario)
        date_list.append(str(list(row.values())[3]))#row.timestamp)
        #To get the desired value, we have to add 5 to the index received (the first 2 rows are for username, id_audio, filename, timestamp and upload date)
        arg_list.append(list(row.values())[int(index)+4])
        if arg_name=='':
            arg_name=list(row.keys())[int(index)+4]
    #The data in the CSV is stored as strings, so we change it to the correct type
    date_list=[datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in date_list]
    arg_list=[float(x) for x in arg_list]


    df = pd.DataFrame(data={"Usuario":user_list,"Timestamp":date_list,arg_name:arg_list})
    fig = px.line(df, x="Timestamp", y=arg_name, color="Usuario", template='plotly_dark')
    div = plot(fig, auto_open=False, output_type='div')
    return render(request,"analisis/display_graph.html", {
        "title":"Análisis histórico de {0}".format(arg_name),
        "graph":div})

@user_passes_test(validate)
def user_list_view(request):
    #Renders a list with all users

    user_list = []
    users=Usuario.objects.filter(id_tipo_user=3)

    for row in users:
        user_list.append(row)

    return render(request, "analisis/user_list.html",{
        "title":"Selección de usuario",
        "users":[*set(user_list)]
    })

@user_passes_test(validate)
def user_info_view(request):
    #Renders the info of the requested user
    user = request.GET["user"]
    user_id=int(user.split(' ')[0])
    try:
        user=Usuario.objects.get(id=user_id)
    except:
        return render(request,"analisis/error.html",{'error_msg':'usuario no encontrado'})
    try:
        coef_id= int(request.GET["id"])
        audios_coef=AudiosCoeficientes.objects.filter(idusuario=user,id=coef_id).values().first()
    except:
        audios_coef=AudiosCoeficientes.objects.filter(idusuario=user).values()
        if audios_coef:
            audios_coef=audios_coef.last()
        else:
            return render(request, "analisis/user_info.html",{
                "title":"Selección de usuario",
                "user":user,
                "args":{'null':'paciente sin data registrada'}
                })
    audios_coef.pop('id')
    audios_coef.pop('idusuario_id')
    nombre_archivo=audios_coef.pop('nombre_archivo')
    timestamp={'Fecha de calculo':audios_coef.pop('timestamp')}
    audios_coef={**timestamp,**audios_coef}

    try:
        ajax=int(request.GET['ajax'])
        if ajax==1:
            return render(request, "analisis/user_info_ajax.html",{
        "title":"Selección de usuario",
        "user":user,
        "args":audios_coef,
        "audio_list":AudiosCoeficientes.objects.filter(idusuario=user).order_by('-id'),
        "audio": '/media/'+nombre_archivo
    })
    except:
        pass

    return render(request, "analisis/user_info.html",{
        "title":"Selección de usuario",
        "user":user,
        "args":audios_coef,
        "audio_list":AudiosCoeficientes.objects.filter(idusuario=user).order_by('-id'),
        "audio": '/media/'+nombre_archivo
    })


