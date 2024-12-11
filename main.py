from nex.rmc import RMCError, RMCClient
from nex.prudp import serve
from nex import settings
from nex.kerberos import KeyDerivationOld
from nex_logger.logger import Logger

import contextlib
import aioconsole
import redis
import os
import asyncio
from dotenv import load_dotenv

logger = Logger()
load_dotenv()

TITLE_ID=0x1010EB00
ACCESS_KEY="25dbf96a"
NEX_VERSION=30504
SECURE_SERVER="Quazal Rendez-Vous"

NEX_SETTINGS = settings.default()
NEX_SETTINGS.configure(ACCESS_KEY, NEX_VERSION)
NEX_SETTINGS["prudp.resend_timeout"] = 1.5
NEX_SETTINGS["prudp.resend_limit"] = 3
NEX_SETTINGS["prudp.version"] = 1
NEX_SETTINGS["prudp.max_substream_id"] = 1

redis_client = redis.from_url(os.getenv("REDIS_URI"))
redis_client.ping()

@contextlib.asynccontextmanager
async def prudp_serve(settings, servers, host="", port=0, vport=1, context=None, key=None):
	async def handle(client):
		host, port = client.remote_address()
		logger.info("New connection: %s:%i", host, port)
		
		client = RMCClient(settings, client)
		async with client:
			await client.start(servers)
	
	logger.info("Starting server at %s:%i:%i", host, port, vport)
	async with serve(handle, settings, host, port, vport, 10, context, key):
		yield
	logger.info("Server is closed.")

async def main():
    settings = NEX_SETTINGS

    auth_servers = [

    ]
    secure_servers = [
        
    ]

    server_key = KeyDerivationOld(65000, 1024).derive_key(os.getenv("KERBEROS_PASSWORD"), pid=2)
    async with prudp_serve(settings, auth_servers, os.getenv("SERVER_IP_ADDRESS"), os.getenv("AUTHENTICATION_PORT")):
        async with prudp_serve(settings, secure_servers, os.getenv("SERVER_IP_ADDRESS"), os.getenv("SECURE_PORT"), key=server_key):
            await aioconsole.ainput("Press ENTER to close the server..\n")


asyncio.run(main())