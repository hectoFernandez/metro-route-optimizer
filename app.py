import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import tkinter as tk
from tkinter import ttk , Toplevel
from tkinter import font
from tkcalendar import Calendar
from datetime import datetime, date, time
from PIL import Image, ImageTk  
import customtkinter
from logic.codigo_aestrella import* 
from data.elementos_apoyo_interfaz import *

# Inicializamos la variable global
ventana= None

#Funciones auxiliares-------------------
# Función que nos permite  el calendario y seleccionar una fecha
def open_calendar():
    global ventana

    def select_date():
        selected_date = cal.selection_get()
        entry_day_widget.config(state="normal")  #Cambiamos a modo normal para poder introducir la fecha 
        entry_day_widget.delete(0, tk.END)
        entry_day_widget.insert(0, selected_date.strftime("%Y-%m-%d"))
        entry_day_widget.config(state="readonly") #Volvemos a modo leer para que no se pueda cambiar la fecha escribiendo directameatne
        ventana.destroy()


    # Verificamos si ya existe una ventana de calendario abierta
    if ventana and ventana.winfo_exists():
        return  # Asi evitamos  abrir múltiples ventanas

    # Creamos una ventana emergente para el calendario
    ventana = tk.Toplevel(app)
    ventana.title("Seleccionar Fecha")
    ventana.geometry("300x250")
    ventana.resizable(False, False)

    # Obtenemos la fecha actual
    today = datetime.today()

    # Creamos el calendario
    cal = Calendar(ventana, selectmode="day", year=today.year, month=today.month, day=today.day)
    cal.pack(pady=10)

    # Creamos un boton para confirmar la fecha seleccionada
    select_btn = ttk.Button(ventana, text="Seleccionar", command=select_date)
    select_btn.pack(pady=5)

    # Bloquemaos la ventana principal hasta que se cierre la ventana del calendario
    ventana.transient(app)  # Hacemos que la ventana emergente sea hija de la principal
    ventana.grab_set()
    app.wait_window(ventana)  
    


#Las operaciones que realizaran cuando hagos click en el boton 
def when_button_click():
    from_st = entry_from.get() #Estacion de origen
    to_st = entry_to.get() #Estacion de fin 
    day = entry_day.get() #Dia de viaje
    hour = hour_var.get() #Hora de viaje
    minute = minute_var.get() #Minuto d e viaje 
    date_day = day.split("-") #Separamos la fecha para tenerla en formato fehca
    final_date = date(int(date_day[0]), int(date_day[1]), int(date_day[2])) #Pasamos a foramto fecha
    final_hour = time(int(hour), int(minute.zfill(2))) #Pasamos a formato time


    try:
        #Calculammos el dia de la semana
        week_day = calcular_fecha(final_date)
        #Avergiamos el camino
        way_to_st: List = calcular_camino(from_st, to_st)

        if len(way_to_st) == 1: #Si la longitud es una tenemos la misma estacion 
            result_label.config(text='Ambas estaciones introducidas son la misma')
        else:
            time_to_st= calcular_tiempo_camino(final_hour, week_day, way_to_st)     
            transfer = None

            if time_to_st is None: #El horario de viaje esta fuera del servicio 
                week_day = None
                way_to_st = None
                time_to_st = None
                result_label.config(text="No hay trenes a estas horas,\ntiene que esperar a que comience la jornada de trenes")
            else:
                time_to_st = round(time_to_st)
                hour_at_st = hora_llegada(final_hour, time_to_st)
                transfer = numero_transbordos(way_to_st)
            #Mostramos el resultado

            result_text = (
                f"🚇 TRAYECTO 🚇\n\n📍 {from_st} -> {to_st}\n\n"
                f"🗓️ {final_date} - {final_hour.strftime('%H:%M')}\n\n"
                f"⏱️ Duración del trayecto: {time_to_st} min\n\n⌚️ Hora de llegada -> {hour_at_st.strftime('%H:%M')}\n\n"
                f"🔄 Transbordos: {len(transfer)}\n\n🚏 Paradas: {len(way_to_st)}\n\n"
                # f"🗺️ Ruta:\n\n{' - '.join(map(str, Camino))}"
            )

            result_label.config(text=result_text)
            popup_route_and_transfer(f"Trayecto:{way_to_st}\n\nTransbordos:{transfer}")
        #Coloreamos los botones de las estaciones
        light_floating_button(app, station_positions, way_to_st, new_color="yellow")

    except Exception as e:
        print(e)

