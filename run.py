from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from .env

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
