import json

def lambda_handler(event, context):
    print("Processando evento de imagem com erro.")
    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda notificarErro ok!')
    }