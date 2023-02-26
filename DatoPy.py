import shutil,time,os,configparser,fileinput,time,glob
from tkinter import *
from tkinter.ttk import *
import time
import subprocess
import threading
import datetime
import logging
import sys
import tkinter as tk
from PIL import Image


carpetas=["data","BITMAPS","FORMS","icons","Inicio","LIBS","MENUS","PROGS","REPORTS","txrx"]
#ruta_local = os.path.dirname(os.path.abspath(__file__))
ruta_remota="\\\\127.0.0.1\\archivos_de_prueba"
ruta_dato="ejecutar_al_finalizar.bat" #Ejecutable de datos4
cerrar_dto = "Taskkill /IM dato45.exe /F" #Cerrar Programa a actualizar

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-s) %(message)s')






def ruta_local():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir)



#################### TKINTER ##################
def actualizar():

    def version_log():
        ##LOCAL
        lo=open("version.log","r")
        vers_loc=lo.readlines()
        lo.close()
        #REMOTO
        re=open(ruta_remota+"\\version.log","r")
        vers_rem=re.readlines()
        re.close()
    
        loc =int(vers_loc[0].rstrip())
        rem =int(vers_rem[0].rstrip())
        ####print("Version LOCAL =",loc," - Version REMOTA=",rem)
        ##AL FINALIZAR actualizar version
        lo=open("version.log","r+")
        loc=str(rem)+'\n'
        lo.seek(0)
        lo.writelines(str(loc))
        lo.close()
    
    
    def cancelar():
        #print("Iniciar Dato")

        subprocess.Popen(ruta_dato)
        sys.exit()
        #label.config(text=count)
        #label2.pack()    
    
    def tk_ventana(cual_ventana):
        global porcentaje
        global carpeta_act
        global titulo
        global finalizar
        global finaliza_hilo

        if cual_ventana == 1:
            ##print("Cual ventana igual a 1")
            def llamar_iniciar():
                ##print("Aqui 1")
                window.destroy()
                t2=tk_ventana(2)
            def llamar_cancelar():
                ##print("Aqui 2")
                cancelar()


            window = Tk()
            window.resizable(0,0)
            window.configure(bg='white')    
            ancho_ventana = 310
            alto_ventana = 330
            x_ventana = window.winfo_screenwidth() // 2 - ancho_ventana // 2
            y_ventana = window.winfo_screenheight() // 2 - alto_ventana // 2
            posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
            window.geometry(posicion)    
            window.iconbitmap("dato.ico")
            window.title('Actualizar Dato')    
            style = Style() 
            style.configure('W.TButton', font =
                           ('calibri', 25, 'bold'),
                            foreground = '#08870e')    
            style2 = Style() 
            style2.configure('TButton', font =
                           ('calibri', 25, 'bold'),
                                borderwidth = '4',foreground = '#bd2109')    
            #BOTON1
            button = Button(window,text='Actualizar',style = 'W.TButton')
            button.config(command=llamar_iniciar)
            
            #BOTON2
            button2 = Button(window,text='Cancelar',style = 'TButton')
            button2.config(command=llamar_cancelar)    
            
            label0 = Label(window,background='white')
            label1 = Label(window,text='               DATO4 \n Actualización Disponible',background='white',font='arial 16 bold')
            label2 = Label(window,background='white')
            label3 = Label(window,background='white')   
            
            
            label0.pack()
            label1.pack()
            label2.pack()
            button.pack(padx=10, pady=15)
            label3.pack()
            button2.pack(padx=20, pady=30)
            
            
            
            window.mainloop()

        elif cual_ventana == 2:
            ##print("Cual ventana igual a 2")
            def llamar_loop():
                
                window = Tk()
                window.resizable(0,0)
                window.configure(bg='white')    
                ancho_ventana = 310
                alto_ventana = 360
                x_ventana = window.winfo_screenwidth() // 2 - ancho_ventana // 2
                y_ventana = window.winfo_screenheight() // 2 - alto_ventana // 2
                posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
                window.geometry(posicion)    
                window.iconbitmap("dato.ico")
                window.title('Actualizar Dato')    
                style = Style() 
                style.configure('W.TButton', font =
                               ('calibri', 20, 'bold'),
                                foreground = '#07ad0f')    
                style2 = Style() 
                style2.configure('TButton', font =
                               ('calibri', 20, 'bold'),
                                    borderwidth = '4',foreground = 'red')    
                  
                
                label0 = Label(window,background='white')
                label1 = Label(window,text='    ACTUALIZANDO... \n ',background='white',font='arial 14 bold')
                label2 = Label(window,background='white')
                label3 = Label(window,background='white')                 
                
                
                label0.pack()
                label1.pack()

                ##GIf
                file="dato_py.gif"
                info = Image.open(file)
                frames = info.n_frames
                im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]
                gif_label = tk.Label(window,image="",background='white')
                gif_label.pack()
                count = 0
                anim = None



                label2.pack()
                label3.pack()

                s = Style()
                #s.theme_use("default")
                s.configure("TProgressbar", thickness=50)

                label_progress2 = Label(window, font='arial 13 bold',background='white')
                label_progress2.pack(padx=20, pady=1)
                progress = Progressbar(window, style="TProgressbar", length=250, mode="determinate")
                progress.pack(padx=10, pady=15)
                label_progress = Label(window, font='arial 18 bold',background='white')
                label_progress.pack(padx=100, pady=3)

                label_progress.config(text="0 %")
                label_progress2.config(text="1 de "+ str(len(carpetas)))
                window.update_idletasks()

                

                while finalizar == False:
                    try:
                        im2 = im[count]
                        gif_label.configure(image=im2)
                        count += 1
                        if count == frames:
                            count = 0

                        if titulo != "":
                            window.title('Procesando...'+titulo)
                        label_progress2.config(text=str(carpeta_act)+" de "+ str(len(carpetas)))
                        progress['value'] = porcentaje
                        time.sleep(0.1)
                        label_progress.config(text=str(porcentaje)+"%")
                        if finalizar == True:## NO se impleenta
                            label_progress.config(text="Iniciando Sistema...",font='arial 9 bold')
                            time.sleep(0.1)
                            quit()
                        
                        window.update()
                    except Exception as e:
                        ##print("Error aqui:",str(e))
                        global finaliza_hilo
                        finaliza_hilo=True
                        quit()

                
                window.mainloop()


            def llamar_iniciar():
                global porcentaje
                global carpeta_act
                global titulo
                global finalizar
                global finaliza_hilo

                #logging.info("Consultando Debug1...")
                subprocess.Popen(cerrar_dto) ##Cerrar Datos abiertos
                can_carpetas=len(carpetas)
                contar=0
                
                for carpeta in carpetas:
                    if porcentaje == 100:
                        time.sleep(3)
                        porcentaje=1
                    if finaliza_hilo == True:
                        break
                    contar=contar+1 ##para contar la carpeta actual
                    ##print("Procesando carpeta:",carpetas[contar-1])
                    #logging.info("Consultando Debug2...")
                    titulo=carpetas[contar-1] ## Variable global
                    carpeta_act=contar##para contar la carpeta actual (Modifico Variable global)
                    lista=sincronizar(carpeta)
                    ###print("PASE1 lista:",lista)
                    contar_archivos=len(lista)
                    vueltas=1 ##compara mas adelante
                    if contar_archivos == 0 :
                        contar_archivos =1
                
                    ###print("PASE2 contar_archivos::",contar_archivos)
                
                    ##### !!! Revisar aqui, cuando los archivos a pasar sean mas de 100 hay que cambiar la division
                
                    if contar_archivos <= 100:
                        div=int(100 / contar_archivos)
                        div2=div
                    else:
                        div=100 / contar_archivos
                        div2=div                
                
                    ###print("PASE 3 div:::",div)                
                    if lista:
                        #for i in range(7,101,):
                        for archivo in lista:
                            if finaliza_hilo == True:
                                break
                            #logging.info("Consultando Debug3...archivo: "+archivo)
                            if div >= 99:
                                div=100

                            copiar_reemplazar(carpeta,archivo)

                            if vueltas == contar_archivos:
                                ####print("Entre aqui")
                                div=100
                            porcentaje = int(div)
                            vueltas=vueltas+1
                            if div >= 100:
                                continue #finalizar bucle de lista actual
                            div=div+div2
                
                    else:
                        # Si lista viene vacio, simular 100%
                        porcentaje = 100                
                
                
                    #break ## Provisorio frena bule de carpetas
                    
                
                if finaliza_hilo==True:
                    quit()
                
                subprocess.Popen(ruta_dato)
                version_log()
                finalizar=True

            



            porcentaje=0
            carpeta_act=0
            titulo=""
            finalizar=False
            finaliza_hilo=False
            threads=list()
            hilo3=threading.Thread(target=llamar_loop)
            hilo4=threading.Thread(target=llamar_iniciar)
            threads.append(hilo4)
            threads.append(hilo3)
            try:
                for t in threads:
                    ##print("Hilo...==>",str(t),"\n")
                    t.start()
                for t in threads:
                    t.join()
                    ##print("FIN:=>",str(t))
            except:
                ##print("Error en HILOS")
                finaliza_hilo=True
    


    ventana=tk_ventana(1)

