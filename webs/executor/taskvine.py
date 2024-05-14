from __future__ import annotations

import sys
from concurrent.futures import Executor
from concurrent.futures import Future
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import TypeVar

if sys.version_info >= (3, 10):  # pragma: >=3.10 cover
    from typing import ParamSpec
else:  # pragma: <3.10 cover
    from typing_extensions import ParamSpec

from pydantic import Field

try:
    import ndcctools.taskvine as vine
    FuturesExecutor = vine.FuturesExecutor
    TASK_VINE_AVAILABLE = True
except ImportError:
    FuturesExecutor = object
    TASK_VINE_AVAILABLE = False

from webs.executor.config import ExecutorConfig
from webs.executor.config import register

P = ParamSpec('P')
T = TypeVar('T')


class TaskVineExecutor(FuturesExecutor):
    def submit(self, fn, *args, **kwargs):
        if isinstance(fn, vine.FuturePythonTask):
            self.manager.submit(fn)
            return fn._future
        elif isinstance(fn, vine.FutureFunctionCall):
            self.manager.submit(fn)
            self.task_table.append(fn)
            return fn._future
        else:
            future_task = self.future_task(fn, *args, **kwargs)
            self.submit(future_task)
            return future_task._future



@register(name='taskvine')
class TaskVineConfig(ExecutorConfig):
    """TaskVine configuration.

    Attributes:
        taskvine_port: TaskVine manager port.
    """

    taskvine_port: int | list[int] = Field([9123, 9129], description='taskvine manager port(s)')

    def get_executor(self) -> TaskVineExecutor:
        """Create an executor instance from the config."""
        if not TASK_VINE_AVAILABLE:
            raise ImportError(
                'ndcctools is not installed so the TaskVine executor '
                'is unavailable. See the installation instructions: '
                'https://cctools.readthedocs.io/en/stable/taskvine/#quick-start'
            )
        return TaskVineExecutor(manager_name='taskvine-manager')
