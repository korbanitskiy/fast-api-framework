import fastapi
import uvicorn

from app.api import example_endpoint
from app.ORM.database import Base, engine

Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI()


def configure():
    app.include_router(example_endpoint.router)


configure()

if __name__ == '__main__':
    uvicorn.run(app)
