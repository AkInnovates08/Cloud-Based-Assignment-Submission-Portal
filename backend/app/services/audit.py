import logging
logger = logging.getLogger("assignment_portal.audit")

def audit(action: str, user_id: int, details: str = ""):
    logger.info("action=%s user_id=%s details=%s", action, user_id, details)
