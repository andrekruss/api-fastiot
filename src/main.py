from contextlib import asynccontextmanager
import sys
from fastapi import FastAPI
import uvicorn
from subprocess import run

from database.config import connect_to_db
from controllers.user_controller import user_router
from controllers.auth_controller import auth_router
from controllers.project_controller import project_router
from controllers.module_controller import module_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup actions (called during startup)
    await connect_to_db()
    yield 
    print("Shutting down the app...")

app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(module_router)

if __name__ == "__main__":
    
    if "--reload" in sys.argv:
        # run with python -m main --reload
        run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"])
    else:
        # run with python -m main
        uvicorn.run("main:app", host="0.0.0.0", port=8001)