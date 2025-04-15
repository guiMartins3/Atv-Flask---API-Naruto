from flask import Flask, app, render_template, request, redirect, url_for, flash
import requests
from models.database import db, Personagem, Imagem
# Essa biblioteca serve para ler uma determinada URL
import urllib
import json
import os
import uuid

ninja_list2 = []
ninja_list = [{'nome': 'Naruto Uzumaki', 
               'vila': 'Aldeia da Folha', 
               'rank': 'Hokage'}]

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/ninjas', methods=['GET', 'POST'])
    def ninjas():
        ninja = ninja_list[0]
        if request.method == 'POST':
            if request.form.get('ninja'):
                ninja_list2.append(request.form.get('ninja'))
                return redirect(url_for('ninjas'))

        return render_template('persoFav.html', ninja=ninja, ninja_list2=ninja_list2)

    @app.route('/cadninjas', methods=['GET', 'POST'])
    def cadninjas():
        # Paginação
        page = request.args.get('page', 1, type=int)  # Pega a página atual, padrão é 1
        per_page = 5  # Define quantos personagens por página

        # Consulta com paginação
        personagens_page = Personagem.query.paginate(page=page, per_page=per_page)

        if request.method == 'POST':
            nome = request.form['nome']
            aldeia = request.form['aldeia']
            rank = request.form['rank']
            
            # Criar um novo personagem e adicionar ao banco de dados
            novo_personagem = Personagem(nome=nome, aldeia=aldeia, rank=rank)
            db.session.add(novo_personagem)
            db.session.commit()

            return redirect(url_for('cadninjas'))

        return render_template('cadNinjas.html', personagens=personagens_page)

    
    @app.route('/editninja/<int:id>', methods=['GET', 'POST'])
    def editninja(id):
        personagem = Personagem.query.get_or_404(id)

        if request.method == 'POST':
            personagem.nome = request.form['nome']
            personagem.aldeia = request.form['aldeia']
            personagem.rank = request.form['rank']
            
            # Commit as alterações no banco de dados
            db.session.commit()
            
            return redirect(url_for('cadninjas'))

        return render_template('editNinjas.html', personagem=personagem)
    
    @app.route('/deleteninja/<int:id>', methods=['GET', 'POST'])
    def deleteninja(id):
        personagem = Personagem.query.get_or_404(id)

        # Excluir o personagem do banco de dados
        db.session.delete(personagem)
        db.session.commit()

        return redirect(url_for('cadninjas'))

    @app.route('/naruto_characters')
    def naruto_characters():
        url = "https://naruto-br-api.site/characters"
        response = requests.get(url)

        if response.status_code == 200:
            characters = response.json()

            for character in characters:
                if isinstance(character.get("village"), dict):
                    character["village"] = character["village"].get("name", "Desconhecida")
                else:
                    character["village"] = "Desconhecida"

            return render_template('naruto_characters.html', characters=characters)
        else:
            return f"Erro ao acessar a API: {response.status_code}"


     #Definindo tipos de arquivos permitidos
    FILE_TYPES=set(['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        return'.'in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES

    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        # Seleciona os nomes dos arquivos de imagens no banco
        imagens = Imagem.query.all()
        if request.method == 'POST':
            #Captura o arquivo vindo do formulário
            file = request.files['file']
            #Verifica se a extensão do arquivo é permitida
            if not arquivos_permitidos(file.filename):
                flash("Utilize os tipos de arquivos referentes a imagem.", 'danger')
                return redirect(request.url)
            
            #Define um nome aleatório para o arquivo
            filename = str(uuid.uuid4())
            
            #Gravando o nome do arquivo no banco
            img = Imagem(filename)
            db.session.add(img)
            db.session.commit()
 
            #Salva o arquivo na pasta de uploads
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Imagem enviada com sucesso!", 'success')
        return render_template('galeria.html', imagens=imagens)
    
if __name__ == '__main__':
    app.run(debug=True)
