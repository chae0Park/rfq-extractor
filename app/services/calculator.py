from app.models.quotation import CostBreakdown, QuotationResult
from app.models.rfq import RFQExtraction
from app.services.base_cost_loader import BaseCostLoader
from app.services.panel_cpi_loader import PanelCPILoader
from app.services.translation_fee_loader import TranslationFeeLoader


class RFQCalculator:

    def __init__(self):
        self.base_cost_loader = BaseCostLoader()
        self.panel_cpi_loader = PanelCPILoader()
        self.translation_fee_loader = TranslationFeeLoader()

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

        programming_fee = self._calculate_programming_fee(rfq)
        translation_fee = self._calculate_translation_fee(rfq)

        direct_cost = (
            base_cost
            + sample_cost
            + programming_fee
            + translation_fee
        )

        pm_fee = self._calculate_pm_fee(direct_cost)

        subtotal = direct_cost + pm_fee

        rush_fee = self._calculate_rush_fee(
            subtotal,
            rfq.rush,
        )

        subtotal += rush_fee

        margin = self._calculate_margin(subtotal)

        total_before_discount = subtotal + margin

        client_discount = self._calculate_client_discount(
            total_before_discount,
            rfq.client_tier,
        )

        total_cost = total_before_discount - client_discount


        return QuotationResult(
            country=rfq.country,
            total_cost=total_cost,
            breakdown=CostBreakdown(
                base_cost=base_cost,
                sample_cost=sample_cost,
                loi_multiplier=loi_multiplier,
                ir_multiplier=ir_multiplier,
                programming_fee=programming_fee,
                translation_fee=translation_fee,
                pm_fee=pm_fee,
                rush_fee=rush_fee,
                margin=margin,
                client_discount=client_discount,
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
        
    def _calculate_programming_fee(
        self,
        rfq: RFQExtraction,
    ) -> float:

        if rfq.loi is None:
            return 500

        if rfq.loi <= 10:
            return 500
        elif rfq.loi <= 20:
            return 700
        elif rfq.loi <= 30:
            return 900
        else:
            return 1200
        
    # def _calculate_translation_fee(
    #     self,
    #     rfq: RFQExtraction,
    # ) -> float:

    #     if (
    #         rfq.source_language is None
    #         or rfq.target_language is None
    #     ):
    #         return 0

    #     return self.translation_fee_loader.get_fee(
    #         rfq.source_language,
    #         rfq.target_language,
    #     )

    def _calculate_translation_fee(
        self,
        rfq: RFQExtraction,
    ) -> float:

        if not rfq.languages:
            return 0

        total_fee = 0

        for language in rfq.languages:
            total_fee += self.translation_fee_loader.get_fee(
                "English",
                language,
            )

        return total_fee
    
    def _calculate_pm_fee(
        self,
        subtotal: float,
    ) -> float:
        return round(subtotal * 0.10, 2)
    
    def _calculate_margin(
        self,
        subtotal: float,
    ) -> float:
        return round(subtotal * 0.20, 2)
    
    def _calculate_rush_fee(
        self,
        subtotal: float,
        rush: bool | None,
    ) -> float:

        if not rush:
            return 0

        return round(subtotal * 0.15, 2)
    
    def _calculate_client_discount(
        self,
        total_cost: float,
        client_tier: str | None,
    ) -> float:

        if client_tier == "Premium":
            return round(total_cost * 0.05, 2)

        if client_tier == "Enterprise":
            return round(total_cost * 0.10, 2)

        return 0