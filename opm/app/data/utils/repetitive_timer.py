import asyncio


class RepetitiveTimer:
    def __init__(self, interval, task_func, *args, **kwargs):
        self.interval = interval
        self._task = None
        self._stop_signal = False
        self._task_func = task_func
        self._args = args
        self._kwargs = kwargs

    async def _repetitive_task(self):
        while not self._stop_signal:
            await self._task_func(*self._args, **self._kwargs)
            await asyncio.sleep(self.interval)

    def start_timer(self):
        if self._task is None:
            self._stop_signal = False
            self._task = asyncio.create_task(self._repetitive_task())

    def stop_timer(self):
        if self._task:
            self._stop_signal = True
            self._task = None
