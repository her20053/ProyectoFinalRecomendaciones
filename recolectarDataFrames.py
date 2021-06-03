import pandas as modulo_pd
import random
"""
Funcion encargada de analizar el csv y retornar una lista solamente con los datos analizados
utilizando dataFrames. Crearemos DataFrames especificos de hombres y mujeres y les asignare
un nombre para que cada usuario sea unico.
"""
listaNombresH = []
nombreCompletoH = []
listaNombresM = []
nombreCompletoM = []
listaApellidos = []
with open("NombresMujer.txt") as nombres:
    for nombre in nombres:
        listaNombresM.append(nombre.replace("\n", ""))
with open("NombresHombres.txt") as nombres:
    for nombre in nombres:
        listaNombresH.append(nombre.replace("\n", ""))
with open("Apellidos.txt") as apellidos:
    for apellido in apellidos:
        listaApellidos.append(apellido.replace("\n",""))
for nombre in listaNombresH:
    apellido = listaApellidos.pop(random.randint(0,len(listaApellidos) - 1))
    nombreCompletoH.append(nombre + " " + apellido)
for nombre in listaNombresM:
    apellido = listaApellidos.pop(random.randint(0,len(listaApellidos) - 1))
    nombreCompletoM.append(nombre + " " + apellido)

def analizarCSV():

    dataFrame = modulo_pd.read_csv("Encuesta.csv")
    dataFrameH = dataFrame[dataFrame["Yo soy:"] == "Hombre"]
    dataFrameM = dataFrame[dataFrame["Yo soy:"] == "Mujer"]

    listaAcomodadaH = nombreCompletoH[0:len(dataFrameH)]
    dataFrameH.insert(0,"Nombre",listaAcomodadaH)

    listaAcomodadaM = nombreCompletoM[0:len(dataFrameM)]
    dataFrameM.insert(0,"Nombre",listaAcomodadaM)

    # contador = 1
    # for i in range(len(dataFrameH)):
    #     print(str(contador) + " " +dataFrameH.iloc[i]["Nombre"])
    #     contador = contador + 1
    # for i in range(len(dataFrameM)):
    #     print(str(contador) + " " +dataFrameM.iloc[i]["Nombre"])
    #     contador = contador + 1
    # for i in range(len(dataFrameM)):
    #     print(dataFrameM.iloc[i])
    # print(len(dataFrameH))
    # print(len(dataFrameM))

    return [dataFrameH,dataFrameM]
