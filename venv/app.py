from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
CORS(app)

rekognition = boto3.client(
    'rekognition',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

@app.route('/analisar-imagem', methods=['POST'])
def analisar_imagem():
    if 'imagem' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    file = request.files['imagem']
    image_bytes = file.read()

    try:
        response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=5,
            MinConfidence=80
        )
        labels = [label['Name'] for label in response['Labels']]
        descricao = 'Imagem contém: ' + ', '.join(labels)
        return jsonify({'descricao': descricao})
    except (BotoCoreError, ClientError) as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
