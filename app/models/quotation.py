from pydantic import BaseModel, Field


class CostBreakdown(BaseModel):
    base_cost: float = Field(
        description="Base cost determined by the target country."
    )

    sample_cost: float = Field(
        default=0,
        description="Additional cost based on sample size."
    )

    loi_multiplier: float = Field(
        default=1.0,
        description="Cost multiplier based on interview length."
    )

    ir_multiplier: float = Field(
        default=1.0,
        description="Cost multiplier based on incidence rate."
    )


class QuotationResult(BaseModel):
    country: str

    total_cost: float

    breakdown: CostBreakdown