from src.web import create_app
from src.core.db import init_db

app = create_app()
app.config['SECRET_KEY']= "Clave re secreta"


def main():
    app.run(debug=True)

if __name__ == "__main__":
    init_db()
    main()