def fill_field(value):
        #Rellenamos   'Origen' o 'Destino' con el valor dado. Sobrescribir empezando desde el origen.
        if entry_from.get() == "Estación de Origen":
            # Si el campo de origen está vacío,  se rellena
            entry_from.set(value)
        elif entry_to.get() == "Estación de Destino":
            # Si el campo de destino está vacío, se rellena
            entry_to.set(value)
        else:
            # Si ambos campos están completos, se sobrescribe comenzando desde el origen
            entry_from.set(value)
            entry_to.set("Estación de Destino")  

#Funcion que crea un botón flotante con texto, posición x e y, y color de fondo.
def create_floating_button(self, text, x, y, bg_color="white"):
    customtkinter.CTkButton(
        self,
        width=14,  # Tamaño pequeño
        height=14,
        corner_radius=15,  # Hacerlo circular
        fg_color="white",  # Color del botón
        bg_color=bg_color,  # Usamos el colon de fondo especificado
        hover_color="yellow",  # Color al pasar el ratón
        text="",  
        command=lambda: fill_field(text)  
    ).place(x=x, y=y)

#Funcion que nos permite coloear los botones  para indicar el camino
def light_floating_button(self, station_positions, Camino, new_color="yellow"):
    for station, data in station_positions.items():
        x, y = data["coords"]  # Obtener las coordenadas de cada estación
        fg_color = new_color if station in Camino else "white"  # Si está en el camino, usamos el color amarillo
        bg_color = data["bg_color"] #Con esto mantenemos el color de fondo de la estacion

        customtkinter.CTkButton(
            self,
            width=14,
            height=14,
            corner_radius=15,
            fg_color=fg_color,
            bg_color=bg_color,
            hover_color="yellow",
            text="",
            command=lambda station=station: fill_field(station)
        ).place(x=x, y=y)


def popup_route_and_transfer(text):
    #Creamos el popu
    popup = tk.Toplevel(app)
    popup.title("Información del trayecto") #Añadimos titulo
    popup.geometry("500x400")  
    popup.transient(app) 
    popup.grab_set()  #Asi obligamos a que el usuario cierre el popup antes de seguir
    label = tk.Label(
        popup,
        text="Detalles del trayecto:",
        font=("Arial", 12),
        justify="center"
    )
    label.pack(pady=20)
    #Cuadro donde escribiremos tanto la ruta como los tranbordos
    text_box = tk.Text(popup, wrap="word", font=("Arial", 12), height=10, width=60)
    text_box.pack(padx=20, pady=20)
    text_box.insert("1.0", text)
    text_box.config(state="disabled")  # Solo puede leerse y no modficarse 
    # Para cerrar el boton 
    close_button = ttk.Button(popup, text="Cerrar", command=popup.destroy)
    close_button.pack(pady=10)
#--------------------





# Creamos la ventana principal
app = tk.Tk()
app.title("Subte - Metro Buenos Aires")

# Dimensiones de la ventana
window_width = 900
window_height = 850

# Obtenemos dimensiones de la pantalla
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculamos  posición centrada
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# Configuramos  la geometría centrada
app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
app.minsize(window_width, window_height)
app.maxsize(window_width, window_height)

#app.geometry("900x850")  # Tamaño de la ventana
app.minsize(900, 850)
app.maxsize(900,850)

#Establecemos el icono
icon_path = os.path.join(BASE_DIR, 'assets', 'images', 'logo_subte.png')
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)

app.iconphoto(False, icon_photo)

# Ponemos el titulo a la interfaz 
title_font = font.Font(family="Arial", size=72, weight="bold", slant="italic")
title_label = tk.Label(app, text="SUBTE", font=title_font, anchor="w")
title_label.pack(padx=40, pady=10, anchor="w")  # Alinear el título al margen izquierdo

# Cargarmos una imagen de un tren para  colocarla debajo del titulo
image_path = os.path.join(BASE_DIR, 'assets', 'images', 'train_no_background_(1).png')
img = Image.open(image_path)
img = img.resize([450,40]) # Ajustamos tamaño de la imagen 
photo = ImageTk.PhotoImage(img)
#Mostramos la imagen 
image_label = tk.Label(app, image=photo)
image_label.pack( pady=5, anchor="w")  