################## FIN TKINTER ################









def verifico_carpetas(carpetas):
    for carpeta in carpetas:
        try:
            os.stat(carpeta)
        except:
            os.mkdir(carpeta)


def procesar_datos(carpeta,ubi):
    lista_fechas=[]
    lista_local=[]
    if ubi == "local":
        ruta_compara=ruta_local+"\\"+carpeta
    elif ubi == "remota":
        ruta_compara=ruta_remota+"\\"+carpeta

    for carpeta in glob.glob(ruta_compara):
        for file in glob.glob(carpeta + '/*.*'):
            stats = os.stat(file)
            lastmod_date = time.localtime(stats[8])
            date_file_tuple = lastmod_date, file
            lista_fechas.append(date_file_tuple)

        lista_fechas.sort()
        lista_fechas.reverse()

        for file in lista_fechas:
            carpeta, nombre_local = os.path.split(file[1])
            date_local = time.strftime("%Y-%m-%d %H:%M:%S", file[0])
            lista_local.append(nombre_local+ '*' + date_local)
            ####print(lista_local)
            #print("Archivo:::",nombre_local+ '*' + date_local)

    return lista_local


def copiar_reemplazar(carpeta,archivo):
    #print("Estoy en Carpeta:",carpeta, "Pasando archivo:",archivo)
    #logging.info("Consultando Debug4...")
    ruta_r=ruta_remota+"\\"+carpeta+"\\"+archivo
    #print("RUTA:",ruta_r)
    ruta_l=ruta_local+"\\"+carpeta

    try:
        shutil.copy2(ruta_r, ruta_l)
        #print("Ya copie :",ruta_r," a: ",ruta_l)
    except:
        pritn("Error al copiar")




