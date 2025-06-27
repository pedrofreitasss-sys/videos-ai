from flask import Flask, render_template, request
import pdfplumber
import openai
import os
from dotenv import load_dotenv

# Carrega a chave da OpenAI do arquivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files['file']

    with pdfplumber.open(file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    if "modo de preparo" in full_text.lower():
        trecho = full_text.lower().split("modo de preparo")[1][:1000]

        prompt = f"""
Você é um assistente que transforma textos técnicos em roteiros para vídeos educativos.
Simplifique e divida o seguinte passo a passo de forma acessível para vídeo:

{trecho}
"""

        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        roteiro = resposta['choices'][0]['message']['content']
        return f"<pre>{roteiro}</pre>"

    return "Modo de preparo não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
