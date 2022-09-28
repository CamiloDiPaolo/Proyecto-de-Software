from src.web import create_app
from src.core.db import init_db

app = create_app()

def main():
    app.run(debug=True)

if __name__ == "__main__":
    init_db()
    main()
