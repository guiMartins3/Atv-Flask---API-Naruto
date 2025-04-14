from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

# Criação do objeto Flask
app = Flask(__name__, template_folder='views')  

# Definindo a URI do banco de dados (SQLite)
dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/Personagem.sqlite3')

# Configurações de uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Tamanho máximo de upload

# Configuração da chave secreta
app.config['SECRET_KEY'] = os.urandom(24)

# Inicializa o banco de dados
db.init_app(app)

# Definir as rotas da aplicação
routes.init_app(app)

# Criação do banco de dados quando a aplicação for rodada
with app.app_context():  # Alteração aqui para usar o contexto correto
    db.create_all()

# Iniciar o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
