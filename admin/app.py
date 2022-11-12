from os import environ
from pathlib import Path

from src.web import create_app

static_folder = Path(__file__).parent.joinpath("public")

app = create_app(static_folder=static_folder)
app.config['SECRET_KEY']= "Clave re secreta"


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
