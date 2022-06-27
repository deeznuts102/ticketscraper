from pydantic import BaseModel, Extra, validator  # type: ignore
from typing import Any, List, Optional


class TotalPriceWithTransactionFee(BaseModel, extra=Extra.allow):
    id: Optional[str]
    amount: int


class AvailableListingPrice(BaseModel, extra=Extra.allow):
    totalPriceWithTransactionFee: TotalPriceWithTransactionFee


class AvailableListingNode(BaseModel, extra=Extra.allow):
    price: AvailableListingPrice


class AvailableListingEdge(BaseModel, extra=Extra.allow):
    node: AvailableListingNode
    id: Optional[str]


class AvailableListings(BaseModel, extra=Extra.allow):
    edges: List[AvailableListingEdge]


class TypeNode(BaseModel, extra=Extra.allow):
    id: str
    availableListings: AvailableListings


class TypeEdge(BaseModel, extra=Extra.allow):
    node: TypeNode


class Types(BaseModel, extra=Extra.allow):
    edges: List[TypeEdge]


class Ticket(BaseModel, extra=Extra.allow):
    id: Optional[str] = ""
    types: Types
    prices: Optional[List[float]] = []

    def __init__(self, **data: Any):
        super().__init__(**data)

        type_edges = self.types.edges
        for type_edge in type_edges:
            for listing_edge in type_edge.node.availableListings.edges:
                amount = (
                    listing_edge.node.price.totalPriceWithTransactionFee.amount / 100
                )
                self.prices.append(amount)
