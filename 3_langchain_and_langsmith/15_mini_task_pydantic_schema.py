from pydantic import BaseModel, Field
from typing import Optional, List 
from rich.console import Console
from rich.markdown import Markdown

console = Console()

class Product(BaseModel):
    product_id: int = Field(description="The unique product identifier.")
    name:str = Field(description="The name of the product.")
    description: str = Field(description="The description of the product")
    price:float = Field(description="The price of the product.")
    in_stock:bool = Field(description="Whether the product is currently in stock.")
    tags: Optional[List[str]] = Field(None, description="A list of tags associated with the product.")
try:
    add_product = Product(
        product_id=123,
        name="Samsung",
        description="Its samsung latest product",
        price=145.5,
        in_stock=True,
        tags=["samsung", "electronics","phone"]
    )
    print(add_product.model_dump_json(indent=2))
except Exception as e:
    print(f"Error creating Product instance: {e}")