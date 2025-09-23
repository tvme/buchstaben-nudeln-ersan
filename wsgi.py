from app import app  # app — это имя вашего файла с приложением

application = app

if __name__ == '__main__':
    app.run(debug=False)