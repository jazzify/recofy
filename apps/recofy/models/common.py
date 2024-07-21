from django.db import models

from apps.core.models import BaseModel


class Genre(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __repr__(self) -> str:
        return f"Genre <{self.id}> {self.name=}"

    def __str__(self) -> str:
        return self.name
