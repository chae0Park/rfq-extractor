from app.models.quotation import CostBreakdown, QuotationResult
from app.models.rfq import RFQExtraction
from app.services.base_cost_loader import BaseCostLoader
from app.services.panel_cpi_loader import PanelCPILoader


class RFQCalculator:

    def __init__(self):
        self.base_cost_loader = BaseCostLoader()
        self.panel_cpi_loader = PanelCPILoader()

    def calculate(self, rfq: RFQExtraction) -> QuotationResult:
        if rfq.country is None:
            raise ValueError("Country is required for quotation calculation.")

        base_cost = self.base_cost_loader.get_base_cost(rfq.country)

        loi_multiplier = self._calculate_loi_multiplier(rfq.loi)
        ir_multiplier = self._calculate_ir_multiplier(rfq.ir)

        sample_cost = (
            self._calculate_sample_cost(
                rfq.country,
                rfq.sample_size,
            )
            * loi_multiplier
            * ir_multiplier
        )

        total_cost = base_cost + sample_cost

        return QuotationResult(
            country=rfq.country,
            total_cost=total_cost,
            breakdown=CostBreakdown(
                base_cost=base_cost,
                sample_cost=sample_cost,
                loi_multiplier=loi_multiplier,
                ir_multiplier=ir_multiplier,
            ),
        )

    def _calculate_sample_cost(
        self,
        country: str,
        sample_size: int | None,
    ) -> float:

        if sample_size is None:
            return 0

        cpi = self.panel_cpi_loader.get_panel_cpi(country)

        return sample_size * cpi
    

    def _calculate_loi_multiplier(
        self,
        loi: int | None,
    ) -> float:

        if loi is None:
            return 1.0

        if loi <= 10:
            return 1.0
        elif loi <= 15:
            return 1.15
        elif loi <= 20:
            return 1.30
        elif loi <= 25:
            return 1.50
        else:
            return 1.80
        
    def _calculate_ir_multiplier(
        self,
        ir: int | None,
    ) -> float:

        if ir is None:
            return 1.0

        if ir >= 80:
            return 1.0
        elif ir >= 60:
            return 1.10
        elif ir >= 40:
            return 1.25
        elif ir >= 20:
            return 1.50
        elif ir >= 10:
            return 2.00
        else:
            return 3.00