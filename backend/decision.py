from config import RISK_THRESHOLD

def compute_risk_score(toxicity: float, sentiment: float, repetition_factor: float=0.0) -> float:
    """
    Risk formula:
    Risk = 0.6 * toxicity + 0.3 * sentiment + 0.1 * repetition_factor
    """
    return float((toxicity * 0.6) + (sentiment * 0.3) + (repetition_factor * 0.1))

def is_toxic(risk_score: float) -> bool:
    return risk_score > RISK_THRESHOLD
