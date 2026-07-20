from fastapi import APIRouter

from app.models.request import RFQRequest
from app.models.result import RFQExtractionResult
from app.services.extractor import RFQExtractor

router = APIRouter(
    prefix="/rfq",
    tags=["RFQ"],
)

extractor = RFQExtractor()


@router.post(
    "/extract",
    response_model=RFQExtractionResult,
    summary="Extract RFQ information from an email",
)
def extract_rfq(request: RFQRequest) -> RFQExtractionResult:
    return extractor.extract(request)