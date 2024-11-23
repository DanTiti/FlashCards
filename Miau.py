from tkinter import *
from tkinter import ttk
import random
import sqlite3
from random import shuffle
from tkinter import messagebox
import time
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
import pygame
import customtkinter
from DataBase import DataBase

global Res
global Acierto

Res = []
Acierto = []
archivo = ""
idTabla = 0

def Imagen(Direccion):
    imagen = Image.open(Direccion)
    imagen = imagen.resize((300,270), Image.LANCZOS)
    img = ImageTk.PhotoImage(imagen)
    Lb_Imagen.config(image=img)
    Lb_Imagen.image=img
    VentanaBarajear.geometry("400x420")

def GuardarImagen():
    global archivo
    try:
        archivo = filedialog.askopenfilename(title= "Abrir Imagen", initialdir="C:/", filetypes=[('Imagenes', 'png'), ('Imagenes', '*jpg'), ('Imagenes', '.jpeg')])
        imagen = Image.open(archivo)
        imagen = imagen.resize((200,130), Image.LANCZOS)
        img = ImageTk.PhotoImage(imagen)
        LbPrevisualizacion.config(text="Se ha seleccionado una imagen")
        lbImagen.config(image=img)
        lbImagen.image=img
        Raiz.geometry(("300x650"))
    except:
        LbPrevisualizacion.config(text="No se ha seleccionado una imagen")
        lbImagen.config(image="")
        Raiz.geometry(("300x500"))    

def BarajearLapsos():
    global NuevasCartas
    global i
    i = 0
    NuevasCartas = BarajearCartas()
    Raiz.deiconify()
    SelectorTiempo()

def BarajearLapsosEnCero():
    global NuevasCartas
    global i
    i = 0
    NuevasCartas = BarajearCartas()
    Raiz.deiconify()
    Lapsos(0)

def ActivarContador(Minutos):
    VentanaLapsos.destroy()
    time.sleep(Minutos * 60)
    Lapsos(Minutos)

def DesactivarBotones():
    BtRespuesta.config(state="disabled")
    BtAdelante.config(state="disabled")
    BtAtras.config(state="disabled")

def DesactivarMenu():
    Menu_Opciones.entryconfig(index="Memorizar", state="disabled")
    Menu_Opciones.entryconfig(index="Lapsos", state="disabled")
    Menu_Opciones.entryconfig(index="Preguntas rapidas", state="disabled")

def DesactivasPrincipal():
    BtGuardar.config(state="disabled")
    BtImagen.config(state="disabled")
    EntradaConcepto.configure(state="disabled")
    EntradaRespuesta.configure(state="disabled")
    EntradaComentarios.configure(state="disabled")

def ActivarPrincipal():
    BtGuardar.config(state="active")
    BtImagen.config(state="active")
    EntradaConcepto.configure(state="normal")
    EntradaRespuesta.configure(state="normal")
    EntradaComentarios.configure(state="normal")

def Destruccion():
    BtGuardar.config(state="active")
    BtImagen.config(state="active")
    EntradaConcepto.configure(state="normal")
    EntradaRespuesta.configure(state="normal")
    EntradaComentarios.configure(state="normal")
    Menu_Opciones.entryconfig(index="Memorizar", state="normal")
    Menu_Opciones.entryconfig(index="Lapsos", state="normal")
    Menu_Opciones.entryconfig(index="Preguntas rapidas", state="normal")
    try:
        VentanaTiempo.destroy()
    except:
        pass

def PreguntaBarajear():
    if (messagebox.askyesno("miau", "¿Seguro que quieres cerrar tu sesion de estudios?")):
        Destruccion()
        VentanaBarajear.destroy()
        Raiz.deiconify()
    else:
        pass

def PreguntaLapsos():
    if (messagebox.askyesno("miau", "¿Seguro que quieres cerrar tu sesion de estudios?")):
        Destruccion()
        VentanaLapsos.destroy()
        Raiz.deiconify()
    else:
        pass
    
def Anterior():
    global Contador

    if(Contador > 0):
        Contador -= 1
        print(Contador)
        LbPregunta.config(text=Cartas[Contador][1])
        LbRespuesta.config(text="")
        Lb_Imagen.config(image="")
        VentanaBarajear.geometry("400x200")
    else:
        Contador = 0

def Respuesta():
    global Contador
    
    LbRespuesta.config(text=Cartas[Contador][2])

