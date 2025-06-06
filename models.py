from typing import Any
from pydantic import BaseModel, Field, AliasChoices


class UserInfo(BaseModel):
    count_creations: int = Field(default=0)
    arena_id: str = Field(default=None, alias=AliasChoices("id", "arena_uuid"))
    arena_followers: int = Field(default=None, alias="followerCount")
    arena_threads: int = Field(default=None, alias="threadCount")

    twitter_handle: str = Field(default=None,
                                alias=AliasChoices("twitterHandle", "twitter_handle", "creator_twitter_handle"))
    twitter_name: str = Field(default=None, alias="twitterName")
    twitter_followers: int = Field(default=None, alias=AliasChoices("twitterFollowers", "twitter_followers"))

    user_address: str | None = Field(default=None, alias="address")
    user_address_before_migration: str | None = Field(default=None, alias="addressBeforeDynamicMigration")
    user_address_prev: str | None = Field(default=None, alias="prevAddress")
    user_address_evm: str | None = Field(default=None, alias="ethereumAddress")


class TokenInfo(BaseModel):
    number: int = Field(default=None, alias="row_id")
    creation_time: int = Field(default=None, alias="create_time")
    creation_hash: str = Field(default=None, alias="transaction_hash")
    chain_id: int = Field(default=None, alias="chain_id")
    arena_contract: str = Field(default=None, alias="contract_address")
    governor_contract: str = Field(default=None, alias="governor_contract")

    twitter_handle: str = Field(default=None, alias="creator_twitter_handle")
    creator_address: str = Field(default=None, alias="creator_address")
    twitter_followers: int = Field(default=None, alias="creator_twitter_followers")

    group_id: int = Field(default=None, alias="group_id")
    name: str = Field(default=None, alias="token_name")
    symbol: str = Field(default=None, alias="token_symbol")
    total_supply: int = Field(default=10000000000, alias="total_supply_eth")
    latest_supply: int = Field(default=10000000000, alias="latest_supply_eth")
    is_official: bool = Field(default=False, alias="is_official")
    token_contract: str = Field(default=None, alias="token_contract_address")
    curve_scaler: int = Field(default=None, alias="curve_scaler")
    lp_deployed: bool = Field(default=False, alias="lp_deployed")

    latest_total_volume: float = Field(default=0.0, alias="latest_total_volume_eth")
    latest_avax_price: float = Field(default=0.0, alias="latest_avax_price")
    latest_price_usd: float = Field(default=0.0, alias="latest_price_usd")
    market_cap_usd: float = Field(default=0.0)
    bonding_curve: float = Field(default=0.0)

    def model_post_init(self, __context: Any) -> None:
        self.market_cap_usd = self.latest_supply * self.latest_price_usd
        self.bonding_curve = (self.latest_supply / self.total_supply) * 100 if self.total_supply else 0

    def __repr__(self):
        return (
            f"🪙{self.symbol}\n"
            f"\tToken Name = {self.name!r}\n"
            f"\tToken Address = {self.token_contract!r}\n"
            f"\tMarket Cap (USD) = {self.market_cap_usd!r}\n"
            f"\tBonding Curve (%) = {self.bonding_curve!r}\n"
            f"\tCreator = {self.twitter_handle!r}\n"
            f"\tCreator Address = {self.creator_address!r}\n"
            f"\tFollowers = {self.twitter_followers!r}"
        )
