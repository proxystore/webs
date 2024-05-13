from __future__ import annotations

import pathlib
from concurrent.futures import Executor

from webs.executor.parsl import ParslConfig


def test_get_thread_config(tmp_path: pathlib.Path) -> None:
    run_dir = str(tmp_path / 'parsl')
    config = ParslConfig(parsl_use_threads=True, parsl_run_dir=run_dir)
    config.get_executor_config()


def test_get_process_config(tmp_path: pathlib.Path) -> None:
    run_dir = str(tmp_path / 'parsl')
    config = ParslConfig(parsl_use_threads=False, parsl_run_dir=run_dir)
    config.get_executor_config()


def test_get_executor(tmp_path: pathlib.Path) -> None:
    run_dir = str(tmp_path / 'parsl')
    config = ParslConfig(parsl_use_threads=True, parsl_run_dir=run_dir)
    executor = config.get_executor()
    assert isinstance(executor, Executor)
