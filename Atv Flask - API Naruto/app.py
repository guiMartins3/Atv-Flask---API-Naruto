from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

app = Flask(__name__, template_folder='views')  
routes.init_app(app)

# Permite ler o diretório absoluto de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passando o diretório do banco ao SQLSlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/Personagem.sqlite3')

# Define pasta que receberá arquivos de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Define o tamanho máximo de um arquivo de upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Iniciar o servidor
if __name__ == '__main__':
    db.init_app(app=app)
    # Cria o banco de dados quando a aplicação é rodada
    with app.test_request_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)