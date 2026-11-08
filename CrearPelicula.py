import json
import os
import uuid
import boto3

def lambda_handler(event, context):
    try:
        # 1. Extracción de variables desde el evento
        body = event['body']
        tenant_id = body['tenant_id']
        pelicula_datos = body['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # 2. Construcción e inserción del registro en DynamoDB
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # 3. Log estandarizado de ÉXITO ("INFO")
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "tenant_id": tenant_id,
                "uuid": uuidv4,
                "pelicula": pelicula
            }
        }
        print(json.dumps(log_info))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Película creada con éxito',
                'pelicula': pelicula
            }, ensure_ascii=False)
        }

    except Exception as e:
        # 4. Log estandarizado de ERROR ("ERROR")
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje_error": str(e),
                "evento_origen": event
            }
        }
        print(json.dumps(log_error))

        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Ocurrió un error al procesar la solicitud',
                'detalle': str(e)
            })
        }
