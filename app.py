from src.web import create_app

app = create_app()

def main():
    app.run()

if __name__ == "__main__":
    main()