def Siguiente():
    global Contador

    try:
        Contador += 1
        print(Contador)
        LbPregunta.config(text=Cartas[Contador][1])
        LbRespuesta.config(text="")
        Lb_Imagen.config(image="")
        VentanaBarajear.geometry("400x200")
    except:
        DesactivarBotones()
        messagebox.showinfo("miaumiaumiau", "Haz terminado todas tus cartas")
        ActivarMenu()
        ActivarPrincipal()
        VentanaBarajear.destroy()

def BarajearCartas():
    Conexion = DataBase()
    Datos = Conexion.ObtenerFlashCards(idTabla)
    print(Datos)
    #print(shuffle(Datos))
    Conexion.Cerrar()

    return Datos

def ActivarMenu():
    Menu_Opciones.entryconfig(index="Memorizar", state="normal")
    Menu_Opciones.entryconfig(index="Lapsos", state="normal")
    Menu_Opciones.entryconfig(index="Preguntas rapidas", state="normal")

def GuardarCarta(idTabla):
    global archivo
    global LbPrevisualizacion
    Conexion = DataBase()
    concepto = EntradaConcepto.get()
    respuesta = EntradaRespuesta.get()
    comentarios = EntradaComentarios.get("1.0", END)
    Conexion.CrearFlashCard(idTabla, concepto, respuesta, comentarios, archivo)
    Conexion.Cerrar()
    print("FlashCard Guardada")
    EntradaRespuesta.delete(0,END)
    EntradaConcepto.delete(0,END)
    EntradaComentarios.delete("1.0", END)
    archivo = ""
    lbImagen.config(image= "")
    LbPrevisualizacion.config(text="No se ha seleccionado una imagen")
    Raiz.geometry("300x500")
    ActivarMenu()

def Barajear():
    global LbPregunta
    global LbRespuesta
    global Contador
    global Cartas
    global VentanaBarajear
    global BtAdelante
    global BtAtras
    global BtRespuesta
    global Lb_Imagen

    Contador = 0

    DesactivarMenu()
    DesactivasPrincipal()

    Raiz.deiconify()
    VentanaBarajear = Toplevel()
    VentanaBarajear.geometry("400x200")
    VentanaBarajear.resizable(FALSE,FALSE)

    Cartas = BarajearCartas()

    #------------------frame principal---------------------------------
    FramePrincipal = Frame(VentanaBarajear)
    FramePrincipal.pack()

    #-------------------Label de la pregunta---------------------------
    LbPregunta = Label(FramePrincipal, text=Cartas[Contador][1], font=("BowersShadow", 18), width=17)
    LbPregunta.grid(column=0, row=0, columnspan=3, pady=5)

    #--------------------Label respuesta-------------------------------
    LbRespuesta = Label(FramePrincipal, text="", fg= "green", font=("Consolas", 14))
    LbRespuesta.grid(column=0, row=1, columnspan=3, pady=(5, 15))
    
    #--------------------Botones----------------------------------------
    BtImagen = Button(FramePrincipal, text="Mostrar Imagen", command=lambda:Imagen(Cartas[Contador][4]))
    BtImagen.grid(column=0, row=2, columnspan=3, sticky=NSEW)

    BtAtras = Button(FramePrincipal, text="Anterior", command=lambda:Anterior())
    BtAtras.grid(column=0, row=3, sticky=NSEW)

    BtRespuesta = Button(FramePrincipal, text="Respuesta", command=lambda:Respuesta())
    BtRespuesta.grid(column=1, row=3, sticky=NSEW)

    BtAdelante = Button(FramePrincipal, text="Siguiente", command=lambda:Siguiente())
    BtAdelante.grid(column=2, row=3, sticky=NSEW)

    Lb_Imagen = Label(FramePrincipal, image="")
    Lb_Imagen.grid(column=0, row=4, columnspan=3, sticky=NSEW)

    VentanaBarajear.protocol("WM_DELETE_WINDOW", lambda:PreguntaBarajear())

