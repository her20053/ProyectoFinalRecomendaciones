from neo4j import GraphDatabase
import pandas as pd
from datetime import datetime as fecha
from email.message import EmailMessage
import smtplib
import matplotlib.pyplot as plt
import io
"""
cc2003email20053
clave: CC2003email20053!
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# graphDataBase = GraphDatabase.driver(uri="bolt://localhost:7687",auth=("neo4j","12345"))
#
# def obtenerPersona(grapho):
#     nombresInstagram = grapho.run("MATCH (p:Persona) WHERE p.edad > 30 return p.nombre")
#     lista = [nodo["p.nombre"] for nodo in nombresInstagram]
#     print(lista)
#     # ['Jose', 'Lucia', 'Mario']
#     nodosInstagram = grapho.run("MATCH(n:Persona) WHERE n.red_social = 'Instagram' return n")
#     lista = [nodo["n"] for nodo in nodosInstagram]
#     for n in lista:
#         # tipo <class 'neo4j.graph.Node'>
#         #< Node #id = 0 #labels = frozenset({'Persona'}) #properties = {'nombre': 'Jose', 'red_social': 'Instagram'} >
#         print(n["nombre"])
#
# session = graphDataBase.session()
# session.read_transaction(obtenerPersona)

def enviar_email(nombre,opcion):
    correo = "cc2003email20053"
    clave  = "CC2003email20053!"
    msg    = EmailMessage()
    msg['Subject'] = "Inicio de sesion realizado"
    msg['From']    = correo
    msg['To']      = "her20053@uvg.edu.gt"
    msg.set_content("El usuario con nombre " + nombre + " ha iniciado sesion y ha elegido la opcion " + opcion)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(correo,clave)
        smtp.send_message(msg)
    print("Correo enviado")
    pass

def obtener_lista_nodos(grapho,comando):

    lista_nombres = []

    edades_filtradas = grapho.run(comando)

    lista_nodos = [nodo["p"] for nodo in edades_filtradas]

    for nodo in lista_nodos:

        lista_nombres.append(nodo["nombre"])

    return lista_nombres

def obtener_redes_sociales(grapho,comando):

    lista_redes_sociales = []

    redes_filtradas = grapho.run(comando)

    # MATCH(p: Persona{nombre:"Mia Gutierrez"}),(r:RedSocial)WHERE(p) - [:Utiliza]-(r) return r

    lista_nodos = [nodo["r"] for nodo in redes_filtradas]

    for nodo in lista_nodos:

        lista_redes_sociales.append(nodo["nombre"])

    return lista_redes_sociales

def asociar_emprendimiento(nombre_usuario,enviar_correo,correo_electronico):

    """
    Aqui se establece la conexion con el servidor de neo4j
    que retrae la data segun las caracteristicas del empredimiento
    :param nombre_usuario:
    :return:
    """

    DataFrame = pd.read_csv("emprendimientos_registrados.csv")
    DataFrame_Usuario = DataFrame[DataFrame["usuario_encargado"] == nombre_usuario]

    graphDataBase = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "12345"))

    session = graphDataBase.session()

    for registro_indice in range(len(DataFrame_Usuario)):

        nom_emprendimiento = DataFrame_Usuario.iloc[registro_indice]["nombre_emprendimiento"]

        int_emprendimiento = DataFrame_Usuario.iloc[registro_indice]["interes_principal"]

        edd_emprendimiento = DataFrame_Usuario.iloc[registro_indice]["edad_apartir_de"]

        gen_emprendimiento = DataFrame_Usuario.iloc[registro_indice]["genero_espefico"]

        prd_emprendimiento = DataFrame_Usuario.iloc[registro_indice]["producto"]

        lista_usuarios = []

        if gen_emprendimiento == "Ambos":
            comando = "MATCH (p:Persona),(i:Interes{nombre:'" + int_emprendimiento + "'}) WHERE p.edad >= " + str(edd_emprendimiento) + "AND (p)-[:HablaDe]-(i) AND p.genero = 'Hombre' return p"
            for nombre in session.read_transaction(obtener_lista_nodos, comando):
                lista_usuarios.append(nombre)
            comando = "MATCH (p:Persona),(i:Interes{nombre:'" + int_emprendimiento + "'}) WHERE p.edad >= " + str(edd_emprendimiento) + "AND (p)-[:HablaDe]-(i) AND p.genero = 'Mujer' return p"
            for nombre in session.read_transaction(obtener_lista_nodos, comando):
                lista_usuarios.append(nombre)
        else:
            comando = "MATCH (p:Persona),(i:Interes{nombre:'" + int_emprendimiento + "'}) WHERE p.edad >= " + str(edd_emprendimiento) + "AND (p)-[:HablaDe]-(i) AND p.genero = '" + gen_emprendimiento + "' return p"
            for nombre in session.read_transaction(obtener_lista_nodos, comando):
                lista_usuarios.append(nombre)

        """
        Ya tenemos los nombres de las personas, hora tenemos que ver que redes sociales son las que utilizan
        """

        diccionario_redes = {"TikTok":0,
                             "Twitter":0,
                             "Facebook":0,
                             "Instagram":0,
                             "Snapchat":0,
                             "LinkedIn":0}

        for usuario in lista_usuarios:

            # MATCH(p: Persona{nombre:"Mia Gutierrez"}),(r:RedSocial)WHERE(p) - [:Utiliza]-(r) return r

            comando = "MATCH(p: Persona{nombre:'"+usuario+"'}),(r:RedSocial) WHERE (p)-[:Utiliza]-(r) return r"

            for red in session.read_transaction(obtener_redes_sociales,comando):
                diccionario_redes[red] = diccionario_redes[red] + 1

        # print(diccionario_redes)

        lista_redes = []
        conteo_redes = []

        for key in diccionario_redes:
            lista_redes.append(key)
            conteo_redes.append(diccionario_redes[key])

        listaBarras = plt.bar(lista_redes,conteo_redes)
        listaBarras[0].set_color("k")
        listaBarras[1].set_color("c")
        listaBarras[2].set_color("b")
        listaBarras[3].set_color("r")
        listaBarras[4].set_color("y")
        listaBarras[5].set_color("c")
        plt.ylabel("Cantidad de apariciones en recoleccion de datos")
        plt.xlabel("Redes sociales")
        plt.show()

        if enviar_correo:

            # Mandar correo

            img_format = 'png'

            f = io.BytesIO()

            plt.savefig(f, format=img_format)

            f.seek(0)

            correo = "cc2003email20053"
            clave = "CC2003email20053!"

            img_data = f.read()

            msg = EmailMessage()
            msg['Subject'] = "Estadisticas realizadas para " + nom_emprendimiento
            msg['From'] = correo
            msg['To'] = correo_electronico
            formato_imprimir = []
            for i in range(len(lista_usuarios)):
                formato_imprimir.append(lista_usuarios[i].split(" ")[0])
            mensaje = "Para su emprendimiento se han obtenido los siguientes datos:\nSe han buscado personas que les interese hablar de su tema, donde la edad sea igual o mayor a la especificada por su negocio\nLas personas que se encontraron fueron: \n" + str(formato_imprimir) + "\nCon las redes sociales: "+str(diccionario_redes)+"."
            msg.set_content(mensaje)
            msg.add_attachment(img_data, maintype = 'image', subtype = img_format)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(correo, clave)
                smtp.send_message(msg)
            print("Correo enviado para " + nom_emprendimiento)

        else:

            print("------------------------------------------------------------------------------------------------")

            print(bcolors.OKBLUE + "Para su emprendimiento '" + nom_emprendimiento + "' se han obtenido los siguientes datos:\n" + bcolors.ENDC)
            # "MATCH (p:Persona),(i:Interes{nombre:'" + int_emprendimiento + "'}) WHERE p.edad >= " + str(edd_emprendimiento) + "AND (p)-[:HablaDe]-(i) AND p.genero = '" + gen_emprendimiento + "' return p"
            print("Se han buscado personas que les interese hablar de "+bcolors.WARNING+int_emprendimiento+bcolors.ENDC+", donde la edad sea igual o mayor a "+bcolors.WARNING+str(edd_emprendimiento)+bcolors.ENDC+ " y el genero al que se dirige es a " +bcolors.WARNING+gen_emprendimiento+bcolors.ENDC)
            print()
            print("Por lo que se obtuvo la siguiente lista de usuarios: (Por motivos de seguridad se han censurado sus apellidos)")
            formato_imprimir = []
            for i in range(len(lista_usuarios)):
                formato_imprimir.append(lista_usuarios[i].split(" ")[0])
            print(bcolors.OKGREEN +str(formato_imprimir)+ bcolors.ENDC)
            print()
            print("Se han obtenido las "+ bcolors.WARNING + "redes sociales" + bcolors.ENDC +" que utiliza cada usuario y el conteo ha llegado de la siguiente manera:")
            print(diccionario_redes)
            print()
            print("En la grafica de barras se puede ilustrar de una manera mas facil la comparacion de cantidad de apariciones contra la red social.\n")
            primerpuesto = ""
            segundopuesto = ""
            contador = 0

            x = dict(sorted(diccionario_redes.items(), key=lambda x:x[0], reverse=True))
            print(x)
            ordenado = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
            print(ordenado)
            # k = dict(sorted(s.items(), key=lambda x: x[0], reverse=True))
            # for clave in diccionario_copia_redes:
            #     if diccionario_redes[clave] > contador:
            #         contador = diccionario_redes[clave]
            #         segundopuesto = primerpuesto
            #         primerpuesto = clave

            print("Viendo la grafica de barras, el programa le puede recomendar que utilice " + bcolors.UNDERLINE + bcolors.OKCYAN + str(list(ordenado.keys())[-1]) + bcolors.ENDC + " como su principal objetivo de ventas.")
            print("En segundo puesto se ubica " + bcolors.OKBLUE + str(list(ordenado.keys())[-2])  + bcolors.ENDC + ", por lo que le recomendamos tomar esta red social como fuente de crecimiento/marketing, no de ventas.")

            print("------------------------------------------------------------------------------------------------\n\n")
        input("\n\nSiguiente registro\n\n")


def crear_nuevo_emprendimiento(usuario):
    print(bcolors.HEADER + "\nCreando nuevo emprendimiento, porfavor complete lo siguientes datos: \n" +bcolors.ENDC)
    nom_emprendimiento = input("Ingrese el nombre de su empredimiento: ")
    fec_emprendimiento = fecha.now().strftime("%Y-%m-%d")
    print("\nPorfavor ingrese el interes principal para su emprendimiento:\n")
    lista_intereses = ["Cine(Seriesopeliculas)",
                       "Deportes",
                       "Politica",
                       "Estudios",
                       "Religion",
                       "Comida",
                       "Musica",
                       "Otros"]
    for interese_indice in range(len(lista_intereses)):
        print(bcolors.BOLD + str(interese_indice + 1) + bcolors.ENDC +" "+ lista_intereses[interese_indice])
    print()
    int_emprendimiento = input(bcolors.WARNING + "Interes: " + bcolors.ENDC)
    while (int_emprendimiento not in lista_intereses):
        print(bcolors.FAIL + "Interes no reconocido o no disponible, intenta de nuevo.." + bcolors.ENDC)
        int_emprendimiento = input(bcolors.WARNING + "Interes: " + bcolors.ENDC)
    print()
    print("Porfavor ingrese la edad a partir de la cual desearia captar personas: ")
    edad_correcta = False
    edd_emprendimiento = 0
    while(not edad_correcta):
        try:
            edd_emprendimiento = int(input(bcolors.WARNING + "Edad requerida: " + bcolors.ENDC))
            edad_correcta = True
        except:
            print(bcolors.FAIL + "La edad tiene que ser un numero, intenta de nuevo.." + bcolors.ENDC)
    print()
    print("Ingrese a que genero desea dirigirse:")
    print()
    lista_opciones_genero = ["Hombre","Mujer","Ambos"]
    for genero_indice in range(len(lista_opciones_genero)):
        print(bcolors.BOLD + str(genero_indice + 1) + bcolors.ENDC +" "+ lista_opciones_genero[genero_indice])
    print()
    gen_emprendimiento = input(bcolors.WARNING + "Genero: " + bcolors.ENDC)
    while (gen_emprendimiento not in lista_opciones_genero):
        print(bcolors.FAIL + "Genero no reconocido en la lista, intenta de nuevo.." + bcolors.ENDC)
        gen_emprendimiento = input(bcolors.WARNING + "Genero: " + bcolors.ENDC)
    print()
    print("Por ultimo, porfavor describa brevemente su producto:")
    dsc_emprendimiento = input("Descripcion de producto: ")

    df = pd.read_csv("emprendimientos_registrados.csv")
    diccionario_emprendimiento = {"usuario_encargado":usuario,
                                  "nombre_emprendimiento":nom_emprendimiento,
                                  "fecha_creacion":str(fec_emprendimiento),
                                  "interes_principal":int_emprendimiento,
                                  "edad_apartir_de":edd_emprendimiento,
                                  "genero_espefico":gen_emprendimiento,
                                  "producto":dsc_emprendimiento}
    df_modificado = df.append(diccionario_emprendimiento,ignore_index=True)
    df_modificado.to_csv("emprendimientos_registrados.csv", index=False)
    print(bcolors.OKGREEN + "\nEmprendimiento creado con exito!\n" + bcolors.ENDC)
def menu_ingreso_usuario(nombre_usuario,correo_electronico):
    print(bcolors.WARNING + "Se ha iniciado sesion como " + nombre_usuario + " ("+correo_electronico+")\n" +bcolors.ENDC)
    continuar_menu = True
    while(continuar_menu):
        print("Listando emprendimientos registrados:")
        emprendimientos_dataframe = pd.read_csv("emprendimientos_registrados.csv")
        df_filtrado_usuario = emprendimientos_dataframe[emprendimientos_dataframe["usuario_encargado"] == nombre_usuario]
        if len(df_filtrado_usuario) == 0:
            print("Aun no tienes ningun emprendimiento registrado.")
        else:
            print(df_filtrado_usuario.to_string(index=False))
        print()
        print("[ 1 ] Crear nuevo emprendimiento")
        if len(df_filtrado_usuario) == 0:
            print("[ 2 ] Asociar un  emprendimiento   {Empredimiento previamente creado requerido}")
        else:
            print("[ 2 ] Asociar un  emprendimiento")
        if len(df_filtrado_usuario) == 0:
            print("[ 3 ] Enviar estadisticas a correo {Empredimiento previamente creado requerido}")
        else:
            print("[ 3 ] Enviar estadisticas a correo")
        print("[ 4 ] Cerrar sesion\n")

        respuesta = input(bcolors.WARNING + "Deseo: " + bcolors.ENDC)
        lista_opciones = []
        if len(df_filtrado_usuario) == 0:
            lista_opciones = ["1","4"]
        else:
            lista_opciones = ["1","4","3","2"]
        while (respuesta not in lista_opciones):
            print(bcolors.FAIL + "Opcion incorrecta o no disponible, intenta de nuevo.." + bcolors.ENDC)
            respuesta = input(bcolors.WARNING + "Deseo: " + bcolors.ENDC)
        if respuesta == "1":
            crear_nuevo_emprendimiento(nombre_usuario)
        elif respuesta == "2":
            asociar_emprendimiento(nombre_usuario,False,correo_electronico)
        elif respuesta == "3":
            asociar_emprendimiento(nombre_usuario,True,correo_electronico)
        else:
            print(bcolors.OKBLUE+"\nCerrando sesion"+bcolors.ENDC)
            continuar_menu = False
            pass
def menu_principal_usuario():
    print(bcolors.HEADER + "\nIniciando sesion, porfavor complete lo siguientes datos: \n" +bcolors.ENDC)
    DataFrame_usuarios = pd.read_csv("registros_usuario.csv")
    usuarios_existentes = []
    lista_correos = []
    claves_afiliadas = {}
    conexion_correos_nombre = {}
    conexiones_nombre_correo = {}
    for i in range(len(DataFrame_usuarios)):
        usuarios_existentes.append(DataFrame_usuarios.iloc[i]["nombre_usuario"])
        usuarios_existentes.append(DataFrame_usuarios.iloc[i]["correo_usuario"])
        lista_correos.append(DataFrame_usuarios.iloc[i]["correo_usuario"])
        conexion_correos_nombre[DataFrame_usuarios.iloc[i]["correo_usuario"]] = DataFrame_usuarios.iloc[i]["nombre_usuario"]
        conexiones_nombre_correo[DataFrame_usuarios.iloc[i]["nombre_usuario"]] = DataFrame_usuarios.iloc[i]["correo_usuario"]
        claves_afiliadas[DataFrame_usuarios.iloc[i]["nombre_usuario"]] = DataFrame_usuarios.iloc[i]["clave_usuario"]
        claves_afiliadas[DataFrame_usuarios.iloc[i]["correo_usuario"]] = DataFrame_usuarios.iloc[i]["clave_usuario"]
    nombre_usuario = input("Nombre de usuario o correo electronico: ")
    if nombre_usuario in usuarios_existentes:
        clave = input("Clave: ")
        if claves_afiliadas[nombre_usuario] == clave:
            print(bcolors.OKCYAN+"\nSesion iniciada!\n" +bcolors.ENDC)
            if nombre_usuario in lista_correos:
                menu_ingreso_usuario(conexion_correos_nombre[nombre_usuario],nombre_usuario)
            else:
                menu_ingreso_usuario(nombre_usuario,conexiones_nombre_correo[nombre_usuario])
        else:
            print(bcolors.FAIL + "\n ! Clave no correspondiente, porfavor vuelva a intentar !" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "\n ! Usuario o correo no existente, porfavor registrese o vuelva a intentar !" + bcolors.ENDC)
def menu_principal_registro():
    DataFrame_usuarios = pd.read_csv("registros_usuario.csv")
    usuarios_existentes = []
    for i in range(len(DataFrame_usuarios)):
        usuarios_existentes.append(DataFrame_usuarios.iloc[i]["nombre_usuario"])
        usuarios_existentes.append(DataFrame_usuarios.iloc[i]["correo_usuario"])
    print(bcolors.WARNING + "\nCreando un nuevo usuario\nPorfavor complete la siguiente informacion requerida:\n" + bcolors.ENDC)
    diccionario_datos = {"Nombre de usuario : ":"",
                         "Clave de ingreso  : ":"",
                         "Correo electronico: ":""}
    nombre = input("Nombre de usuario : ")
    if nombre in usuarios_existentes:
        print(bcolors.FAIL + "\n ! Usuario ya existente, porfavor inicie sesion o elija otro nombre !" + bcolors.ENDC)
    else:
        diccionario_datos["Nombre de usuario : "] = nombre
        clave = input("Clave de ingreso  : ")
        diccionario_datos["Clave de ingreso  : "] = clave
        correo = input("Correo electronico: ")
        if correo in usuarios_existentes:
            print(bcolors.FAIL + "\n ! Correo ya existente, porfavor inicie sesion o elija otro correo !" + bcolors.ENDC)
        else:
            diccionario_datos["Correo electronico: "] = correo
            print(bcolors.OKGREEN + "\nUsuario creado con exito! Porfavor inicie sesion para continuar.")
            nuevoDF = DataFrame_usuarios.append({"nombre_usuario":nombre,"clave_usuario":clave,"correo_usuario":correo},ignore_index=True)
            nuevoDF.to_csv("registros_usuario.csv",index = False)
    pass
def obtener_informacion_inicio():
    print(bcolors.WARNING+"\nBienvenido usuario"+bcolors.ENDC)
    print("\n[ 1 ]   Iniciar sesion ")
    print(  "[ 2 ]   Registrarme \n")
    respuesta = input(bcolors.WARNING+"Deseo: "+bcolors.ENDC)
    while(respuesta not in ["1","2"]):
        print(bcolors.FAIL + "Fallo al intentar reconocer opcion, intenta de nuevo.."+bcolors.ENDC)
        respuesta = input(bcolors.WARNING+"Deseo: "+bcolors.ENDC)
    if respuesta == "1":
        menu_principal_usuario()
    else:
        menu_principal_registro()

# Aqui inicia el programa:
while(True):
    obtener_informacion_inicio()

