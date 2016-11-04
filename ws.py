from autobahn.asyncio.websocket import (
    WebSocketServerProtocol, WebSocketServerFactory
)

from rx import Observable
from rx.concurrency import AsyncIOScheduler


class ServiceClient:
    def __init__(self):
        sock = ctx.socket(zmq.PULL)
        sock.bind(url)
        msg = yield from sock.recv_multipart() # waits for msg to be ready
        reply = yield from async_process(msg)
        out = yield from sock.send_multipart(reply)

        next(out)

    def get(self):
        pass


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.broadcast_manager = BroadcastManager()


class BroadcastManager:

    def __init__(self):
        self._clients = []
        # Spit out an incrementing number across multiple subscribers.
        self.obs = Observable.interval(100).share()

    def register_client(self, client):
        self._clients.append(client)

    def unregister_client(self, client):
        self._clients.remove(client)

    def get_count(self):
        return len(self._clients)

    def subscribe(self, client):
        def on_next(x):
            print("running")
            client.sendMessage(str(x).encode('utf8'), False)

        def on_completed(x):
            print("completed")

        def on_error(e):
            print("An error occured: {}".format(e)

        subscription = self.obs.subscribe(
            on_next, on_completed, on_error
        )

        return subscription


class LobbyProtocol(WebSocketServerProtocol):
    def onMessage(self, payload, is_binary):
        if is_binary is False:
            print("incoming: {}".format(payload.decode('utf8')))

        print("subscribing")
        self.subscription = self.factory.broadcast_manager.subscribe(self)

        print("sending count")
        self.sendMessage(
            "Open Clients: {}".format(
                self.factory.broadcast_manager.get_count()
            ).encode('utf8'),
            False
        )

    def onConnect(self, request):
        self.factory.broadcast_manager.register_client(self)

    def onOpen(self):
        print("on open")

    def onClose(self, was_clean, code, reason):
        self.subscription.dispose()
        print("closed")


if __name__ == '__main__':
    import asyncio

    factory = BroadcastServerFactory()
    factory.protocol = LobbyProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