#Ventana en la que se muestra todos los datos sobre cuales salieron bien y cuales no
def VentanaAciertos(Respuestas, Aciertos):
    global Res
    global Acierto

    print(Respuestas)
    print(Aciertos)
    Raiz.deiconify()
    VentanaAciertos = Toplevel()
    VentanaAciertos.geometry("410x212")
    VentanaAciertos.resizable(FALSE, FALSE)

    FramePrincipal = Frame(VentanaAciertos)
    FramePrincipal.pack(fill=BOTH, expand=1)

    MiCanvas = Canvas(FramePrincipal, background="white")
    MiCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    MiScrollbar = Scrollbar(MiCanvas, orient=VERTICAL, command=MiCanvas.yview)
    MiScrollbar.pack(side=RIGHT, fill=Y)

    MiCanvas.configure(yscrollcommand=MiScrollbar.set)
    MiCanvas.bind('<Configure>', lambda e: MiCanvas.configure(scrollregion=MiCanvas.bbox("all")))

    SegundoFrame = Frame(MiCanvas, background="#EAEEF1")

    MiCanvas.create_window((0,0), window=SegundoFrame, anchor="nw", width=390)

    for i, elemento in enumerate(NuevasCartas, 0):
        
        if(Aciertos[i] == "Correcto"):
            C = "#CBD8B0"
        else:
            C = "#EEB3BC"

        FrameBigDaddy = Frame(SegundoFrame)
        FrameBigDaddy.pack(fill=BOTH, pady=(0,30))

        FrameHijo = Frame(FrameBigDaddy, background=C)
        FrameHijo.pack(fill=BOTH)

        Label(FrameHijo, text=Acierto[i], background=C, anchor=E).grid(column=0, row=0)

        FrameContenedor = Frame(FrameBigDaddy, background="#E1E2E9")
        FrameContenedor.pack(fill=BOTH)

        Label(FrameContenedor, text="Concepto: " + NuevasCartas[i][1].upper(), background="#E1E2E9", font=("BowersShadow", 10)).grid(column=0, row=i)
        Label(FrameContenedor, text="Respuesta: " + NuevasCartas[i][2], background="#E1E2E9").grid(column=0, row=i+1)
        Label(FrameContenedor, text="Tu respuesta: " + Res[i], background="#E1E2E9").grid(column=0, row=i+2)

    Acierto = []
    Res = []
    
def VerificarRespuesta(Respuesta, Minutos):

    global i

    print("i:", i)
    print("Respuesta:", Respuesta)
    print("Pregunta:", NuevasCartas[i][2])
    Pregunta = NuevasCartas[i][2].lower()
    if(Respuesta == Pregunta.lower()):
        print("Respuesta Correcta")
        Acierto.append("Correcto")
        Res.append("✓" + Respuesta)
        Entrada_Respuesta.delete(0,END)
        if(i < len(NuevasCartas) - 1):
            i += 1
            print(i)
            ActivarContador(Minutos)
        else:
            VentanaLapsos.destroy()
            ActivarMenu()
            ActivarPrincipal()
            VentanaAciertos(Res, Acierto)
    else:
        print("Respuesta Incorrecta")
        Acierto.append("Incorrecto")
        Res.append("✘" + Respuesta)
        Entrada_Respuesta.delete(0,END)
        if(i < len(NuevasCartas) - 1):
            i += 1
            ActivarContador(Minutos)
        else:
            VentanaLapsos.destroy()
            ActivarMenu()
            ActivarPrincipal()
            VentanaAciertos(Res, Acierto)

def Opcion(Op):
    if Op == "1 Minuto":
        Minutos = 1
    elif Op == "5 Minutos":
        Minutos = 5
    elif Op == "10 Minutos":
        Minutos = 10
    elif Op == "15 Minutos":
        Minutos = 15
    elif Op == "20 Minutos":
        Minutos = 20
    elif Op == "25 Minutos":
        Minutos = 25
    elif Op == "30 Minutos":
        Minutos = 30

    return Lapsos(Minutos)

def Lapsos(Minutos):
    global VentanaTiempo
    global NuevasCartas
    global VentanaLapsos
    global Entrada_Respuesta
    global LbPregunta

    print("Pregunta:",NuevasCartas[i][1])
    print("Respuesta:", NuevasCartas[i][2])

    try:
        VentanaTiempo.destroy()
    except:
        pass
    DesactivarMenu()
    DesactivasPrincipal()
    VentanaLapsos = Toplevel()
    VentanaLapsos.geometry("410x200")
    VentanaLapsos.config(background="#E5DDEA")
    VentanaLapsos.resizable(FALSE, FALSE)

    VentanaLapsos.columnconfigure(0, weight=1)
    VentanaLapsos.columnconfigure(1, weight=1)
    VentanaLapsos.columnconfigure(2, weight=1)

    LbPregunta = Label(VentanaLapsos, text=NuevasCartas[i][1].upper(), background="#E5DDEA", font=("BowersShadow", 18))
    LbPregunta.grid(column=0, row=0, columnspan=3, pady=20)

    Entrada_Respuesta = Entry(VentanaLapsos, width=25, background="#EBE9EC", borderwidth=5, font=("Consolas", 10), justify=CENTER)
    Entrada_Respuesta.grid(column=0, row=1, columnspan=2, ipady=10)

    BtProbar = Button(VentanaLapsos, text="Probar", borderwidth=6, background="#FFF7D2",command=lambda:VerificarRespuesta(Entrada_Respuesta.get().lower(), Minutos))
    BtProbar.grid(column=2, row=1, ipadx=10, ipady=10)
    VentanaLapsos.protocol("WM_DELETE_WINDOW", lambda:PreguntaLapsos())
    Raiz.iconify()

