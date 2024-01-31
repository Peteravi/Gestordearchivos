from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:piteravi07@localhost:3306/file_manager'
db = SQLAlchemy(app)

# Configura la carpeta estática
app.static_folder = 'static'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # Crea el directorio si no existe
            os.makedirs('uploads', exist_ok=True)

            # Guarda el archivo en el directorio de carga
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Agrega la información del archivo a la base de datos
            new_file = File(filename=file.filename)
            db.session.add(new_file)
            db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Abre la aplicación en el navegador automáticamente
    webbrowser.open('http://127.0.0.1:5000')
    
    app.run(debug=True)