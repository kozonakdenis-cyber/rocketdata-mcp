import os
from typing import Optional
import httpx
from fastmcp import FastMCP

ROCKETDATA_BASE_URL = os.getenv("ROCKETDATA_BASE_URL", "https://api.rocketdata.io").rstrip("/")
ROCKETDATA_TOKEN = os.environ["ROCKETDATA_TOKEN"]

mcp = FastMCP("RocketData Reviews")


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Token {ROCKETDATA_TOKEN}",
        "Accept": "application/json",
    }


async def _get(path: str, params: dict) -> dict:
    clean = {k: v for k, v in params.items() if v is not None}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{ROCKETDATA_BASE_URL}{path}",
            headers=_headers(),
            params=clean,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_companies(
    q: Optional[str] = None,
    company_ids: Optional[str] = None,
    active: Optional[bool] = True,
    page: int = 1,
    count: int = 100,
) -> dict:
    """List/search RocketData companies available to the account."""
    return await _get(
        "/public/v1/companies/",
        {
            "q": q,
            "company_ids": company_ids,
            "active": active,
            "page": page,
            "count": count,
        },
    )


@mcp.tool()
async def get_reviews(
    company_ids: Optional[str] = None,
    date_gte: Optional[str] = None,
    date_lte: Optional[str] = None,
    rating: Optional[int] = None,
    rating_type: Optional[str] = None,
    is_replied: Optional[bool] = None,
    catalog_ids: Optional[str] = None,
    without_text: Optional[bool] = None,
    per_page: int = 100,
) -> dict:
    """Get RocketData reviews with filters. rating_type can be positive, negative, or neutral."""
    return await _get(
        "/public/v4/reviews/",
        {
            "company_ids": company_ids,
            "date_gte": date_gte,
            "date_lte": date_lte,
            "rating": rating,
            "rating_type": rating_type,
            "is_replied": is_replied,
            "catalog_ids": catalog_ids,
            "without_text": without_text,
            "per_page": per_page,
        },
    )


@mcp.tool()
async def get_review_statistics(
    company_ids: Optional[str] = None,
    date_gte: Optional[str] = None,
    date_lte: Optional[str] = None,
    rating: Optional[int] = None,
    rating_type: Optional[str] = None,
    is_replied: Optional[bool] = None,
    catalog_ids: Optional[str] = None,
    without_text: Optional[bool] = None,
) -> dict:
    """Get aggregated RocketData review statistics for the selected filters."""
    return await _get(
        "/public/v4/reviews/statistic/",
        {
            "company_ids": company_ids,
            "date_gte": date_gte,
            "date_lte": date_lte,
            "rating": rating,
            "rating_type": rating_type,
            "is_replied": is_replied,
            "catalog_ids": catalog_ids,
            "without_text": without_text,
        },
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    mcp.run(transport="http", host="0.0.0.0", port=port)
