from fastapi import FastAPI

from app.api.rfq import router as rfq_router

app = FastAPI(
    title="RFQ Extraction API",
    description="AI-powered RFQ Information Extraction Service",
    version="1.0.0",
)

app.include_router(rfq_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to RFQ Extraction API"
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok"
    }