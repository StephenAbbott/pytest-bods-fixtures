# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-04-20

### Changed
- Renamed PyPI distribution from `pytest-bods-fixtures` to
  `pytest-bods-v04-fixtures` to make the BODS version scope explicit and
  match the `bods-v04-fixtures` data pack it parametrizes over. The pytest
  fixture name (`bods_fixture`) and the Python import path
  (`pytest_bods_fixtures`) are unchanged.
- `bods-fixtures` dep retargeted at `bods-v04-fixtures>=0.1.1,<0.2` on PyPI.
- First PyPI release via trusted publishing.

## [0.1.0] - 2026-04-19

### Added
- Initial release.
- `bods_fixture` pytest fixture, auto-parametrized over every case in the
  [bods-fixtures](https://github.com/StephenAbbott/bods-fixtures) pack.
- `pytest_generate_tests` hook so test IDs are the fixture names
  (e.g. `test_x[core/01-direct-ownership]`) rather than opaque
  `[bods_fixture0]` tags.
- Registered as a pytest plugin via the `pytest11` entry point — adapters
  only need to `pip install pytest-bods-fixtures` to start using it.
