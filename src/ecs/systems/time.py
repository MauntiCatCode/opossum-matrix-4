import esper

from datetime import datetime, timedelta

from ..components.time import GlobalTime, DeltaTime
from ..utils import get_singleton_component

class TimeSystem(esper.Processor):
    def __init__(self):
        self._ecs_time = get_singleton_component(GlobalTime)
        self._ecs_dt = get_singleton_component(DeltaTime)
        self._dt = timedelta(0)
        self._real_time = datetime.now()

    def process(self):
        self._update_real_time()
        self._ecs_time.global_time += self.dt
        self._ecs_dt.dt = self.dt.total_seconds()

    def _update_real_time(self):
        now = datetime.now()
        self.dt = now - self._real_time
        self.real_time = now
 