def SelectorTiempo():
    global VentanaTiempo
    messagebox.showinfo("Info", "Para continuar, selecciona la cantidad de tiempo en que deseas que aparezca una carta de otra.")
    Raiz.deiconify
    DesactivarMenu()
    DesactivasPrincipal()
    VentanaTiempo = Toplevel()
    VentanaTiempo.geometry("300x140")
    VentanaTiempo.resizable(FALSE,FALSE)
    FrameTiempo = Frame(VentanaTiempo)
    FrameTiempo.pack()
    LbTxt = Label(FrameTiempo, text="Seleccione el lapso de tiempo entre cada carta.")
    LbTxt.grid(column=1, row=0, columnspan=3, pady=10)
    ComboTxt = StringVar()
    Combo = ttk.Combobox(FrameTiempo, values=["1 Minuto", "5 Minutos", "10 Minutos", "15 Minutos", "20 Minutos", "25 Minutos", "30 Minutos"], state="readonly", textvariable=ComboTxt, width=25)
    Combo.grid(column=0, row=1, pady=10, padx=5, columnspan=2, sticky=NSEW)
    Combo.set("1 Minuto")

    Btn = Button(FrameTiempo, text="Aceptar", width=5, command=lambda:Opcion(ComboTxt.get()))
    Btn.grid(column=2, row=1, sticky=NSEW)

    VentanaTiempo.protocol("WM_DELETE_WINDOW", lambda:Destruccion())

def Charlar():
    Raiz.deiconify()
    VentanaCharlar = Toplevel()
    


def VentanaPrincipal():

    global EntradaConcepto
    global EntradaRespuesta
    global EntradaComentarios
    global Menu_Opciones
    global lbImagen
    global FrameImagen
    global LbPrevisualizacion
    global Raiz
    global BtImagen
    global BtGuardar

    Raiz = Tk()
    pygame.mixer.init()
    
    FramePrincipal = Frame(Raiz)
    FramePrincipal.pack()
    #----------------Menu------------------------------

    Barra_Menu = Menu()
    Menu_Opciones = Menu(Barra_Menu, tearoff=False)
    Barra_Menu.add_cascade(menu=Menu_Opciones, label="Opciones")
    Menu_Opciones.add_command(label="Memorizar", command=lambda:Barajear(), state="disabled")
    Menu_Opciones.add_command(label="Lapsos", command=lambda:BarajearLapsos(), state="disabled")
    Menu_Opciones.add_command(label="Preguntas rapidas", command=lambda:BarajearLapsosEnCero(), state="disabled")
    Menu_Opciones.add_command(label="Charlar", command=lambda:Charlar(), state="disabled")

    #--------------Entrada del concepto---------------
    LbConcepto = Label(FramePrincipal, text="Concepto o pregunta")
    LbConcepto.grid(column=0, row=0, columnspan=3)

    EntradaConcepto = customtkinter.CTkEntry(FramePrincipal, width=200)
    EntradaConcepto.grid(column=0, row=1, columnspan=3, pady=10, ipady= 5)

    #--------------Entrada definicion o significado-----------

    LbRespuesta = Label(FramePrincipal, text="Respuesta")
    LbRespuesta.grid(column=0, row=2, columnspan=3)

    EntradaRespuesta = customtkinter.CTkEntry(FramePrincipal, width=200)
    EntradaRespuesta.grid(column=0, row=3, columnspan=3, pady=10, ipady=5)

    #--------------Entrada de comentarios-------------------

    LbComentario = Label(FramePrincipal, text="Comentarios")
    LbComentario.grid(column=0, row=4, columnspan=3)

    EntradaComentarios = customtkinter.CTkTextbox(FramePrincipal, height=150, width=200, border_width=2)
    EntradaComentarios.grid(column=0, row=5, columnspan=3, pady=10)

    #---------------Introduccion de imagenes-----------------

    LbImagen = Label(FramePrincipal, text="Introducir Imagen: ")
    LbImagen.grid(column=0, row=6, pady=10)

    BtImagen = Button(FramePrincipal, text="Seleccionar", width=10, command=lambda:GuardarImagen())
    BtImagen.grid(column=1, row=6, columnspan=2, pady=10)

    #---------------Boton de guardar carta--------------------

    BtGuardar = Button(FramePrincipal, width=28, text="Guardar", command=lambda: GuardarCarta(idTabla))
    BtGuardar.grid(column=0, row=7, columnspan=3, pady=10)

    #--------------previsualizacion de imagen-----------------------

    LbPrevisualizacion = Label(FramePrincipal, text="No se ha seleccionado una imagen")
    LbPrevisualizacion.grid(column=0, row=8, columnspan=3, pady=10)

    FrameImagen = Frame(FramePrincipal, borderwidth=10, width=200, height=150)
    FrameImagen.grid(column=0, row=9, columnspan=3, pady=10)    

    lbImagen = Label(FrameImagen, image="")
    lbImagen.grid(column=0, row=0)

    Raiz.config(menu=Barra_Menu)
    Raiz.geometry("300x500")
    Raiz.resizable(FALSE, FALSE)
    Raiz.title("StudyStar")
    

    try:
        Conexion = DataBase
        Datos = Conexion.ObtenerFlashCards(idTabla)
        if(len(Datos) != 0):
            ActivarMenu()
        Conexion.Cerrar()
    except:
        print("Error al obtener los datos")

    Raiz.mainloop()

