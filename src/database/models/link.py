"""A peewee-friendly model that represents a mapping between an original link and the shortened link"""

from peewee import CharField, Model

from ..database import Database


class Link(Model):
    """A peewee-friendly model that represents a mapping between an original link and the shortened link"""

    original_url = CharField(unique=True)
    short_back_half = CharField(max_length=10, unique=True)

    class Meta:
        database = Database.db

    def __str__(self):
        return str(self.short_back_half)
