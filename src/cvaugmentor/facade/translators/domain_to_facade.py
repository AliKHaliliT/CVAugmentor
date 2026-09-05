from cvaugmentor.domain.schemas.results import ItemOutcome, JobResult
from cvaugmentor.facade.schemas import AugmentationReport, ItemReport


def domain_to_facade_item_report(outcome: ItemOutcome) -> ItemReport:

    """

    Convert a domain ItemOutcome to a facade ItemReport.

    """

    return ItemReport(source=outcome.source,
                      written=list(outcome.written),
                      skipped_reason=outcome.skipped_reason)


def domain_to_facade_augmentation_report(result: JobResult) -> AugmentationReport:

    """

    Convert a domain JobResult to a facade AugmentationReport.

    """

    return AugmentationReport(kind=result.kind,
                              mode=result.mode,
                              total_inputs=len(result.outcomes),
                              total_written=len(result.written),
                              total_skipped=len(result.skipped),
                              items=[domain_to_facade_item_report(outcome) for outcome in result.outcomes])
