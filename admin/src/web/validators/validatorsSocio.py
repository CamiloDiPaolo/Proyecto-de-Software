import re

def validate_data(data,operation ="create"):
    if not "apellido" in data and operation == "create": 
        return "No ingresaste el apellido"
    if not "nombre" in data and operation == "create":
        return "No ingresaste el nombre"
    if not "genero" in data and operation == "create":
        return "No ingreso genero"
    if not "estado" in data and operation == "create":
        return "No ingreso estado"
    if not "direccion" in data and operation == "create":
        return "No ingresaste la direccion"
    
    if (operation != "UPDATE"):
        if ((data["tipo_documento"] != "DNI") &  (data["tipo_documento"] != "RUC") & (data["tipo_documento"] != "CARNET_EXT") & (data["tipo_documento"] != "PASAPORTE") & (data["tipo_documento"] != "P.NAC")):
            return "El tipo de documento debe ser una de las opciones indicadas"
        
        if not "tipo_documento" in data and operation == "create":
            return "No se ingreso tipo de documento"
        
        if not "nro_documento" in data and operation == "create":
            return "No ingresaste el numero de documento"
        
        if data["nro_documento"] == "":
            return "El numero de documento no puede estar vacio"
        if (data["tipo_documento"] == ""):
            
            return "El tipo de documento no puede estar vacio"
        if not(data["nro_documento"].isnumeric()):
            return "El numero de documento debe ser un Numero"  
    
    
    
    if ((data["genero"] != "Masculino") & (data["genero"] != "Femenino") & (data["genero"] != "Otro")):
        return "El genero debe ser uno de los indicados"
    
    if ((data["estado"] != "Activo") & (data["estado"] != "Inactivo")):
        return "El estado debe ser uno de los indicados"
    
    if (data["telefono"]) != '':
        if not (type(data["telefono"]).isnumeric):
            return "El telefono debe ser un numero"
    if (data["email"]) != '' :
        if type(data["email"]) != str:
            return "El email debe ser de tipo string" 
        
    if type(data["apellido"]) != str:
        return "El apellido debe ser de tipo string"
    
    if type(data["nombre"]) != str:
        return "El nombre debe ser de tipo string"
      
    
    if not(valid_direction(data["direccion"])):
        return "La direccion ingresada no es valida"
    if (data["direccion"]== " "):
        return "La direccion no puede quedar vacia"
    if (data["email"] != ''):
        if(not valid_email(data["email"])):
            return "El email ingresado no es valido"    
    if data["nombre"] == " ":
        return "El nombre no puede ser un string vacio"
    if data["apellido"] == " ":
        return "El apellido no puede ser un string vacio"
    if (data["genero"] == ""):
        return "El genero no puede estar vacio"
    if (data["estado"] == ""):
        return "EL genero no puede estar vacio"
    
def valid_email(email):
   reg = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(reg,email):
      return True
   return False

def valid_direction(direction):
    reg="[%&/()#!!-/:-@[-`{-~]"
    if re.match(reg,direction): 
        return False
    return True
