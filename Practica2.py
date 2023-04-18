import tkinter as tk
from tkinter import messagebox
import os
from pysnmp.hlapi import *
import time
import rrdtool

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import *
from createRRD import rrdtool_create
from graphRRD import generar_imagenes


class PracticaUnoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Practica 1")

        # Crear el menú escogible
        self.menu = tk.Menu(master)
        self.menu.add_command(label="Agregar dispositivo",
                              command=self.agregar_dispositivo)
        self.menu.add_command(
            label="Cambiar información del dispositivo", command=self.cambiar_informacion)
        self.menu.add_command(label="Eliminar dispositivo",
                              command=self.eliminar_dispositivo)
        self.menu.add_command(label="Generar reporte",
                              command=self.generar_reporte)
        master.config(menu=self.menu)

    def agregar_dispositivo(self):
        # Crear la ventana para agregar dispositivo
        self.agregar_dispositivo_window = tk.Toplevel(self.master)
        self.agregar_dispositivo_window.title("Agregar dispositivo")

        # Crear los campos de entrada para la información del dispositivo
        tk.Label(self.agregar_dispositivo_window,
                 text="Nombre del host o dirección IP:").grid(row=0, column=0)
        self.host_entry = tk.Entry(self.agregar_dispositivo_window)
        self.host_entry.grid(row=0, column=1)

        tk.Label(self.agregar_dispositivo_window,
                 text="Versión SNMP:").grid(row=1, column=0)
        self.snmp_entry = tk.Entry(self.agregar_dispositivo_window)
        self.snmp_entry.grid(row=1, column=1)

        tk.Label(self.agregar_dispositivo_window,
                 text="Nombre de la comunidad:").grid(row=2, column=0)
        self.comunidad_entry = tk.Entry(self.agregar_dispositivo_window)
        self.comunidad_entry.grid(row=2, column=1)

        tk.Label(self.agregar_dispositivo_window,
                 text="Puerto:").grid(row=3, column=0)
        self.puerto_entry = tk.Entry(self.agregar_dispositivo_window)
        self.puerto_entry.grid(row=3, column=1)

        # Crear el botón para agregar el dispositivo
        agregar_button = tk.Button(
            self.agregar_dispositivo_window, text="Agregar", command=self.guardar_dispositivo)
        agregar_button.grid(row=4, column=1)

    def guardar_dispositivo(self):
        # Obtener la información ingresada por el usuario
        host = self.host_entry.get()
        snmp = self.snmp_entry.get()
        comunidad = self.comunidad_entry.get()
        puerto = self.puerto_entry.get()

        # Guardar la información en un archivo de texto
        with open("dispositivos.txt", "a") as f:
            f.write(f"{host}, {snmp}, {comunidad}, {puerto}\n")

        # Cerrar la ventana de agregar dispositivo
        self.agregar_dispositivo_window.destroy()

    def cambiar_informacion(self):
        # Leer los dispositivos del archivo de texto
        dispositivos = []
        with open("dispositivos.txt", "r") as f:
            for line in f:
                datos = line.strip().split(", ")
                dispositivos.append(datos)

        # Crear la ventana para cambiar la información del dispositivo
        self.cambiar_informacion_window = tk.Toplevel(self.master)
        self.cambiar_informacion_window.title(
            "Cambiar información del dispositivo")

        # Crear el campo de lista para seleccionar el dispositivo
        tk.Label(self.cambiar_informacion_window,
                 text="Seleccionar dispositivo:").grid(row=0, column=0)
        self.dispositivo_var = tk.StringVar(self.cambiar_informacion_window)
        # Seleccionar el primer dispositivo por defecto
        self.dispositivo_var.set(dispositivos[0][0])
        self.dispositivo_option = tk.OptionMenu(self.cambiar_informacion_window, self.dispositivo_var, *[
                                                d[0] for d in dispositivos])
        self.dispositivo_option.grid(row=0, column=1)

        # Crear los campos de entrada para la información del dispositivo
        tk.Label(self.cambiar_informacion_window,
                 text="Nombre del host o dirección IP:").grid(row=1, column=0)
        self.host_entry = tk.Entry(self.cambiar_informacion_window)
        self.host_entry.grid(row=1, column=1)

        tk.Label(self.cambiar_informacion_window,
                 text="Versión SNMP:").grid(row=2, column=0)
        self.snmp_entry = tk.Entry(self.cambiar_informacion_window)
        self.snmp_entry.grid(row=2, column=1)

        tk.Label(self.cambiar_informacion_window,
                 text="Nombre de la comunidad:").grid(row=3, column=0)
        self.comunidad_entry = tk.Entry(self.cambiar_informacion_window)
        self.comunidad_entry.grid(row=3, column=1)

        tk.Label(self.cambiar_informacion_window,
                 text="Puerto:").grid(row=4, column=0)
        self.puerto_entry = tk.Entry(self.cambiar_informacion_window)
        self.puerto_entry.grid(row=4, column=1)

        # Mostrar la información del dispositivo seleccionado por defecto

        # Crear el botón para guardar los cambios
        tk.Button(self.cambiar_informacion_window, text="Guardar",
                  command=self.guardar_cambios).grid(row=5, column=1)

    def guardar_cambios(self):
        # Leer los dispositivos del archivo de texto
        dispositivos = []
        with open("dispositivos.txt", "r") as f:
            for line in f:
                datos = line.strip().split(", ")
                dispositivos.append(datos)

        # Obtener la información del dispositivo seleccionado
        dispositivo_actual = self.dispositivo_var.get()
        for i, d in enumerate(dispositivos):
            if d[0] == dispositivo_actual:
                # Actualizar la información del dispositivo en la lista de dispositivos
                dispositivos[i][0] = self.host_entry.get()
                dispositivos[i][1] = self.snmp_entry.get()
                dispositivos[i][2] = self.comunidad_entry.get()
                dispositivos[i][3] = self.puerto_entry.get()

                # Escribir los dispositivos actualizados en el archivo de texto
                with open("dispositivos.txt", "w") as f:
                    for d in dispositivos:
                        f.write(", ".join(d) + "\n")

                messagebox.showinfo(
                    "Cambios guardados", "La información del dispositivo ha sido actualizada.")

                # Cerrar la ventana de cambiar información del dispositivo
                self.cambiar_informacion_window.destroy()

    def eliminar_dispositivo(self):
        # Crear la ventana para eliminar dispositivo
        self.eliminar_dispositivo_window = tk.Toplevel(self.master)
        self.eliminar_dispositivo_window.title("Eliminar dispositivo")

        # Crear el campo de entrada para el nombre del host o dirección IP
        tk.Label(self.eliminar_dispositivo_window,
                 text="Nombre del host o dirección IP:").grid(row=0, column=0)
        self.host_eliminar_entry = tk.Entry(self.eliminar_dispositivo_window)
        self.host_eliminar_entry.grid(row=0, column=1)

        # Crear el botón para eliminar el dispositivo
        eliminar_button = tk.Button(
            self.eliminar_dispositivo_window, text="Eliminar", command=self.confirmar_eliminar)
        eliminar_button.grid(row=1, column=1)

    def confirmar_eliminar(self):
        # Obtener el nombre del host o dirección IP ingresado por el usuario
        host_eliminar = self.host_eliminar_entry.get()

        # Buscar el dispositivo en el archivo de texto
        encontrado = False
        with open("dispositivos.txt", "r") as f:
            lines = f.readlines()
        with open("dispositivos.txt", "w") as f:
            for line in lines:
                if not line.startswith(host_eliminar):
                    f.write(line)
                else:
                    encontrado = True

        if encontrado:
            # Eliminar los archivos generados para el dispositivo
            for filename in os.listdir("."):
                if filename.startswith(host_eliminar):
                    os.remove(filename)

            # Mostrar mensaje al usuario indicando que se eliminó el dispositivo
            messagebox.showinfo("Dispositivo eliminado",
                                f"Se eliminó el dispositivo con dirección IP o nombre de host: {host_eliminar}")
        else:
            # Mostrar mensaje al usuario indicando que no se encontró el dispositivo
            messagebox.showerror("Dispositivo no encontrado",
                                 f"No se encontró el dispositivo con dirección IP o nombre de host: {host_eliminar}")

        # Cerrar la ventana de eliminar dispositivo
        self.eliminar_dispositivo_window.destroy()

    def generar_reporte(self):
        # Obtener la lista de dispositivos del archivo de texto
        dispositivos = []
        with open("dispositivos.txt", "r") as f:
            for line in f:
                dispositivo = line.strip().split(", ")
                dispositivos.append(dispositivo)

        # Crear la ventana para generar reporte
        self.generar_reporte_window = tk.Toplevel(self.master)
        self.generar_reporte_window.title("Generar reporte")

        # Crear el menú escogible para seleccionar el dispositivo
        tk.Label(self.generar_reporte_window, text="Seleccionar dispositivo:").grid(
            row=0, column=0)
        self.dispositivos_menu = tk.StringVar(self.generar_reporte_window)
        self.dispositivos_menu.set(dispositivos[0][0])
        dispositivos_options = [dispositivo[0] for dispositivo in dispositivos]
        tk.OptionMenu(self.generar_reporte_window, self.dispositivos_menu,
                      *dispositivos_options).grid(row=0, column=1)

        # Crear el botón para generar el reporte
        generar_button = tk.Button(
            self.generar_reporte_window, text="Generar", command=self.guardar_reporte)
        generar_button.grid(row=1, column=1)

    def consultaSNMP(self, comunidad, ip, oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(comunidad, mpModel=0),
                   UdpTransportTarget((ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))))

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                  errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                varB = (' = '.join([x.prettyPrint() for x in varBind]))
                resultado = varB.split("=")[1]
        return resultado

    def guardar_reporte(self):
        # Obtener el dispositivo seleccionado
        dispositivo_seleccionado = self.dispositivos_menu.get()

        # Buscar el dispositivo en el archivo de texto
        encontrado = False
        with open("dispositivos.txt", "r") as f:
            for line in f:
                dispositivo = line.strip().split(", ")
                if dispositivo[0] == dispositivo_seleccionado:
                    encontrado = True
                    host, snmp, comunidad, puerto = dispositivo
                    break

        if encontrado:
            rrdtool_create(host)
            # Obtener la información del dispositivo usando SNMP
            consulta = self.consultaSNMP(comunidad, host, "1.3.6.1.2.1.1.1.0")
            so = self.consultaSNMP(comunidad, host, "1.3.6.1.2.1.1.1.0")
            ubicacion = self.consultaSNMP(comunidad, host, "1.3.6.1.2.1.1.4.0")
            contacto = self.consultaSNMP(comunidad, host, "1.3.6.1.2.1.1.6.0")

            messagebox.showinfo("Informacion de Reporte",
                                "espera 10 min a que se genere el archivo PDF")
            paquetes_unicast = 0
            paquetes_protocolo_ip = 0
            mensajes_ICMP = 0
            segmentos_recibidos = 0
            datagramas_UDP = 0

            start_time = time.time()
            while True:
                paquetes_unicast = int(self.consultaSNMP(comunidad, host,
                                                         '1.3.6.1.2.1.2.2.1.11.3'))
                paquetes_protocolo_ip = int(self.consultaSNMP(comunidad, host,
                                                              '1.3.6.1.2.1.4.3.0'))
                mensajes_ICMP = int(self.consultaSNMP(comunidad, host,
                                                      '1.3.6.1.2.1.5.1.0'))
                segmentos_recibidos = int(self.consultaSNMP(comunidad, host,
                                                            '1.3.6.1.2.1.6.10.0'))
                datagramas_UDP = int(self.consultaSNMP(comunidad, host,
                                                       '1.3.6.1.2.1.7.1.0'))

                valor = "N:" + str(paquetes_unicast) + ':' + str(paquetes_protocolo_ip) + ':' + str(mensajes_ICMP) + ':' + \
                    str(segmentos_recibidos) + ':' + str(datagramas_UDP)

                print(valor)
                db_name = host +'.rdd'
                rrdtool.update(db_name, valor)

                if (time.time() - start_time) >= 600:  # 10 minutes
                    break

                time.sleep(1)
            

            generar_imagenes(host)
            db_name = host +'.rdd'


            interfaces = []
            # Obtener el número de interfaces
            num_interfaces = int(self.consultaSNMP(
                comunidad, host, "1.3.6.1.2.1.2.1.0"))
            for i in range(1, num_interfaces + 1):
                # Obtener la descripción y estado de la interfaz
                descr_bytes = self.consultaSNMP(
                    comunidad, host, "1.3.6.1.2.1.2.2.1.2."+str(i))[3:-2]
                # descr = codecs.decode(descr_bytes,'hex').decode('ascii')
                try:
                    descr = bytes.fromhex(descr_bytes).decode('utf-8')
                except Exception:
                    descr = 'No se pudo decodificar'

                estado = self.consultaSNMP(
                    comunidad, host, f"1.3.6.1.2.1.2.2.1.8.{i}")
                estados = {
                    1: "up",
                    2: "down",
                    3: "testing",
                    4: "unknown",
                    5: "dormant",
                    6: "notPresent",
                    7: "lowerLayerDown"
                }
                print(estado)
                if int(estado) in estados:
                    estado = estados[int(estado)]
                else:
                    print(f"Estado desconocido: {estado}")
                    estado = "Estado desconocido"
                # Agregar la información a la lista de interfaces
                interfaces.append((descr, estado))
                print(interfaces)

            filename = f"{host}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            # Crear la lista de elementos que irán en el PDF
            elementos = []
            # Agregar el título del reporte
            elementos.append(Paragraph(f"Reporte del dispositivo {host}"))
            elementos.append(Paragraph("Carlos Rojas Diaz Barriga Practica 2"))

            elementos.append(Spacer(1, 12))
            # Agregar la información general del dispositivo
            elementos.append(Paragraph(f"dispositivo: {so}"))
            elementos.append(Paragraph(f"Ubicación: {ubicacion}"))
            elementos.append(Paragraph(f"Contacto: {contacto}"))
            elementos.append(Spacer(1, 12))
            # Verificar si el sistema operativo es Linux o Windows
            print(so)
            if "linux" in so.lower():
                imagen_path = "linux.png"
            elif "windows" in so.lower():
                imagen_path = "windows.png"

            # Cargar la imagen
            imagen = Image(imagen_path, width=50, height=50)

            # Agregar la imagen al documento
            elementos.append(imagen)

            elementos.append(Spacer(1, 12))
            # Agregar la tabla de interfaces
            data = [["Descripción", "Estado"]]
            for interfaz in interfaces:
                data.append([interfaz[0], interfaz[1]])
            table = Table(data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black)
            ]))
            elementos.append(table)
            elementos.append(Spacer(1, 12))
            elementos.append(Image(db_name+"_paquetes.png"))
            elementos.append(Image(db_name+"_paquetes_ip.png"))
            elementos.append(Image(db_name+"_mensajes.png"))
            elementos.append(Image(db_name+"_segmentos.png"))
            elementos.append(Image(db_name+"_datagramas.png"))
            # Generar el PDF
            doc.build(elementos)
        else:
            messagebox.showerror("Dispositivo no encontrado",
                                 f"No se encontró el dispositivo con dirección IP o nombre de host: {host}")


root = tk.Tk()
practica_uno_gui = PracticaUnoGUI(root)
root.mainloop()
