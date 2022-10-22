from wtforms import Form, BooleanField, StringField, PasswordField, validators

class validadoresDisciplinas():
    
    def validarForm(formulario):
        nombre = StringField('nombre',
        [
            validators.Requiered(message = "El nombre es requerido."),
            validators.length(min=2, max=25, message="Ingrese un nombre de usuario valido")
        ]
        )
        
