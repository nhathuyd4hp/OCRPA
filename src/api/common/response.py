from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class TResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True, description="Success flag")

    message: str = Field(default="success", description="Response message")

    data: T | None = Field(default=None, description="Response data")

    @classmethod
    def example(
        cls,
        data: Any = None,
        message: str = "success",
        description: str = "Successful Response",
        status_code: int = 200,
    ) -> dict:
        return {
            status_code: {
                "description": description,
                "content": {
                    "application/json": {
                        "example": {
                            "success": True,
                            "message": message,
                            "data": data,
                        }
                    }
                },
            },
        }
