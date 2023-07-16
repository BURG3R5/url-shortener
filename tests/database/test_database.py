from pathlib import Path
import pytest

from src.database import Database


class TestDatabase:
    def test_initialize(self, tmp_path: Path):
        db_path = tmp_path / "test.db"

        Database.initialize(str(db_path))

        assert Database.db.get_tables() == ["link"]

        Database.terminate()

    @pytest.mark.usefixtures("pre_init_db")
    def test_set_and_fetch(self):
        original_url = "https://github.com/BURG3R5/"

        short_back_half = Database.create_short_link(original_url)
        received_url = Database.get_original_url(short_back_half)

        assert received_url == original_url

    @pytest.mark.usefixtures("pre_init_db")
    def test_fetch_fails_None(self):
        received_url = Database.get_original_url("this-link-doesnt-exist-1312")

        assert received_url is None

    # @pytest.mark.usefixtures("pre_init_db")
    def test_delete_link(self, my_short_link):
        Database.remove_link(my_short_link)

        assert Database.get_original_url(my_short_link) is None

    @pytest.mark.usefixtures("pre_init_db")
    def test_delete_fails_silently(self):
        Database.remove_link("this-link-doesnt-exist-1312")


# region FIXTURES


@pytest.fixture
def pre_init_db():
    Database.initialize(":memory:")

    yield

    Database.terminate()


@pytest.fixture
def my_short_link(pre_init_db):
    back_half = Database.create_short_link("https://github.com/BURG3R5/")

    yield back_half

    Database.remove_link(back_half)


# endregion
