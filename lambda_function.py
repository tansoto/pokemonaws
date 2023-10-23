import json
import psycopg2
import os
from psycopg2 import sql

def lambda_handler(event, context):
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_port = os.environ['DB_PORT']

    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        print("Connected to database")
        cursor = conn.cursor()
        body = json.loads(event['body'])
        nombre = body['nombre_pokemon']
        tipo = body['tipo_pokemon']
        region = body['region_pokemon']
        insert = sql.SQL("INSERT INTO pokemon (nombre_pokemon) VALUES ({nombre}) returning id")

        cursor.execute(insert)
        id_pokemon = cursor.fetchone()[0]
        conn.commit

        insert = sql.SQL("INSERT INTO tipo pokemon = {id_pokemon}, tipo_pokemon = {tipo}")
        cursor.execute(insert)
        conn.commit
        insert = sql.SQL("INSERT INTO region pokemon = {id_pokemon}, region_pokemon = {region}")
        cursor.execute(insert)
        conn.commit

        cursor.close()
        conn.close()

        response = {
            "statusCode": 200,
            "body": "Pokemon insertado correctamente"
        }
    except Exception as e:
        print(e)
        response = {
            "statusCode": 500,
            "body": "Error al insertar el pokemon"
        }
    return response
        