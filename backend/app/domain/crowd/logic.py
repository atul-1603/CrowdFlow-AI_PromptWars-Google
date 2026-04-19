def get_status_label(density: int) -> str:
    """Business rule to translate percentage into a meaningful status label."""
    if density < 40:
        return "LOW"
    elif density < 75:
        return "MEDIUM"
    elif density < 90:
        return "HIGH"
    else:
        return "CRITICAL"
