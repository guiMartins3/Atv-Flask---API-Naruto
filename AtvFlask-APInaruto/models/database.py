from flask_sqlalchemy import SQLAlchemy

# Criando uma instância do SQLAlchemy
db = SQLAlchemy()

# Classe responsável por criar a entidade "Personagem" no banco com seus atributos
class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(150))
    aldeia = db.Column(db.String(150))
    rank = db.Column(db.String(50))
    
    # Método Construtor da classe
    def __init__(self, nome, aldeia, rank):
        self.nome = nome
        self.aldeia = aldeia
        self.rank = rank
        

# Classe para imagens
class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, filename):
        self.filename = filename