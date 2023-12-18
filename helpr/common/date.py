from dataclasses import dataclass
from datetime import datetime

@dataclass
class TimeInterval:
    start_time: datetime
    end_time: datetime