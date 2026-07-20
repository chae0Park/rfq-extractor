from openai import OpenAI

from app.config.settings import settings
from app.models.request import RFQRequest
from app.models.rfq import RFQExtraction
from app.prompts.extraction import EXTRACTION_SYSTEM_PROMPT


# class RFQExtractor:
#     def __init__(self):
#         self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
class RFQExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract(self, request: RFQRequest) -> RFQExtraction:
        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": EXTRACTION_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": request.email,
                },
            ],
            text_format=RFQExtraction,
        )

        return response.output_parsed