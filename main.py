from fastapi import APIRouter, FastAPI
import uvicorn
from api.handlers import user_crud


app = FastAPI(title="data manager by phone")

main_api_router = APIRouter()
app.include_router(user_crud)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# connect to db
# dal
# cash
# docker
# tests
