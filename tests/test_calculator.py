from app.models.rfq import RFQExtraction
from app.services.calculator import RFQCalculator


def main():
    
    rfq = RFQExtraction(
        country="South Korea",
        sample_size=1000,
        loi=20,
        ir=20,
        languages=[
            "Korean",
            "Japanese",
        ],
        rush=True,
        client_tier="Enterprise",
    )
    calculator = RFQCalculator()

    result = calculator.calculate(rfq)

    print(result.model_dump())


if __name__ == "__main__":
    main()