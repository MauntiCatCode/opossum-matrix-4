from dataclasses import dataclass
from datetime import datetime


@dataclass
class GlobalTime:
    global_time: datetime

@dataclass
class DeltaTime:
    dt: float