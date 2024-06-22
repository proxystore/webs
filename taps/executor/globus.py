from __future__ import annotations

from typing import Literal

import globus_compute_sdk
from pydantic import Field

from taps.executor.config import ExecutorConfig
from taps.executor.dag import DAGExecutor
from taps.plugins import register


@register('executor')
class GlobusComputeConfig(ExecutorConfig):
    """Globus Compute configuration.

    Attributes:
        endpoint: Globus Compute endpoint UUID.
    """

    name: Literal['globus'] = 'globus'
    endpoint: str = Field(description='endpoint UUID')
    batch_size: int = Field(
        128,
        description='maximum number of tasks to coalesce before submitting',
    )

    def get_executor(self) -> DAGExecutor:
        """Create an executor instance from the config."""
        executor = globus_compute_sdk.Executor(
            self.endpoint,
            batch_size=self.batch_size,
        )
        return DAGExecutor(executor)