def sincronizar(carpeta):
    pasar_archivos=[]
    pasar_tmp=[]
    local_tmp=[]
    ###print ("")
    ###print("BUSCANDO EN UBICACION LOCAL: ",carpeta)
    archivos_locales=procesar_datos(carpeta, "local")
    ###print("ARCHIVOS LOCALES:")
    ####print(archivos_locales)
    ###print ("")
    
    ###print ("")
    ###print("BUSCANDO EN UBICACION REMOTA: ",carpeta)
    archivos_remotos=procesar_datos(carpeta, "remota")
    ###print("ARCHIVOS REMOTOS:")
    ####print(archivos_remotos)
    ###print ("")
    
    
    ## Primero separa las listas y guarda en "pasar_tmp" archivos DIFERENTES
    for r in archivos_remotos:
        if r not in archivos_locales:
            pasar_tmp.append(r)
    ## Segundo recorrer los archivos Diferentes y buscarlos en archivos remotos y locales para comparar fechas, solo van a quedar(en pasar_tmp)
    ## aquuellos en los que la fecha remota sea MAYOR  a la fecha LOCAL
    #print("Lista temporal de carpeta ",carpeta)
    #print(pasar_tmp)
    
    for archivo in pasar_tmp:
        for r in archivos_remotos:
            ##Separar  nombre y fecha mediante el delimitador * que contiene el string r
            separador = "*"
            remoto = r.split(separador)
            a= archivo.split(separador) ##separo archivo
            if a[0] == remoto[0]:
                for l in archivos_locales:
                    ##Separar  nombre y fecha mediante el delimitador * que contiene el string l
                    local =l.split(separador)
                    if a[0] == local[0]:
                        if remoto[1] > local[1]:
                            pasar_archivos.append(remoto[0])
    
                        break ##Rompo el bucle cuando ya proceso coincidencia archivo == local[0]
                    #break ##Rompo el bucle cuando ya proceso coincidencia archivo == remoto[0]
    
    ## Tercer si existen archivos en pasar_tmp que no existes en archivos_locales, Los sumo a pasar_archivos tambien(antes separlo archivos_locales)
    for l in archivos_locales:
        separador="*"
        local=l.split(separador)
        local_tmp.append(local[0])

    for archivo in pasar_tmp:
        if archivo not in archivos_locales:
            separador="*"
            a=archivo.split(separador)
            pasar_archivos.append(a[0])
    
    
    for archivo in pasar_tmp:
        separador="*"
        a=archivo.split(separador)
        if a[0] not in local_tmp:
            pasar_archivos.append(a[0])
    
    return pasar_archivos



    


################################# MAIN #################################################
ruta_local=ruta_local()
verifico_carpetas(carpetas)
## Consultar Version
##LOCAL
lo=open("version.log","r")
vers_loc=lo.readlines()
lo.close()
#REMOTO
re=open(ruta_remota+"\\version.log","r")
vers_rem=re.readlines()
re.close()

loc =int(vers_loc[0].rstrip())
rem =int(vers_rem[0].rstrip())
###print("Version LOCAL =",loc," - Version REMOTA=",rem)

if rem > loc:
    ###print("HAY ACTUALIZACIONES DISPONIBLES")
    ## AQUI VA TODO EL CODIGO

    t1 = threading.Thread(name="Hilo_Uno:1",target=actualizar)
    t1.daemon = True
    t1.start()
    t1.join()
        
else:
    ###print("TODO ACTUALIZADO.....CONTI NU AR ...")
    subprocess.Popen(ruta_dato)
    '''
    re=open(ruta_remota+"\\version.log","r+")
    rem=loc+'\n'
    re.seek(0)
    re.writelines(rem)
    re.close()
    '''







