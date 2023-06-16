from flask import Flask, request, jsonify
import json
from difflib import SequenceMatcher

app = Flask(__name__)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def apply_matching(json_a, json_b):
    for key_a, value_a in json_a.items():
        for key_b in json_b:
            similarity = similar(key_a, key_b)
            if similarity >= 0.98:
                json_b[key_b] = value_a
    return json_b

@app.route('/matcher-answers', methods=['POST'])
def process_files():
    if 'file_a' not in request.files or 'file_b' not in request.files:
        return jsonify({'error': 'Both files are required'})

    file_a = request.files['file_a']
    file_b = request.files['file_b']

    # Carrega o JSON A do arquivo
    json_a = json.load(file_a)

    # Carrega o JSON B do arquivo
    json_b = json.load(file_b)

    # Aplica o método Matcher
    json_result = apply_matching(json_a, json_b)

    # Salva o resultado em um arquivo JSON
    """with open('./output/destino.json', 'w') as output_file:
        json.dump(json_result, output_file)"""

    # Retorna uma resposta indicando o sucesso
    return jsonify({'message': 'File successfully processed', 'json': json_result})

if __name__ == '__main__':
    app.run(debug=True)
