from src import app

if __name__ == "__main__":
    app.env = "development"
    app.run(debug=True)
