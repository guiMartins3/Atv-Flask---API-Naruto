from flask import render_template, request, redirect, url_for
import requests
from models.database import db, Personagem
# Essa biblioteca serve para ler uma determinada URL
import urllib
import json

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

if __name__ == '__main__':
    app.run(debug=True)
