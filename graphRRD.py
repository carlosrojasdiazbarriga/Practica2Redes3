import rrdtool
import time

def generar_imagenes(nombre_bd):
    tiempo_actual = int(time.time())
    tiempo_inicial = tiempo_actual - 1200
    nombre_bd = nombre_bd +'.rdd'
    
    paquetes_path = f"{nombre_bd}_paquetes.png"
    ret = rrdtool.graph(paquetes_path,
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_actual),
                        "--vertical-label=Bytes/s",
                        "--title=paquetes unicast de un agente \n Usando SNMP y RRDtools",
                        f"DEF:paquetesunicast={nombre_bd}:packunicast:AVERAGE",
                        "CDEF:escalaIn=paquetesunicast,8,*",
                        "LINE1:escalaIn#FF0000:paquetes de unicast")

    paquetes_ip_path = f"{nombre_bd}_paquetes_ip.png"
    ret = rrdtool.graph(paquetes_ip_path,
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_actual),
                        "--vertical-label=Bytes/s",
                        "--title=paquetes protocolo ip de un agente \n Usando SNMP y RRDtools",
                        f"DEF:paquetesprotocoloip={nombre_bd}:packproip:AVERAGE",
                        "CDEF:escalaIn=paquetesprotocoloip,8,*",
                        "LINE1:escalaIn#FF0000:paquetes de protocolo ip")

    mensajes_path = f"{nombre_bd}_mensajes.png"
    ret = rrdtool.graph(mensajes_path,
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_actual),
                        "--vertical-label=Bytes/s",
                        "--title=mensajes icmp enviados \n Usando SNMP y RRDtools",
                        f"DEF:mensajesICMP={nombre_bd}:menICMP:AVERAGE",
                        "CDEF:escalaIn=mensajesICMP,8,*",
                        "LINE1:escalaIn#FF0000:mensajes icmp")

    segmentos_path = f"{nombre_bd}_segmentos.png"
    ret = rrdtool.graph(segmentos_path,
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_actual),
                        "--vertical-label=Bytes/s",
                        "--title=segmentos de un agente \n Usando SNMP y RRDtools",
                        f"DEF:segmentos={nombre_bd}:segmentos:AVERAGE",
                        "CDEF:escalaIn=segmentos,8,*",
                        "LINE1:escalaIn#FF0000:segmentos enviados")

    datagramas_path = f"{nombre_bd}_datagramas.png"
    ret = rrdtool.graph(datagramas_path,
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_actual),
                        "--vertical-label=Bytes/s",
                        "--title=datagramas por UDP de un agente \n Usando SNMP y RRDtools",
                        f"DEF:datagramasudp={nombre_bd}:dataUDP:AVERAGE",
                        "CDEF:escalaIn=datagramasudp,8,*",
                        "LINE1:escalaIn#FF0000:segmentos enviados")
