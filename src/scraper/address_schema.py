from pydantic import BaseModel, Field
from typing import Optional

class AddressInfo(BaseModel):
    '''Schema for address details extracted from the site'''
    has_address : bool = Field(
        description="True if a physical location address exists in text, else False"
    )

    street_address : Optional[str] = Field(
        default = None,
        description= "Street name, house/building/suite number"
    )

    city : Optional[str] = Field(
        default = None,
        description= "district, city or town"
    )

    state_or_province : Optional[str]  = Field(
        default = None,
        description= "State, province, or Region"
    )

    country : Optional[str] = Field(
        default = None,
        description= "Country"
    )

    postal_code : Optional[str] = Field(
        default = None,
        description = "ZIP code or postal code"
    )

    full_formated_address : Optional[str] = Field(
        default = None,
        description= "Complete full formated address or single line address"
    )

