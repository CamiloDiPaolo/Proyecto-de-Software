import re

def validate_data(data, operation = "create"):
    print(data)
    # validamos que se ingresen los datos que se tengan que ingresar
    # en una operacion de update puede no haber campos
    if not "email" in data and operation == "create":
        return "No ingresaste el email"
    if not "username" in data and operation == "create": 
        return "No ingresaste el username"
    if not "contraseña" in data and operation == "create": 
        return "No ingresaste la contraseña"
    if not "apellido" in data and operation == "create": 
        return "No ingresaste el apellido"
    if not "nombre" in data and operation == "create":
        return "No ingresaste el nombre"
    
    # validamos que los tipos sean los correctos
    # for item in data.items():
    #     print(type(item[1]))
    if type(data["email"]) != str:
        return "El email debe ser de tipo string"
    if type(data["username"]) != str:
        return "El username debe ser de tipo string"
    if type(data["nombre"]) != str:
        return "El nombre debe ser de tipo string"
    if type(data["apellido"]) != str:
        return "El apellido debe ser de tipo string"
    if type(data["contraseña"]) != str:
        return "La contraseña debe ser de tipo string"
    
    # validamos cada campo por separado
    if(not valid_email(data["email"])):
        return "El email ingresado no es valido"
    if data["username"] == "":
        return "El username no puede ser un string vacio"
    if data["nombre"] == "":
        return "El nombre no puede ser un string vacio"
    if data["apellido"] == "":
        return "El apellido no puede ser un string vacio"
    if data["contraseña"] == "":
        return "La contraseña no puede ser un string vacio"

    return False

def valid_email(email):
   reg = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(reg,email):
      return True
   return False
