from typing import Dict, Iterable, List

from orats.constructs.api import data as constructs


def bounds(lower_bound, upper_bound):
    """Format bounds for API requests

    Args:
      lower_bound:
        Smallest number of days to expiration allowed.
        If not specified, no bound will be set.
      upper_bound:
        Largest number of days to expiration allowed.
        If not specified, no bound will be set.

    Returns:
      Range bounds as a comma separated pair
    """
    return ",".join(map(str, (lower_bound, upper_bound)))


def group_by_ticker(strikes: Iterable[constructs.DataApiConstruct]):
    group: Dict[str, List[constructs.DataApiConstruct]] = {}
    for item in strikes:
        value = item.ticker
        if value not in group:
            group[value] = []
        group[value].append(item)
    return group
