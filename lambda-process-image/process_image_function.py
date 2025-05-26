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
    # Evento de trigger do S3
    for record in event['Records']:
        bucket = record['s3']['$S3_BUCKET_NAME']['name'] #replace the bucket name
        key = record['s3']['object']['key']
        s3_url = f"s3://{bucket}/{key}"

        try:
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

            user_id = extract_user_id_from_event(event)
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
            print(f"Erro ao processar {key}: {str(e)}")
            raise

    return {
        'statusCode': 200,
        'body': 'Processamento concluído.'
    }

def extract_user_id_from_event(event): # obtem os dados da credencial
  try:
    # 'username': o nome de usuário visível no Cognito, se preferir algo mais legível.
    # 'sub': um identificador único do usuário no Cognito.
    return event['requestContext']['authorizer']['claims']['username']
  except KeyError:
    return "desconhecido"