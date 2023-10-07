import nats
import json
import time

NATS_TOPICOS = "6512dca521ba772b300c0a53.stat.652018e269c5153ed05bed5a.0x4a2f7e1b3d5c8f90"

async def publish( position: str):
    client = await nats.connect(servers=["nats://leaf-node-aws.olli.digital:4222"], 
                                user_credentials="auth/user.creds", 
                                connect_timeout=3)

    message = json.dumps({"position":position}).encode()

    await client.publish(NATS_TOPICOS, message)
    await client.drain()
