import asyncio
import websockets

HOST = 'localhost'
PORT = 5000

async def main():
    async with websockets.connect(f'wss://85f8-2804-29b8-511b-4d4f-00-102.ngrok-free.app') as websocket:
        await websocket.send('Bom dia tropa')

        while True:
            data = await websocket.recv()
            print(f'Dados recebidos: {data}')

if __name__ == '__main__':
    asyncio.run(main())
