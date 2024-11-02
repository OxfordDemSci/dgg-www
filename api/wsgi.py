from app import create_app

if __name__ == "__main__":
    app = create_app("local_development")
    app.run(debug=True, port=8080)

else:
    app = create_app("development")