from fastapi import Request
from starlette.responses import RedirectResponse


async def index(request: Request):
    """
    Index page just redirects to login page.
    """
    return RedirectResponse(url=request.url_for("login"))
