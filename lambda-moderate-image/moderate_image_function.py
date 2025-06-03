import json

def lambda_handler(event, context):
    print("Moderando evento de imagem.")
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda moderarImagem ok!')
    }