"""Defines the ASGI app that is the URL shortener"""

from typing import Annotated
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from src.database import Database

app = FastAPI()


@app.post("/shorten", status_code=201)
def shorten(original_url: Annotated[str, Body(embed=True)]):
    """Create a shortened link and return the back half/endpoint"""

    endpoint = Database.create_short_link(original_url)
    return {"endpoint": endpoint}


@app.get("/{back_half}", status_code=307)
def redirect(back_half: str):
    """Redirects to the original URL, if found"""

    original_url = Database.get_original_url(back_half)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(original_url)


@app.get("/{back_half}/+")
def display(back_half: str):
    """Returns (not redirects) to the original URL, if found"""

    original_url = Database.get_original_url(back_half)
    if original_url is None:
        return {"message": f"{back_half} is not registered with us"}
    return {"original_url": original_url}


if __name__ == "__main__":
    Database.initialize("database/url_shortener.db")
