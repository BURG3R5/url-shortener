"""Contains the `Database` singleton which wraps a connection to the database"""

from peewee import SqliteDatabase

from ..utils.random_string import generate_random_string


class Database:
    """Singleton that holds the methods to connect to the database"""

    db = SqliteDatabase(None)

    @classmethod
    def initialize(cls, db_path: str):
        """Creates and connects to an SQLite database at the given path"""
        from .models.link import Link

        cls.db.init(db_path)
        cls.db.connect()
        cls.db.create_tables([Link])

    @classmethod
    def create_short_link(cls, original_url: str) -> str:
        """Creates a new Link and returns the shortened link"""
        from .models.link import Link

        short_back_half = generate_random_string(10)

        Link.create(
            original_url=original_url,
            short_back_half=short_back_half,
        )

        return short_back_half

    @classmethod
    def get_original_url(cls, short_back_half: str) -> str | None:
        """Returns whether original url for given back half"""
        from .models.link import Link

        try:
            link = Link.get(short_back_half=short_back_half)
            return link.original_url
        except Link.DoesNotExist:  # type: ignore
            return None

    @classmethod
    def remove_link(cls, short_back_half: str):
        """Finds and deletes link with given back half"""
        from .models.link import Link

        link = Link.get_or_none(short_back_half=short_back_half)
        if link:
            link.delete_instance()

    @classmethod
    def terminate(cls):
        """Closes the connection to the database"""

        cls.db.close()
