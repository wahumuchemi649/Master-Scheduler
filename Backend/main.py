from app import create_app

app = create_app()
@app.route("/")
def home():
    return "OK", 200

if __name__ == '__main__':
    
    app.run(debug=True)