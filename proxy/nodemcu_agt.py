import asyncio
import json
import os
from proxy.utils import read_yaml_config, singleton


_MAX_BUF_SIZE = 1024
_PROXY = None


def nodemcu_agt_set_proxy(proxy):
    global _PROXY
    _PROXY = proxy


# noinspection PyBroadException
@asyncio.coroutine
def handle_connection(reader, writer):
    while True:
        data = yield from reader.read(_MAX_BUF_SIZE)
        if not data:
            _PROXY.msg_2_aws(writer, "disconnect", None)
            return

        try:
            evt = json.JSONDecoder().decode(data.decode())
        except json.decoder.JSONDecodeError:
            continue
        except:
            continue
        else:
            for (key, val) in evt.items():
                _PROXY.msg_2_aws(writer, key, val)


@asyncio.coroutine
def handle_snd_buffer(l_buf):
    while True:
        if len(l_buf) != 0:
            tup = l_buf.pop()
            writer = tup[0]
            data = tup[1]
            writer.write(bytes(str.encode(json.dumps(data))))
            yield from writer.drain()
        else:
            yield from asyncio.sleep(0.3)


@asyncio.coroutine
def snd_data(client, data):
    client.write(data)
    yield from client.drain()


class NodemcuAgent(metaclass=singleton):
    def __init__(self):
        self.__config = read_yaml_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yaml'))
        self.__snd_buf = list()

    def send_data(self, writer, data):
        self.__snd_buf.append((writer, data))

    def start(self):
        loop = asyncio.get_event_loop()
        rcv_data = asyncio.start_server(handle_connection,
                                        self.__config["tcp_server"]["host"],
                                        self.__config["tcp_server"]["port"],
                                        loop=loop,
                                        reuse_address=True,
                                        reuse_port=True)

        tasks = [rcv_data, handle_snd_buffer(self.__snd_buf)]

        server = loop.run_until_complete(asyncio.gather(*tasks))

        try:
            loop.run_forever()
        finally:
            loop.close()
            server.close()
