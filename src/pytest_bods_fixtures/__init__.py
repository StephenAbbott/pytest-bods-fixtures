"""Pytest plugin providing parametrized access to the bods-fixtures pack.

The plugin contributes a single pytest fixture, ``bods_fixture``, which is
auto-parametrized over every fixture in the bods-fixtures pack so that each
test runs once per fixture. Test IDs are the fixture names
(e.g. ``test_does_not_raise[core/01-direct-ownership]``), so any failure
points at the exact fixture that triggered it.
"""

VERSION = "0.1.0"
