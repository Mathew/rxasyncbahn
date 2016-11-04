from autobahn.asyncio.websocket import (
    WebSocketClientProtocol, WebSocketClientFactory
)


class LobbyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Connected: {}".format(response.peer))

    def onOpen(self):
        print("Subscribing")
        self.sendMessage("I'm subscribing".encode('utf8'))

    def onMessage(self, payload, is_binary):
        print("from server: {}".format(payload))


if __name__ == '__main__':
    import asyncio

    factory = WebSocketClientFactory()
    factory.protocol = LobbyClientProtocol


loop = asyncio.get_event_loop()
coro = loop.create_connection(factory, '0.0.0.0', 9000)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
