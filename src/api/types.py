from typing import Any
from pydantic import AliasPath, BaseModel, Field
import humps
def to_camel(string):
    return humps.camelize(string)

class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True



class APIURI(CamelModel):
    uri: list[str] | None | str = None
    match: int | None = Field(validation_alias=AliasPath('match', 1), default=None)

class APILoginItem(CamelModel):
    username: str| None = None
    password: str| None = None
    uris: list[APIURI] | None = None
    totp: str | None = None

class APISecureNoteItem(CamelModel):
    type: int | None = Field(validation_alias=AliasPath('type', 1),default=None)

class APICardItem(CamelModel):
    cardholder_name: str | None = None
    brand: str | None = None
    number: str | None = None
    exp_month: str | None = None
    exp_year: str | None = None
    code: str | None = None

class APIIdentityItem(CamelModel):
    title: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    company: str | None = None
    country: str | None = None
    phone: str | None = None
    email: str | None = None
    ssn: str | None = None
    license_number: str | None = None
    passport_number: str | None = None
    username: str | None = None
    password: str | None = None

class APIField(CamelModel):
    name: str| None = None
    value: str| None = None
    type: int = Field(validation_alias=AliasPath('type', 1))

class APIItem(CamelModel):
    organization_id: str | None = None
    collection_ids: list[str] | None = None
    folder_id: str | None = None
    type: int
    name: str| None = None
    favorite: bool
    fields: list[APIField] | None = None
    login: APILoginItem | None = None
    secure_note: APISecureNoteItem | None = None
    card: APICardItem | None = None
    identity: APIIdentityItem | None = None
    reprompt: int
    password_history: Any = None
    organization_id: str | None = None
    collection_ids: list[str] | None = None
    notes: str | None = None
