import asyncio
from telethon import TelegramClient, events
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)

api_id = api_id_from_your_app
api_hash = "api_hash_from_your_app"

client = TelegramClient('session', api_id, api_hash)

# Lista dos canais
channel_ids = [
    -1001814812033,
    -1001683170953,
    -1001930458968,
    -1001793361060,
    -1001549517995,
    -1001850880231
]

connected_websockets = set()

# Dicionário para armazenar a última mensagem de cada canal
latest_messages = {}

async def websocket_handler(websocket, path):
    connected_websockets.add(websocket)
    try:
        async for message in websocket:
            pass
    finally:
        connected_websockets.remove(websocket)

async def handler(event):
    print('Handler iniciado')
    global channel_ids, latest_messages
    id = event.message.peer_id.channel_id
    id = f'-100{id}'
    print(id)
    if int(id) in channel_ids:
        mensagem = event.message.message
        # Atualizar a última mensagem para esse canal no dicionário latest_messages com o formato "id: mensagem"
        latest_messages[id] = mensagem
        # Converter o dicionário latest_messages em uma string JSON
        latest_messages_formatted = {k: f"{v}" for k, v in latest_messages.items()}
        latest_messages_json = json.dumps(latest_messages_formatted, ensure_ascii=False)
        print(f'\n\n{latest_messages_json}')
        for websocket in connected_websockets:
            try:
                # Enviar a última mensagem de cada canal no dicionário latest_messages aos clientes
                await websocket.send(latest_messages_json)
            except Exception as e:
                print(f'Erro ao enviar payload aos clients: {e}')
            finally:
                print(f'Payload enviado com sucesso!')

async def main():
    global channel_ids
    await client.start()
    start_server = websockets.serve(websocket_handler, "0.0.0.0", 5001)
    
    # Register the event handler
    client.add_event_handler(handler, events.NewMessage(chats=channel_ids))
    run = client.run_until_disconnected()
    # Run the websockets server
    await asyncio.gather(run, start_server)

if __name__ == '__main__':
    asyncio.run(main())
