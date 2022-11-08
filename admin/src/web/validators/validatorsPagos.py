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