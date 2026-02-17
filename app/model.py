# app/model.py

from enum import Enum
from typing import Dict


class Decision(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COUNTER = "COUNTER"


def build_ai_response(
    prediction: str,
    probability: float,
    base_price: float,
    offered_price: float,
    trust_score: float,
    attempt_number: int
) -> Dict:
    """
    Converts raw ML output into explainable AI response
    """

    price_ratio = round(offered_price / base_price, 2)

    if prediction == Decision.ACCEPTED:
        explanation = (
            "The AI accepted your offer because it is close to the base price "
            "and your trust score indicates reliable negotiation behavior."
        )
    elif prediction == Decision.COUNTER:
        explanation = (
            "The AI suggests a counter offer because the price difference is moderate "
            "and negotiation history allows flexibility."
        )
    else:
        explanation = (
            "The AI rejected the offer because the price deviation is too high "
            "based on current trust score and negotiation patterns."
        )

    return {
        "decision": prediction,
        "finalPrice": offered_price if prediction == Decision.ACCEPTED else base_price,
        "confidence": round(probability, 2),
        "explanation": explanation,
        "metadata": {
            "basePrice": base_price,
            "offeredPrice": offered_price,
            "priceRatio": price_ratio,
            "trustScore": trust_score,
            "attemptNumber": attempt_number
        }
    }
