from neo4j import GraphDatabase

graphDataBase = GraphDatabase.driver(uri="bolt://localhost:7687",auth=("neo4j","12345"))

sesion = graphDataBase.session()

def realizarComando(tx,comando):
    return tx.run(comando)

listaComandos = ["MATCH (n:Persona)-[r:Utiliza]->() DELETE r",
                 "MATCH (n:Persona)-[r:Es]->() DELETE r",
                 "MATCH (n:Persona)-[r:HablaDe]->() DELETE r",
                 "MATCH (n:Persona)-[r:Salario]->() DELETE r",
                 "MATCH (n:Persona) DELETE n"]
for comando in listaComandos:
    realizarComando(sesion,comando)
    print("Limpiando")
print("Limpio")