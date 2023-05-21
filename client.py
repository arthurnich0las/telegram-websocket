import asyncio
import websockets

HOST = 'localhost'
PORT = 5000

async def main():
    async with websockets.connect(f'ws://localhost:5001') as websocket:
        await websocket.send('')

        while True:
            data = await websocket.recv()
            print(f'Dados recebidos: {data}')

if __name__ == '__main__':
    asyncio.run(main())
