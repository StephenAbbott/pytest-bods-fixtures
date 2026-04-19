# pytest-bods-fixtures

A pytest plugin that exposes the canonical [bods-fixtures](https://github.com/StephenAbbott/bods-fixtures) pack as a single auto-parametrized fixture, so adapter test suites can run their pipeline against every BODS v0.4 conformance case with one line of test code.

## Why

If you write a tool that ingests, transforms, or emits [Beneficial Ownership Data Standard](https://standard.openownership.org/) statements, you want to know it handles the full shape of the standard — not just the happy path. The bods-fixtures pack provides that coverage (direct ownership, chains, circular ownership, joint control, declared-unknown UBOs, etc.). This plugin removes the parametrize boilerplate so you can drop the fixture into any test file and get one test per case.

## Install

While the project is pre-PyPI, install from the git tags directly:

```bash
pip install "bods-fixtures @ git+https://github.com/StephenAbbott/bods-fixtures.git@v0.1.0"
pip install --no-deps "pytest-bods-fixtures @ git+https://github.com/StephenAbbott/pytest-bods-fixtures.git@v0.1.0"
```

Once both are published to PyPI, this collapses to `pip install pytest-bods-fixtures` and the data pack resolves transitively.

## Use

```python
def test_my_adapter_does_not_raise(bods_fixture):
    MyAdapter().convert(bods_fixture.statements)
```

That's it. The test will run once per fixture in the pack. Failures show the fixture name in the test ID, so the offending case is obvious:

```
FAILED tests/test_adapter.py::test_my_adapter_does_not_raise[core/05-circular-ownership]
```

The `bods_fixture` parameter is a `bods_fixtures.Fixture` object exposing the same helper API the data pack ships:

```python
def test_pipeline_emits_one_party_per_entity(bods_fixture):
    entities = bods_fixture.by_record_type("entity")
    persons = bods_fixture.by_record_type("person")
    output = MyAdapter().convert(bods_fixture.statements)
    assert len(output.parties) == len(entities) + len(persons)
```

## Targeting specific cases

`bods_fixture` runs over every case. To target a subset, use pytest's standard `-k` selector:

```bash
pytest -k "circular-ownership"
```

Or write your own narrowly-scoped tests using `bods_fixtures.load(name)` directly:

```python
from bods_fixtures import load

def test_anonymous_owner_is_not_silently_dropped():
    fixture = load("core/04-anonymous-interested-party")
    output = MyAdapter().convert(fixture.statements)
    # adapter-specific assertions about the FATF-relevant signal
```

## Versioning

`pytest-bods-fixtures` pins to a `bods-fixtures` major version. Upgrading to a new minor of `bods-fixtures` (which may add fixtures) just adds new test cases to your suite. Upgrading to a new major (which may change fixture shape) requires a new major of this plugin.

## License

MIT — see [LICENSE](LICENSE).
