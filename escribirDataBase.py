from recolectarDataFrames import analizarCSV as getDFs
from neo4j import GraphDatabase
import time
import pandas
import random

dfH = getDFs()[0]
dfM = getDFs()[1]

graphDataBase = GraphDatabase.driver(uri="bolt://localhost:####",auth=("neo4j","12345"))

sesion = graphDataBase.session()

# Conexion establecida

def realizarComando(tx,comando):
    '''
    Template de Persona:
    CREATE (persona:Persona{nombre:"Liam Kelly",genero:"Hombre",edad:24}) RETURN persona
    '''
    return tx.run(comando)

def realizarConexiones(tx,comando):
    return tx.run(comando)

contador = 1

for i in range(len(dfH)):

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    usuario = dfH.iloc[i]

    nombre = usuario["Nombre"]

    genero = usuario["Yo soy:"]

    edadSinFiltro = usuario["Mi edad se encuentra entre:"]

    edad = 0

    # Modificando la entrada de edad:
    if int(edadSinFiltro[0:2]) <= 17:
        edad = random.randint(15,18)
    elif int(edadSinFiltro[0:2]) <= 24:
        edad = random.randint(18,25)
    elif int(edadSinFiltro[0:2]) <= 33:
        edad = random.randint(25,35)
    else:
        edad = random.randint(35,45)
    redesSociales = usuario["De las siguientes redes sociales, por favor seleccione las que utiliza:"]

    intereses = usuario["Me gusta hablar y ver posts sobre:"]

    salario = usuario["Por favor responde las siguiente preguntas: [¿Mantengo un salario actualmente?]"]

    if salario == "Si":
        pass

    compraEnLinea = usuario["Por favor responde las siguiente preguntas: [¿Compraria cosas en linea?]"]

    recomienda = usuario["Por favor responde las siguiente preguntas: [¿Recomendaria paginas que me gustan?]"]

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    comando = "CREATE (persona:Persona{nombre:'" + nombre + "',genero:'" + genero + "',edad:" + str(edad) + "}) RETURN persona"

    #Aqui se agrega la persona
    realizarComando(sesion,comando)

    #Aqui se agrega si tiene salario:
    if salario == "Si":
        salarioComando = "MATCH(p:Persona),(g:Salario)WHERE p.nombre = '" + nombre + "' AND g.nombre = 'Salario' CREATE (p)-[u:Salario]->(g) RETURN p,g"
        realizarComando(sesion, salarioComando)

    #Aqui se le asigna el genero:
    generoComando = "MATCH(p:Persona),(g:Genero)WHERE p.nombre = '" + nombre + "' AND g.nombre = '" + genero + "' CREATE (p)-[u:Es]->(g) RETURN p,g"
    realizarComando(sesion,generoComando)


    #Aqui se agrega las redes de cada usuario:
    listaRedes = redesSociales.replace(" ","").split(",")
    for red in listaRedes:
        # MATCH (n:Persona) where n.nombre = "Liam Hernandez" MERGE (n) -[u:UTILIZA]->(r:REDSOCIAL{nombre:"Instagram"})
        conexionComando = "MATCH(p:Persona),(r:RedSocial)WHERE p.nombre = '" + nombre + "' AND r.nombre = '" + red + "' CREATE (p)-[u:Utiliza]->(r) RETURN p,r"
        realizarConexiones(sesion,conexionComando)

    # Aqui se agregan los intereses de cada persona:
    listaIntereses = intereses.replace(" ", "").split(",")
    for interes in listaIntereses:
        conexionComando = "MATCH(p:Persona),(r:Interes)WHERE p.nombre = '" + nombre + "' AND r.nombre = '" + interes + "' CREATE (p)-[u:HablaDe]->(r) RETURN p,r"
        realizarConexiones(sesion, conexionComando)



    print(str(contador) + " Registro agregado para: " + nombre)
    contador = contador + 1


for i in range(len(dfM)):

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    usuario = dfM.iloc[i]

    nombre = usuario["Nombre"]

    genero = usuario["Yo soy:"]

    edadSinFiltro = usuario["Mi edad se encuentra entre:"]

    edad = 0

    # Modificando la entrada de edad:
    if int(edadSinFiltro[0:2]) <= 17:
        edad = random.randint(15,18)
    elif int(edadSinFiltro[0:2]) <= 24:
        edad = random.randint(18,25)
    elif int(edadSinFiltro[0:2]) <= 33:
        edad = random.randint(25,35)
    else:
        edad = random.randint(35,45)
    redesSociales = usuario["De las siguientes redes sociales, por favor seleccione las que utiliza:"]

    intereses = usuario["Me gusta hablar y ver posts sobre:"]

    salario = usuario["Por favor responde las siguiente preguntas: [¿Mantengo un salario actualmente?]"]

    compraEnLinea = usuario["Por favor responde las siguiente preguntas: [¿Compraria cosas en linea?]"]

    recomienda = usuario["Por favor responde las siguiente preguntas: [¿Recomendaria paginas que me gustan?]"]

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    comando = "CREATE (persona:Persona{nombre:'" + nombre + "',genero:'" + genero + "',edad:" + str(edad) + "}) RETURN persona"

    #Aqui se agrega la persona
    realizarComando(sesion,comando)

    #Aqui se agrega si tiene salario:
    if salario == "Si":
        salarioComando = "MATCH(p:Persona),(g:Salario)WHERE p.nombre = '" + nombre + "' AND g.nombre = 'Salario' CREATE (p)-[u:Salario]->(g) RETURN p,g"
        realizarComando(sesion, salarioComando)

    #Aqui se le asigna el genero:
    generoComando = "MATCH(p:Persona),(g:Genero)WHERE p.nombre = '" + nombre + "' AND g.nombre = '" + genero + "' CREATE (p)-[u:Es]->(g) RETURN p,g"
    realizarComando(sesion,generoComando)


    #Aqui se agrega las redes de cada usuario:
    listaRedes = redesSociales.replace(" ","").split(",")
    for red in listaRedes:
        # MATCH (n:Persona) where n.nombre = "Liam Hernandez" MERGE (n) -[u:UTILIZA]->(r:REDSOCIAL{nombre:"Instagram"})
        conexionComando = "MATCH(p:Persona),(r:RedSocial)WHERE p.nombre = '" + nombre + "' AND r.nombre = '" + red + "' CREATE (p)-[u:Utiliza]->(r) RETURN p,r"
        realizarConexiones(sesion,conexionComando)

    # Aqui se agregan los intereses de cada persona:
    listaIntereses = intereses.replace(" ", "").split(",")
    for interes in listaIntereses:
        conexionComando = "MATCH(p:Persona),(r:Interes)WHERE p.nombre = '" + nombre + "' AND r.nombre = '" + interes + "' CREATE (p)-[u:HablaDe]->(r) RETURN p,r"
        realizarConexiones(sesion, conexionComando)

    print(str(contador) + " Registro agregado para: " + nombre)
    contador = contador + 1