def ventanaCarpetas():
    conexion = DataBase()
    data = conexion.ObtenerCarpetas()
    conexion.Cerrar()

    def CrearCarpeta(nombre):
        conexion = DataBase()
        conexion.CrearCarpeta(nombre)
        data = conexion.ObtenerCarpetas()
        print(data)
        conexion.Cerrar()

    def NombreCarpeta():
        win = Toplevel()
        win.geometry("300x200")

        labelInfo = Label(win, text="Añade un nombre a la carpeta")
        labelInfo.pack()
        entryNombre = customtkinter.CTkEntry(win, corner_radius=25, width=200)
        entryNombre.pack()
        btnConfirmar = customtkinter.CTkButton(win, corner_radius=25, text="Crear", command=lambda: (CrearCarpeta(entryNombre.get()), win.destroy()))
        btnConfirmar.pack()

    def on_carpeta_click(carpeta_id, carpeta_nombre):
        global idTabla
        print(f"Carpeta seleccionada: {carpeta_nombre} (ID: {carpeta_id})")
        idTabla = carpeta_id
        main.destroy()
        VentanaPrincipal()

    main = Tk()
    main.geometry("550x500")

    frametop = Frame(main)
    frametop.pack(fill="both", expand=True)
    framebot = Frame(main, bg="gray")
    framebot.pack(side="bottom", fill="x")
    framebot.columnconfigure(0, weight=1)
    framebot.columnconfigure(1, weight=1)
    framebot.columnconfigure(2, weight=1)

    #configuracion del frame inferior----------------------------------
    
    btnCrear = customtkinter.CTkButton(framebot, text="Crear carpeta", corner_radius=25, command=lambda: NombreCarpeta())
    btnCrear.grid(column=1, row=0, padx= 10, pady=(10,15))

    btnImportar = customtkinter.CTkButton(framebot, text="importar carpeta", corner_radius=25)
    btnImportar.grid(column=0, row=0)

    btnEliminar = customtkinter.CTkButton(framebot, text="Eliminar carpeta", corner_radius=25)
    btnEliminar.grid(column=2, row=0)

    #configuracion del frame superior-------------------------------------

    canvas = Canvas(frametop, background="white")
    canvas.pack(side=LEFT, fill="both", expand=True)  # Hace que el canvas llene todo el frametop.

    MiScrollbar = Scrollbar(frametop, orient=VERTICAL, command=canvas.yview)  # Scrollbar también dentro del frametop.
    MiScrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=MiScrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    SegundoFrame = Frame(canvas, background="#EAEEF1")

    canvas.create_window((0, 0), window=SegundoFrame, anchor="center", width=550)

    for carpeta in data:
        carpeta_id, carpeta_nombre = carpeta
        frameContenedor = Frame(SegundoFrame, bg="red", padx=5, pady=5)
        frameContenedor.pack(fill="x", pady=5)

        labelName = Label(
            frameContenedor, 
            text=carpeta_nombre, 
            bg="red", 
            fg="white", 
            font=("Arial", 12, "bold")
        )

        labelName.pack()

        frameContenedor.bind("<Button-1>", lambda e, cid=carpeta_id, cname=carpeta_nombre: on_carpeta_click(cid, cname))
        labelName.bind("<Button-1>", lambda e, cid=carpeta_id, cname=carpeta_nombre: on_carpeta_click(cid, cname))


    main.mainloop()

ventanaCarpetas()