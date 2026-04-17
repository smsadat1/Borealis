import anyio
import asyncio
from grpc import aio
import secrets

from sqlmodel import select, Session

from rpc import auth_pb2, auth_pb2_grpc
from setup.db import engine, init_db
from setup.model import User


async def get_key():
    key = secrets.token_hex(16)
    return key


class AuthServicer(auth_pb2_grpc.AuthServicer):

    async def ValidateAPIKey(self, request, context):
        
        api_key = request.api_key

        def db_query():
            with Session(engine) as db:
                statement = select(User).where(User.api_key==api_key)
                return db.exec(statement).first()

        user = await anyio.to_thread.run_sync(db_query)

        if not user:
            return auth_pb2.ValidateResponse(valid=False, user_id="", rate_limit=0)
        
        return auth_pb2.ValidateResponse(valid=True, user_id=str(user.id), rate_limit=10)
    
    async def close(self):
        print("Closing Auth grpc server at port 50053")
        await self.channel.close()


async def serve():
    init_db()
    print("[AUTH] Starting Auth gRPC server...")
    server = aio.server() 
    servicer = AuthServicer()
    auth_pb2_grpc.add_AuthServicer_to_server(servicer, server)

    server.add_insecure_port('0.0.0.0:50053')
    await server.start()
    print("[AUTH] Auth gRPC server running on port 50053")

    try:
        await server.wait_for_termination()
    finally:
        await servicer.close()

if __name__ == "__main__":
    asyncio.run(serve())