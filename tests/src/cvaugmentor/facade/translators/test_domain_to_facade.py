from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from cvaugmentor.domain.schemas.results import ItemOutcome, JobResult
from cvaugmentor.facade.translators import (domain_to_facade_augmentation_report,
                                            domain_to_facade_item_report)

# The gate must reproduce on every run, so every property runs derandomized with no example
# database; free-roaming randomness stays a local exploration tool. A green property test
# claims no counterexample in its generated cases, not a proof (decision 0035).
PATHS = st.from_regex(r"[a-z0-9_]{1,8}\.(png|mp4)", fullmatch=True).map(Path)
OUTCOMES = st.builds(
    ItemOutcome,
    source=PATHS,
    written=st.lists(PATHS, max_size=4),
    skipped_reason=st.none() | st.text(max_size=20),
)
RESULTS = st.builds(
    JobResult,
    kind=st.sampled_from(["image", "video"]),
    mode=st.sampled_from(["sequential", "singular"]),
    outcomes=st.lists(OUTCOMES, max_size=5),
)


@given(outcome=OUTCOMES)
@settings(derandomize=True, database=None)
def test_property_an_item_report_carries_its_outcome_without_loss(outcome: ItemOutcome) -> None:
    report = domain_to_facade_item_report(outcome)

    assert report.source == outcome.source
    assert report.written == outcome.written
    assert report.skipped_reason == outcome.skipped_reason


@given(result=RESULTS)
@settings(derandomize=True, database=None)
def test_property_a_report_counts_and_orders_every_outcome(result: JobResult) -> None:
    report = domain_to_facade_augmentation_report(result)

    assert report.kind == result.kind
    assert report.mode == result.mode
    assert report.total_inputs == len(result.outcomes)
    assert [item.source for item in report.items] == [outcome.source for outcome in result.outcomes]


@given(result=RESULTS)
@settings(derandomize=True, database=None)
def test_property_the_written_and_skipped_totals_agree_with_the_items_they_summarise(result: JobResult) -> None:
    report = domain_to_facade_augmentation_report(result)

    assert report.total_written == sum(len(item.written) for item in report.items)
    assert report.total_skipped == sum(item.skipped_reason is not None for item in report.items)
    assert report.total_skipped <= report.total_inputs
