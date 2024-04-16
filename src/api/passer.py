from enum import Enum, auto
import json
import humps
from pydantic import BaseModel

from src.api.types import APICardItem, APIIdentityItem, APIItem, APILoginItem, APISecureNoteItem


class ItemType(Enum):
    Login = auto()
    Card = auto()
    Identity = auto()
    SecureNote = auto()
    Empty = auto()

class Item(BaseModel):
    name: str | None
    item_type: ItemType
    value: APILoginItem | APICardItem | APIIdentityItem | APISecureNoteItem | None
    note: str | None
def convert_keys_to_snake_case(data):
    if isinstance(data, dict):
        return {humps.decamelize(key): convert_keys_to_snake_case(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data


def read_from_str(items_str: str) -> list[Item]:
    items = json.loads(items_str)
    api_items = [
        APIItem(**(item)) for item in items
    ]
    return api_items_to_items(api_items)

def _api_item_to_item(api_item: APIItem) -> Item:
    if api_item.login is not None:
        return Item(
            name=api_item.name,
            item_type=ItemType.Login,
            value=api_item.login,
            note = api_item.notes
        )
    elif api_item.card is not None:
        return Item(
            name=api_item.name,
            item_type=ItemType.Card,
            value=api_item.card,
            note = api_item.notes
        )
    elif api_item.identity is not None:
        return Item(
            name=api_item.name,
            item_type=ItemType.Identity,
            value=api_item.identity,
            note = api_item.notes
        )
    elif api_item.secure_note is not None:
        return Item(
            name=api_item.name,
            item_type=ItemType.SecureNote,
            value=api_item.secure_note,
            note = api_item.notes
        )
    else:
        return Item(
            name=api_item.name,
            item_type=ItemType.Empty,
            value=None,
            note = api_item.notes
        )

def api_items_to_items(items: list[APIItem]) -> list[Item]:
    return [
        _api_item_to_item(item) for item in items
    ]
