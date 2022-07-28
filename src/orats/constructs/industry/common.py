from typing import Dict, Iterable, List

from orats.constructs.api import data as api_constructs


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


def group_by_ticker(constructs: Iterable[api_constructs.DataApiConstruct]):
    group: Dict[str, List[api_constructs.DataApiConstruct]] = {}
    for constructs in constructs:
        ticker = constructs.ticker
        if ticker not in group:
            group[ticker] = []
        group[ticker].append(constructs)
    return group
