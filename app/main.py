# ------------------------- Libraries -------------------------
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.starting_counter import increment_counter
from app.routers import user, listing, auth, weather

# Initialize FastAPI app
app = FastAPI()

increment_counter()

ALLOWED_ORIGINS = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CLIENTS = ["127.0.0.1", "172.23.0.1"]


@app.middleware("http")
async def allowed_client_ips(request: Request, call_next):
    allowed_clients = set(ALLOWED_CLIENTS)

    # Handle cases where request.client is None, e.g., during tests
    client_ip = request.client.host if request.client else "127.0.0.1"

    if client_ip not in allowed_clients:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "This IP is not allowed."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = await call_next(request)
    return response


# ------------------------- Routes -------------------------

@app.get('/')
def root():
    return {"message": "Hello World!"}


app.include_router(user.router)
app.include_router(listing.router)
app.include_router(auth.router)
app.include_router(weather.router)
