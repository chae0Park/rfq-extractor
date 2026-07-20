from fastapi import APIRouter

from app.models.request import RFQRequest
from app.models.rfq import RFQExtraction
from app.services.extractor import RFQExtractor

router = APIRouter(
    prefix="/rfq",
    tags=["RFQ"],
)

extractor = RFQExtractor()


@router.post(
    "/extract",
    response_model=RFQExtraction,
    summary="Extract RFQ information from an email",
)
def extract_rfq(request: RFQRequest) -> RFQExtraction:
    return extractor.extract(request)