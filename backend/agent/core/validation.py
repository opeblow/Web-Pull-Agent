"""Validation module - handles data validation."""
from typing import Any, Callable
from pydantic import BaseModel, ValidationError
import json


class ValidationSchema:
    """Handles data validation using Pydantic schemas."""

    def __init__(self):
        """Initialize empty schema registry."""
        self.schemas: dict[str, type[BaseModel]] = {}

    def register_schema(self, name: str, schema: type[BaseModel]) -> None:
        """Register a validation schema.
        
        Args:
            name: Schema identifier.
            schema: Pydantic model class.
        """
        self.schemas[name] = schema

    def validate(self, data: Any, schema_name: str) -> BaseModel:
        """Validate data against a registered schema.
        
        Args:
            data: Data to validate.
            schema_name: Name of registered schema.
            
        Returns:
            Validated Pydantic model.
            
        Raises:
            ValueError: If schema not found.
            ValidationError: If validation fails.
        """
        if schema_name not in self.schemas:
            raise ValueError(f"Schema '{schema_name}' not found.")

        schema = self.schemas[schema_name]

        try:
            if isinstance(data, dict):
                validated = schema(**data)
            elif isinstance(data, str):
                data_dict = json.loads(data)
                validated = schema(**data_dict)
            elif isinstance(data, schema):
                validated = data
            else:
                raise ValueError(f"Cannot validate data of type {type(data)}")
            return validated
        except ValidationError as e:
            raise e
