from typing import Optional

from fastapi import FastAPI, Query, HTTPException

from pydantic import BaseModel

from data import (
    accounts,
    sales_reps,
    deals,
    touches,
    deal_history,
)


app = FastAPI(
    title="Sales CRM Source API",
    description="Synthetic CRM source system",
    version="1.0.0"
)


def paginate(rows, page, page_size):

    start = (page - 1) * page_size
    end = start + page_size

    page_rows = rows[start:end]

    has_more = end < len(rows)

    return {
        "data": page_rows,
        "page": page,
        "page_size": page_size,
        "total": len(rows),
        "has_more": has_more,
        "next_page": page + 1 if has_more else None
    }


def filter_updated(rows, updated_since):

    if not updated_since:
        return rows

    from datetime import datetime

    cutoff = datetime.fromisoformat(
        updated_since
    )

    return [
        row
        for row in rows
        if datetime.fromisoformat(
            row["updated_at"]
        ) > cutoff
    ]


@app.get("/")
def root():

    return {
        "service": "Sales CRM Source API",
        "status": "ok",
        "docs": "/docs"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/accounts")
def get_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    updated_since: Optional[str] = None
):

    rows = filter_updated(
        accounts,
        updated_since
    )

    return paginate(
        rows,
        page,
        page_size
    )


@app.get("/sales-reps")
def get_sales_reps(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000)
):

    return paginate(
        sales_reps,
        page,
        page_size
    )


@app.get("/deals")
def get_deals(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    updated_since: Optional[str] = None
):

    rows = filter_updated(
        deals,
        updated_since
    )

    return paginate(
        rows,
        page,
        page_size
    )


@app.get("/touches")
def get_touches(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    updated_since: Optional[str] = None
):

    rows = filter_updated(
        touches,
        updated_since
    )

    return paginate(
        rows,
        page,
        page_size
    )


@app.get("/deal-history")
def get_deal_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    updated_since: Optional[str] = None
):

    rows = filter_updated(
        deal_history,
        updated_since
    )

    return paginate(
        rows,
        page,
        page_size
    )


@app.get("/simulate/failure")
def simulate_failure():

    raise HTTPException(
        status_code=500,
        detail="Simulated source-system failure"
    )

class DealUpdateRequest(BaseModel):
    deal_id: int
    stage: str | None = None
    deal_value: float | None = None


class NewDealRequest(BaseModel):
    account_id: int
    deal_name: str
    stage: str
    deal_value: float
