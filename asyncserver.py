import asyncio

from server import EchoServer

import settings

class SimpleServer(EchoServer):

    def __init__(self):

        EchoServer.__init__(self)

        self._loop = asyncio.get_event_loop()

        self.perform_mainloop()


    async def mainloop2(self):

        await asyncio.sleep(1)
        self.mainloop()
    
    def perform_mainloop(self):

    
        self._loop.run_until_complete(self.mainloop2())
        self._loop.run_forever()
        self._loop.close()





if __name__ == '__main__':

    server = SimpleServer()


    
