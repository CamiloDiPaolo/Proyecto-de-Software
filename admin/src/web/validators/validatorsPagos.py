def validate_data(data, operation = "create"):
    # validamos que se ingresen los datos que se tengan que ingresar
    if not "fecha" in data and operation == "create":
        return "No ingresaste una fecha"
    if not "pago" in data and operation == "create": 
        return "No ingresaste un pago"
    if not "id_socio" in data and operation == "create":
        return "No ingresaste un numero de socio"
    
    # validamos que los tipos sean los correctos
    if type(data["pago"]) != str:
        return "El pago debe ser de tipo string"
    if type(data["fecha"]) != str:
        return "La fecha debe ser de tipo string"
    if type(data["id_socio"]) != str:
        return "La id del Socio debe ser de tipo string"

    
    # validamos cada campo por separado
    if data["pago"] == "":
        return "El pago no puede ser un string vacio"
    if data["fecha"] == "":
        return "La fecha no puede ser un string vacio"
    if data["id_socio"] == "":
        return "La id del Socio no puede ser un string vaion"

    return False

def validate_json(data):
    if not "date" in data:
        return "No ingresaste una fecha"
    if not "pay" in data:
        return "No ingresaste un pago"
    if not "certificate" in data:
        return "No ingresaste un certificado"
    
    if "date" in data == '':
        return "La fecha no debe estar vacia"
    if "pay" in data == '':
        return "El numero de pago no debe estar vacio"
    if "certificate" in data =='':
        return "El certificado no se pudo verificar correctamente"
    
    print(type(data["certificate"]))
    
    if  (type(data["date"])!= str):
        return "La fecha debe ser un string"
    if (type(data["certificate"])!= str):
        return "El certificado no se cargo correctamente"
    if (type(data["pay"]) != int):
        return "El numero de pago No es un numero"
    
    