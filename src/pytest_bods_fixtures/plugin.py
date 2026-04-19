"""Pytest plugin: auto-parametrized ``bods_fixture`` over the bods-fixtures pack.

Usage in an adapter's test suite::

    def test_my_adapter_does_not_raise(bods_fixture):
        MyAdapter().convert(bods_fixture.statements)

The test runs once per fixture in the pack. Failures show the fixture name
in the test ID, so the offending case is obvious.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from bods_fixtures import list_cases, load

if TYPE_CHECKING:
    from bods_fixtures import Fixture


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrize ``bods_fixture`` across every case in the pack.

    Implemented as a generate-time hook (not a fixture with ``params=``) so
    each case becomes a distinct test ID like ``test_x[core/01-direct-ownership]``
    rather than an opaque ``[bods_fixture0]``.
    """
    if "bods_fixture" not in metafunc.fixturenames:
        return
    cases = list_cases()
    metafunc.parametrize(
        "bods_fixture",
        [load(name) for name in cases],
        ids=cases,
    )


@pytest.fixture
def bods_fixture() -> "Fixture":  # noqa: D401
    """Placeholder; the real value is supplied by ``pytest_generate_tests``.

    Defining a fixture with this name lets pytest resolve the parameter
    correctly even when no ``conftest.py`` declares it. The body is never
    executed because parametrization always overrides it.
    """
    raise RuntimeError(
        "bods_fixture must be parametrized by the pytest-bods-fixtures plugin. "
        "If you see this error, the plugin is not installed or not loaded."
    )
