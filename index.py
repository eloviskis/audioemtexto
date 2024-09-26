from flask import Flask, render_template, request, redirect, url_for
import whisper
import os

model = whisper.load_model("tiny")

app = Flask(__name__)

# Carregar o modelo Whisper
model = whisper.load_model("base")

# Página principal (frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para upload de áudio e transcrição
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Salvar o arquivo temporariamente
        filepath = os.path.join("static", file.filename)
        file.save(filepath)

        # Transcrever o áudio usando Whisper
        result = model.transcribe(filepath)
        text = result["text"]

        # Remover o arquivo de áudio após a transcrição
        os.remove(filepath)

        return render_template('index.html', transcription=text)

if __name__ == "__main__":
    app.run(debug=True)
