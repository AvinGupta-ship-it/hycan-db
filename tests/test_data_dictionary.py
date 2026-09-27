"""Assert docs/data_dictionary.md documents the schema it claims to document.

§8.7 requires the data dictionary to be updated by the commit that changes the
schema. Nothing checked it, and it was skipped twice: schema v1.2 added
`physical_activation`, `chemical_activation` and `chemical_exfoliation` to
`synthesis_method` and `not_applicable` to `measurement_method`, and all four
appeared **zero times** in the dictionary until the commit that added this file.
The relabel migration is what made it load-bearing: it put 36 rows onto values
the dictionary said did not exist.

The manual's own lesson is that a manual step nothing checks will be skipped.
This is the check.

**The vocabularies are read off the live Pydantic model, never off a regex over
the source.** An earlier attempt in this project mined a `Literal` block with a
regex and picked up comment prose as allowed values. `MeasurementEntry` is the
authority (§0: `schema.py` outranks the manual on schema questions), so the
model is what gets introspected.
"""

from __future__ import annotations

import re
import typing
from pathlib import Path

import pytest

from hycan.schema import MeasurementEntry

REPO_ROOT = Path(__file__).resolve().parents[1]
DICTIONARY = REPO_ROOT / "docs" / "data_dictionary.md"


def _literal_values(annotation: object) -> tuple[str, ...] | None:
    """Return a field's Literal values, seeing through Optional[...]."""
    if typing.get_origin(annotation) is typing.Literal:
        return typing.get_args(annotation)
    for arg in typing.get_args(annotation):
        if arg is type(None):
            continue
        if typing.get_origin(arg) is typing.Literal:
            return typing.get_args(arg)
    return None


def vocabulary_fields() -> dict[str, tuple[str, ...]]:
    return {
        name: values
        for name, field in MeasurementEntry.model_fields.items()
        if (values := _literal_values(field.annotation)) is not None
    }


def dictionary_text() -> str:
    return DICTIONARY.read_text(encoding="utf-8")


def backticked_tokens(text: str) -> set[str]:
    return set(re.findall(r"`([^`\n]+)`", text))


def test_the_dictionary_exists_and_the_model_has_vocabularies():
    """Guards the two tests below against passing on an empty input.

    MUTATION: rename the dictionary, or make _literal_values always return None
    -> the tests below would pass vacuously. This fails.
    """
    assert DICTIONARY.is_file()
    fields = vocabulary_fields()
    assert len(fields) >= 14, f"only found {len(fields)} vocabulary fields"
    assert "synthesis_method" in fields
    assert "chemical_activation" in fields["synthesis_method"]


@pytest.mark.parametrize("field", sorted(vocabulary_fields()))
def test_every_vocabulary_field_has_a_section_in_the_dictionary(field):
    """MUTATION: add a Literal field to the model without documenting it ->
    this fails for that field."""
    headings = re.findall(r"^#{2,4}\s+(.*)$", dictionary_text(), flags=re.M)
    named = {
        name
        for heading in headings
        for name in re.findall(r"`([a-z0-9_]+)`", heading)
    }
    assert field in named, (
        f"{field} is a controlled vocabulary in MeasurementEntry with no "
        f"section in docs/data_dictionary.md (§8.7)"
    )


@pytest.mark.parametrize("field", sorted(vocabulary_fields()))
def test_every_allowed_value_appears_in_the_dictionary(field):
    """The check that would have caught all four values v1.2 left undocumented.

    Document-wide rather than per-section on purpose: a field's values are
    sometimes documented in a later version's section (v1.3 documented
    `surface_area_method`'s three additions in a second section 580 lines below
    the first), and a per-section rule would fail on that correct arrangement.
    Document-wide has no false positives against the current file and would have
    caught every real omission, because all four missing values appeared nowhere
    at all.

    MUTATION: add a value to any Literal in schema.py without adding it to
    docs/data_dictionary.md -> this fails for that field.
    """
    documented = backticked_tokens(dictionary_text())
    missing = [v for v in vocabulary_fields()[field] if v not in documented]
    assert not missing, (
        f"{field} allows {missing}, which appear nowhere in "
        f"docs/data_dictionary.md (§8.7 requires the dictionary to be updated "
        f"by the commit that changes the schema)"
    )
