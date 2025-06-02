import boto3
import datetime
import json
import uuid

def lambda_handler(event, context):
    #print("event: " + json.dumps(event))
    imageName = "default_"
    if 'imageName' in event:
        imageName = event['imageName']
    else:
        imageName = f'image_{uuid.uuid4().hex}.png'

    user_id = extract_user_id_from_event(event)

    s3_client = boto3.client('s3')
    bucket_name = "$BUCKET_NAME"  # alterar o nome adequadamente
    object_key = user_id + "/" + imageName

    print("object_key:", object_key)

    url = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=3600
    )
    print("URL gerada:", url)

    return {
        'statusCode': 200,
        'url': url
    }


def extract_user_id_from_event(event): # obtem os dados da credencial
  try:
    # 'cognito:username': o nome de usuário visível no Cognito.
    # 'sub': um identificador único do usuário no Cognito (caso não quiser identificar o usuário pelo nome).
    return event['requestContext']['authorizer']['claims']['cognito:username']
  except KeyError:
    return "desconhecido"
