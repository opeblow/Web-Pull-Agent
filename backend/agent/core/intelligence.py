"""Intelligence module - handles AI reasoning and decision making."""
from typing import Optional, Any
from openai import OpenAI
from pydantic import BaseModel


class Intelligence:
    """Handles AI reasoning and decision making using OpenAI."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """Initialize intelligence with OpenAI client.
        
        Args:
            api_key: OpenAI API key.
            model: Model identifier to use.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_decision(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate AI response from prompt.
        
        Args:
            prompt: User prompt.
            system_prompt: Optional system instructions.
            temperature: Sampling temperature (0-2).
            
        Returns:
            Generated text response.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

    def structured_output(
        self,
        prompt: str,
        response_model: type[BaseModel],
        system_prompt: Optional[str] = None,
    ) -> BaseModel:
        """Generate structured output using Pydantic model.
        
        Args:
            prompt: User prompt.
            response_model: Pydantic model for response.
            system_prompt: Optional system instructions.
            
        Returns:
            Parsed response as specified model.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=response_model,
        )
        return response.choices[0].message.parsed
