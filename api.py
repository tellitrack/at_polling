import requests
from enum import StrEnum

from models import TokenInfo


class ArenaEndpoints(StrEnum):
    GROUPS_PLUS = "/groups_plus"
    GROUPS_PLUS_RECENT = "/rpc/groups_plus_recent"


USER_PNL_CHOICES = ["user_address", "twitter_handle"]


class ArenaAPI:
    def __init__(self):
        self.url_arena = "https://api.arena.trade"
        self.url_starsarena = "https://api.starsarena.com"
        self.chainid = 43114  # AVAX
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def get_groups_plus(self, query_key: str, value):
        groups_plus_choices = [
            "group_id",  # int
            "token_symbol",  # str
            "lp_deployed",  # str ("false", "true")
            "token_contract_address",  # str
            "creator_address",  # str
            "creator_twitter_handle"  # str
        ]

        if query_key in groups_plus_choices:
            url = f"{self.url_arena + ArenaEndpoints.GROUPS_PLUS}?{query_key}=eq.{value}"
            response = requests.get(url, headers=self.headers)
            return response.json() if response.status_code == 200 else []
        return []

    def get_groups_plus_recent(
            self, limit: int = 10, min_supply_eth: int = 0, offset: int = 0, require_photo: str = "true",
            has_twitter: bool = True
    ):
        """
        Fetch the most recently created tokens on arena.trade
        """
        creator_has_twitter = "&creator_twitter_handle=not.is.null"
        url = (
            f"{self.url_arena + ArenaEndpoints.GROUPS_PLUS_RECENT}?in_limit={limit}"
            f"&in_min_supply_eth={min_supply_eth}"
            f"&in_offset={offset}"
            f"&in_require_photo_url={require_photo}"
            f"{creator_has_twitter if has_twitter else ''}"
        )
        response = requests.get(url, headers=self.headers)
        last_tokens = [TokenInfo(**token) for token in response.json() if response.status_code == 200]
        return last_tokens if last_tokens else []
