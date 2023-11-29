from dataclasses import dataclass
import datetime

@dataclass
class TimeInterval:
    start_time: datetime.time
    end_time: datetime.time
    