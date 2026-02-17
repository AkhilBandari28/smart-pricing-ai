from fastapi import FastAPI
from app.schemas import (
    NegotiationAIRequest,
    NegotiationAIResponse
)
from app.predictor import predict_negotiation

app = FastAPI(
    title="Smart Pricing AI Service",
    description="AI-powered negotiation decision engine",
    version="1.1.0"
)

# =====================================================
# 🔍 HEALTH CHECK
# =====================================================
@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "message": "AI Service is running"
    }


# =====================================================
# 🤖 AI NEGOTIATION ENDPOINT
# =====================================================
@app.post("/ai/negotiate", response_model=NegotiationAIResponse)
def ai_negotiate(request: NegotiationAIRequest):

    """
    Receives negotiation context from Spring Boot
    Calls ML model
    Returns ACCEPT / REJECT / COUNTER decision
    """

    # =========================
    # 🤖 ML PREDICTION
    # =========================
    prediction = predict_negotiation(
        base_price=request.base_price,
        offered_price=request.offered_price,
        trust_score=request.trust_score,
        attempt_number=request.attempt_number
    )

    decision = prediction["decision"]
    confidence = float(prediction["confidence"])
    explanation = prediction["explanation"]

    # =========================
    # 🧠 DECISION MAPPING
    # =========================
    if decision == "ACCEPTED":
        return NegotiationAIResponse(
            decision="ACCEPT",
            final_price=request.offered_price,
            confidence_score=confidence,
            explanation=explanation
        )

    elif decision == "COUNTER":
        # Smart counter logic (example)
        counter_price = max(
            request.offered_price,
            request.base_price * 0.92
        )

        return NegotiationAIResponse(
            decision="COUNTER",
            counter_price=round(counter_price, 2),
            confidence_score=confidence,
            explanation=explanation
        )

    else:
        return NegotiationAIResponse(
            decision="REJECT",
            final_price=None,
            confidence_score=confidence,
            explanation=explanation
        )
