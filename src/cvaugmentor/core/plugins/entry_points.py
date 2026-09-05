from importlib.metadata import entry_points

from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.interfaces import IAugmentation

PLUGIN_GROUP = "cvaugmentor.augmentations"

logger = get_logger("core.plugins")


def load_entry_point_augmentations(group: str = PLUGIN_GROUP) -> list[IAugmentation]:

    """

    Discovers third-party augmentations published under an entry-point group.


    Usage
    -----
    A plugin is any installed distribution exposing an IAugmentation
    implementation (a class or a zero-argument factory) under the group.
    Discovery is fault isolated. A plugin that fails to load, fails to
    construct, or does not satisfy the IAugmentation contract is logged and
    skipped, never fatal; one broken third-party package must not take the
    pipeline down with it.
    ```python
    from cvaugmentor.core.plugins import load_entry_point_augmentations

    augmentations = load_entry_point_augmentations()
    ```


    Parameters
    ----------
    group : str, optional
        The entry-point group to scan.


    Returns
    -------
    list[IAugmentation]
        The successfully constructed augmentation implementations.


    Raises
    ------
    ValueError
        If `group` is not a non-empty string.

    """

    if not isinstance(group, str) or not group.strip():
        raise ValueError(f"group must be a non-empty string. Received: {group} with type {type(group)}")


    augmentations: list[IAugmentation] = []

    for entry_point in entry_points(group=group):
        try:
            loaded = entry_point.load()
            candidate = loaded() if callable(loaded) and not isinstance(loaded, IAugmentation) else loaded
        except Exception:
            logger.exception(f"Skipping plugin '{entry_point.name}': failed to load or construct")
            continue

        if not isinstance(candidate, IAugmentation):
            logger.warning(f"Skipping plugin '{entry_point.name}': object does not implement IAugmentation")
            continue

        augmentations.append(candidate)

    return augmentations
