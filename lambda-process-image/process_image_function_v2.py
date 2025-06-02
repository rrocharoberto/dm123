import boto3
from PIL import Image
from io import BytesIO
import uuid
import json
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dm123-images')

def lambda_handler(event, context):
    print("Iniciando processamento da imagem.")
    print("event: " + json.dumps(event))
    try:
        # Evento do SQS
        record = event['Records'][0]
        print("record: " + json.dumps(record))
        body = json.loads(record['body'])
        print("body: " + json.dumps(body))
        s3_record = body['Records'][0]
        print("s3_record: " + json.dumps(s3_record))
        bucket_name = s3_record['s3']['bucket']['name']
        object_key = s3_record['s3']['object']['key']
                
        process_image(bucket_name, object_key)
    except Exception as e:
        print(f"Erro ao processar evento: {event}: {str(e)}")
        raise

    print("Finalizando processamento da imagem.")
    return {
        'statusCode': 200,
        'body': 'Processamento concluído.'
    }

def process_image(bucket, key):
    print(f"Processando bucket: {bucket} objeto: {key}")
    try:
        s3_url = f"s3://{bucket}/{key}"

        # Baixar imagem
        response = s3.get_object(Bucket=bucket, Key=key)
        img_data = response['Body'].read()
        image = Image.open(BytesIO(img_data))
        
        # Extrair metadados básicos
        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,  # (width, height)
        }

        user_id = get_user_id_from_s3_object(key)
        # Criar um registro para o DynamoDB
        item = {
            "imageId": str(uuid.uuid4()),
            "userId": user_id,
            "createdAt": datetime.utcnow().isoformat(),
            "s3url": s3_url,
            "status": "PROCESSADO",
            "metadata": json.dumps(metadata)
        }

        # Inserir no DynamoDB
        table.put_item(Item=item)
        
    except Exception as e:
        print(f"Erro ao processar {bucket}:{key}: {str(e)}")
        raise

def get_user_id_from_s3_object(object_key):
  try:
    # Extracts the first part of an S3 object key (before the first slash).
    return object_key.split('/')[0]
  except KeyError:
    return "desconhecido"
