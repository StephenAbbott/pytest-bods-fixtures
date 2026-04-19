"""Meta-tests for the pytest-bods-fixtures plugin.

These run a synthetic test suite via pytest's ``pytester`` fixture and
inspect the resulting test IDs / outcomes to verify the plugin behaves
as advertised.
"""

from __future__ import annotations

import pytest
from bods_fixtures import list_cases

pytest_plugins = ["pytester"]


def test_plugin_parametrizes_bods_fixture(pytester: pytest.Pytester) -> None:
    """Every case in the pack should produce one test invocation."""
    pytester.makepyfile(
        """
        def test_smoke(bods_fixture):
            assert bods_fixture.name
            assert isinstance(bods_fixture.statements, list)
            assert bods_fixture.statements
        """
    )
    result = pytester.runpytest("-v")
    expected = len(list_cases())
    result.assert_outcomes(passed=expected)


def test_test_ids_are_fixture_names(pytester: pytest.Pytester) -> None:
    """Test IDs should be the fixture names, not opaque ``bods_fixture0`` tags.

    A failing test should point at the exact fixture that broke things —
    that's the whole reason this is a generate-time hook rather than a
    ``params=`` fixture.
    """
    pytester.makepyfile(
        """
        def test_smoke(bods_fixture):
            pass
        """
    )
    result = pytester.runpytest("-v", "--collect-only", "-q")
    output = "\n".join(result.outlines)
    for case_name in list_cases():
        assert case_name in output, (
            f"expected case ID {case_name!r} in collected test list"
        )


def test_does_not_inject_fixture_when_unused(pytester: pytest.Pytester) -> None:
    """Tests that don't request ``bods_fixture`` must not be parametrized."""
    pytester.makepyfile(
        """
        def test_unrelated():
            assert 1 + 1 == 2
        """
    )
    result = pytester.runpytest("-v")
    result.assert_outcomes(passed=1)


def test_fixture_record_lookup_helpers_work(pytester: pytest.Pytester) -> None:
    """The Fixture object passed in should expose the bods-fixtures helper API."""
    pytester.makepyfile(
        """
        def test_helpers(bods_fixture):
            entities = bods_fixture.by_record_type("entity")
            persons = bods_fixture.by_record_type("person")
            relationships = bods_fixture.by_record_type("relationship")
            # Every fixture must contain at least one record of some type.
            assert entities or persons or relationships
        """
    )
    result = pytester.runpytest("-v")
    expected = len(list_cases())
    result.assert_outcomes(passed=expected)
