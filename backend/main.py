from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import interactions, chat, hcps

app = FastAPI(title="HCP CRM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://hcp-crm-gules.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hcps.router,         prefix="/api/hcps",         tags=["HCPs"])
app.include_router(interactions.router, prefix="/api/interactions",  tags=["Interactions"])
app.include_router(chat.router,         prefix="/api/chat",          tags=["Chat"])


@app.get("/")
async def root():
    return {"message": "HCP CRM API is running", "docs": "/docs"}
