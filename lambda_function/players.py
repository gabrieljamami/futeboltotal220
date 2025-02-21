import json
import boto3
import requests

# Acesso ao S3
s3_client = boto3.client('s3')
bucket_name = 'futeboltotal220'

# URL da API
api_url = 'https://api.football-data.org/v4/persons/'

# Token da API
api_token = ''

# Função para consultar a API
def get_player_data(pearson_id):
    headers = {
        'X-Auth-Token': api_token,  # Usando o token fornecido
    }
    
    response = requests.get(f"{api_url}{pearson_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retorna os dados da API em formato JSON
    else:
        print(f"Erro na API para ID {pearson_id}: {response.status_code}")
        return None

# Função principal que será executada pela Lambda
def lambda_handler(event, context):
    # Recebe os batches dos IDs vindos do SQS
    for record in event['Records']:
        # A mensagem do SQS contém o caminho do arquivo no S3
        message = json.loads(record['body'])
        batch_file_key = message['file_key']  # Obtém a chave do arquivo no S3
        print(f"Processando arquivo: {batch_file_key}")
        
        # Recupera o conteúdo do arquivo no S3
        batch_data = s3_client.get_object(Bucket=bucket_name, Key=batch_file_key)
        batch = json.loads(batch_data['Body'].read().decode('utf-8'))

        # Processa cada ID no batch
        for pearson_id in batch:
            player_data = get_player_data(pearson_id)

            if player_data:
                # Salva os dados obtidos no S3
                file_key = f'raw/PL/persons/{pearson_id}.json'
                s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(player_data))
