import asyncio
from telethon import TelegramClient, events
import websockets
import logging

logging.basicConfig(level=logging.INFO)

api_id = 24189974
api_hash = '9f92d41c87279a7d0ba64fc8cff6f584'
phone_number = '+5582996124615'

client = TelegramClient('session', api_id, api_hash)

mensagens = []

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

async def websocket_handler(websocket, path):
    connected_websockets.add(websocket)
    try:
        async for message in websocket:
            pass
    finally:
        connected_websockets.remove(websocket)


async def handler(event):
    print('Handler iniciado')
    global channel_ids
    id = event.message.peer_id.channel_id
    id = f'-100{id}'
    print(id)
    if int(id) in channel_ids:
        mensagem = event.message.message
        payload = f"Nova Mensagem: {mensagem} Id: {id}"
        mensagens.append(payload)
        print(payload)
        for websocket in connected_websockets:
            try:
                await websocket.send(payload)
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
