import asyncio

from client import EchoClient

import settings

import threading


class SimpleClient(EchoClient):

    def __init__(self):
        EchoClient.__init__(self)
        self._loop = asyncio.get_event_loop()
        self.perform_run()
       



    async def run2(self):

        await asyncio.sleep(1)
        print('running')
        self.run()
    
    def perform_run(self):

        
        self._loop.run_until_complete(self.run2())
        

        self._loop.close()
if __name__ == '__main__':

    client = SimpleClient()
    client_thread = threading.Thread(target=client, daemon=True)
    client_thread.start()



