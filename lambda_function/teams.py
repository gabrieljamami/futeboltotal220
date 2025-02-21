import json
import requests
import boto3

def lambda_handler(event, context):
    # Configurações da API e S3
    chave_api = ''
    headers = {"X-Auth-Token": chave_api}
    base_url = "https://api.football-data.org/v4/competitions/PL/teams?season={}"
    s3_bucket = "futeboltotal220"
    s3_prefix = "raw/PL/teams/"
    
    s3 = boto3.client('s3')

    # Iterar pelas temporadas e salvar no S3
    for season in range(2022, 2025):
        url = base_url.format(season)
        
        # Requisição para a API de futebol
        response = requests.get(url, headers=headers)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            
            # Nome do arquivo JSON no S3
            s3_key = f"{s3_prefix}teams_season_{season}.json"

            # Upload para o S3
            s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=json.dumps(data))
            print(f"Dump da temporada {season} feito com sucesso!")
        else:
            print(f"Erro ao requisitar temporada {season}: {response.status_code}")
    
    # Retorno da execução bem-sucedida
    return {
        'statusCode': 200,
        'body': json.dumps('Execução concluída com sucesso!')
    }
