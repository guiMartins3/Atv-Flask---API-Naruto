from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

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
        if request.method == 'POST':
            form_data = request.form.to_dict()
            ninja_list.append(form_data)
            return redirect(url_for('cadninjas')) 

        return render_template('cadNinjas.html', ninja_list=ninja_list)

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
