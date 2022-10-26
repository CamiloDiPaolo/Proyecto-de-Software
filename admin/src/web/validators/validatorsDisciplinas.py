import re
regexFloat = '[0-9]+\.[0-9]+'
def validate_data(data, operation = "create"):
    print(data)
    # validamos que se ingresen los datos que se tengan que ingresar
    # en una operacion de update puede no haber campos
    if not "nombre" in data and operation == "create":
        return "No ingresaste el nombre"
    if not "horarios" in data and operation == "create": 
        return "No ingresaste el horario"
    if not "instructores" in data and operation == "create": 
        return "No ingresaste a los instructores"
    if not "costo" in data and operation == "create": 
        return "No ingresaste el costo"
    

    # validamos cada campo por separado
    if data["nombre"] == "":
        return "El nombre no puede ser un string vacio"
    if data["horarios"] == "":
        return "El horario no puede ser un string vacio"
    if data["instructores"] == "":
        return "Los instructores no pueden ser un string vacio"
    if data["costo"] == "":
        return "El costo no puede estar vacío"

    # validamos que los tipos sean los correctos
    # for item in data.items():
    if type(data["nombre"]) != str:
        return "El nombre debe ser de tipo string"
    if type(data["horarios"]) != str:
        return "El horario debe ser de tipo string"
    if type(data["instructores"]) != str:
        return "Los instructores deben ser de tipo string"
    if not ((data["costo"].isnumeric()) or (re.search(regexFloat,data["costo"]))):
        return "El costo debe ser de tipo numérico"

    if not data["nombre"].isalpha():
        return "El nombre solo puede contener letras" 


    return False
