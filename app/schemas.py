from pydantic import BaseModel, Field
from typing import Optional


# =====================================================
# 🔗 SPRING BOOT → AI SERVICE (FULL CONTEXT REQUEST)
# =====================================================
# Used when Java backend calls AI service
# Includes IDs for logging, tracing, analytics
# AI logic itself SHOULD NOT depend on IDs
# =====================================================
class NegotiationAIRequest(BaseModel):
    user_id: int = Field(..., example=101)
    product_id: int = Field(..., example=55)

    base_price: float = Field(..., gt=0, example=100000)
    offered_price: float = Field(..., gt=0, example=85000)

    trust_score: float = Field(..., ge=0, le=100, example=72.5)
    attempt_number: int = Field(..., ge=1, le=3, example=2)

    class Config:
        schema_extra = {
            "example": {
                "user_id": 101,
                "product_id": 55,
                "base_price": 100000,
                "offered_price": 85000,
                "trust_score": 72.5,
                "attempt_number": 2
            }
        }


# =====================================================
# 📤 AI → SPRING BOOT RESPONSE
# =====================================================
# decision:
#   ACCEPT  → final_price filled
#   REJECT  → prices null
#   COUNTER → counter_price filled
# =====================================================
class NegotiationAIResponse(BaseModel):
    decision: str = Field(
        ...,
        description="ACCEPT | REJECT | COUNTER",
        example="COUNTER"
    )

    final_price: Optional[float] = Field(
        None,
        description="Final price if ACCEPT",
        example=90000
    )

    counter_price: Optional[float] = Field(
        None,
        description="Suggested counter price if COUNTER",
        example=91500
    )

    confidence_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="AI confidence between 0 and 1",
        example=0.87
    )

    explanation: str = Field(
        ...,
        description="Human-readable explanation for decision",
        example="Counter suggested due to moderate trust score and narrow price gap"
    )


# =====================================================
# 🤖 INTERNAL ML MODEL INPUT (FEATURE-ONLY)
# =====================================================
# Used ONLY inside predictor.py / trainer.py
# NO user_id, NO product_id (pure ML best practice)
# =====================================================
class NegotiationPredictionRequest(BaseModel):
    base_price: float = Field(..., gt=0, example=100000)
    offered_price: float = Field(..., gt=0, example=92000)
    trust_score: float = Field(..., ge=0, le=100, example=80)
    attempt_number: int = Field(..., ge=1, le=3, example=1)


# =====================================================
# 🤖 INTERNAL ML MODEL OUTPUT
# =====================================================
class NegotiationPredictionResponse(BaseModel):
    decision: str = Field(..., example="ACCEPTED")
    confidence: float = Field(..., ge=0, le=1, example=0.93)
    explanation: str = Field(
        ...,
        example="Model predicts high acceptance probability due to strong trust score"
    )