#Escrbimos un texto informativo para el usuario
exp_font = font.Font(family="Arial", size=11, weight="bold", slant="italic")
exp_label = tk.Label(
    app,
    text="Puede seleccionar las estaciones tanto en el desplegable\ncomo en el mapa interactivo",
    font=exp_font,  # Tipo y tamaño de letra
    anchor="w",
    justify="center" 
)
exp_label.pack(padx=20,pady=10, anchor="w")


frame = ttk.Frame(app, padding=20)
frame.pack(padx=40, anchor="w")  

output_frame = ttk.Frame(app, padding=20)
output_frame.pack(padx=10, pady=10, anchor="w")  

# Establecemos el desplegable de la estación de origen
entry_from = ttk.Combobox(frame, values=estaciones, width=30, state="readonly")
entry_from.pack(pady=5, anchor="w")  
entry_from.set("Estación de Origen")  # Texto antes de elegir la estacion deseada 

# Establecemos el desplegable de la estación de destino 
entry_to = ttk.Combobox(frame, values=estaciones, width=30, state="readonly")
entry_to.pack(pady=5, anchor="w")
entry_to.set("Estación de Destino")   # Texto antes de elegir la estacion deseada 

#Creamos la fila de seleccion de calendario
frame_day = ttk.Frame(frame)
frame_day.pack(pady=5, anchor="w")

# Configurar fecha por defecto
today = datetime.today()  # Obtener la fecha de hoy
entry_day = tk.StringVar()
entry_day.set(today.strftime("%Y-%m-%d"))  # Establecer la fecha actual

# Crear campo de entrada para la fecha
entry_day_widget = ttk.Entry(frame_day, width=20, textvariable=entry_day, state="readonly")
entry_day_widget.pack(side=tk.LEFT, padx=5)

# Botón para abrir el calendario
calendar_btn = ttk.Button(frame_day, text=" 🗓️ ", command=open_calendar)  # Llamamos a la función calendario
calendar_btn.pack(side=tk.LEFT)


# Creamos la cuarta fila donde se podra seleccionar las horas
hour_var = tk.StringVar()
minute_var = tk.StringVar()

#Establecemos las posibles horas y minutos
hours = [f"{h:02}" for h in range(24)]
minutes = [f"{m:02}" for m in range(0, 60, 1)]

#ELegimos la hora actual y lo ponemos como valor predetermiando
current_hour = today.strftime("%H")
current_minute = int(today.strftime("%M"))

#Creamos el apartado de las horas y minutos 
frame_time = ttk.Frame(frame)
frame_time.pack(pady=10, anchor="w")

hour_menu = ttk.Combobox(frame_time, textvariable=hour_var, values=hours, width=5, state="readonly")
hour_menu.set(current_hour)  # Seleccionas la  hora actual por defecto
hour_menu.pack(side=tk.LEFT, padx=5)

minute_menu = ttk.Combobox(frame_time, textvariable=minute_var, values=minutes, width=5, state="readonly")
minute_menu.set(f"{current_minute:02}")  # Seleccionamos los  minutos actuales por defecto
minute_menu.pack(side=tk.LEFT, padx=5)

# Etiqueta para mostrar el resultado
result_label = tk.Label(output_frame, text="", font=("Arial", 12), justify="left", anchor="w")
result_label.pack(fill=tk.BOTH, expand=True)

# Botón para buscar ruta
button = ttk.Button(frame, text="Buscar ruta", command=when_button_click)
button.pack(padx=185, pady=20, anchor="w")

bg_path = os.path.join(BASE_DIR, 'assets', 'images', 'fondo.jpg')
bg = Image.open(bg_path)
bg = bg.resize((450,775))
background = ImageTk.PhotoImage(bg)

# Etiqueta para mostrar la imagen
bg_label = tk.Label(app, image=background)
bg_label.place(relx=1.0, y=1, anchor="ne")  # Posiciona en la esquina superior derecha


# A continuacion llamamos a la funcion anterior para crear los botones
for station, data in station_positions.items():
    x, y = data["coords"]  # Accedemos a la posicion de cada estacion
    bg_color = data["bg_color"]  # Estraemos su color de fonfo
    create_floating_button(app, station, x, y, bg_color) #Creamos los botones


# Iniciamos el bucle de la aplicación
app.mainloop()
