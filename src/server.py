import dataclasses
import asyncio
import vhttp


@dataclasses.dataclass
class ServerSettings:
    bind_address: str
    port: int


class Server:
    def __init__(self, settings: ServerSettings):
        self.settings = settings

    def run(self):
        asyncio.run(self.arun())

    async def arun(self):
        server = await asyncio.start_server(self.handle_connection, self.settings.bind_address, self.settings.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def handle_connection(self, reader: asyncio.StreamReader, writer):
        print(f"Connection")
        try:
            request = await vhttp.HttpRequest.read(reader)
            print(f"{request.request_line.method} {request.request_line.uri}")
        except vhttp.HttpError:
            pass  # TODO: send error response
