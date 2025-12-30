from datetime import datetime
from typing import Optional, Dict, Any

class Session:
    """
    מחלקה לניהול מצב סשן המשתמש
    """
    def __init__(self):
        self.active: bool = False
        self.awaiting_problem: bool = False
        self.analysis: Optional[Any] = None
        self.slots: Dict[str, str] = {}
        self.pending_slot: Optional[str] = None
        self.pending_kind: Optional[str] = None
        self.pending_question: Optional[str] = None
        self.last_activity: datetime = datetime.now()
    
    def update_activity(self):
        """עדכון זמן פעילות אחרון"""
        self.last_activity = datetime.now()
    
    def reset(self):
        """איפוס הסשן"""
        self.active = False
        self.awaiting_problem = False
        self.analysis = None
        self.slots = {}
        self.pending_slot = None
        self.pending_kind = None
        self.pending_question = None
        self.last_activity = datetime.now()