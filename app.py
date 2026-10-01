from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from data import (
    accounts,
    sales_reps,
    deals,
    touches,
    deal_history,
    update_deal,
    create_deal,
    create_touch,
)

app = FastAPI(
    title="Sales CRM Source API",
    description=(
        "Simulated Sales CRM source system for "
        "an end-to-end Data Engineering pipeline."
    ),
    version="1.1.0",
)


def paginate(
    data,
    page: int,
    page_size: int,
    base_path: str,
    updated_since: Optional[str] = None,
):
    start = (page - 1) * page_size
    end = start + page_size

    page_data = data[start:end]

    next_url = None

    if end < len(data):
        next_page = page + 1

        next_url = (
            f"{base_path}"
            f"?page={next_page}"
            f"&page_size={page_size}"
        )

        if updated_since:
            next_url += (
                "&updated_since="
                + updated_since
            )

    return {
        "page": page,
        "page_size": page_size,
        "total_records": len(data),
        "data": page_data,
        "paging": {
            "next": next_url
        },
    }


def filter_updated_since(
    data,
    updated_since: Optional[str]
):
    if not updated_since:
        return data

    try:
        cutoff = datetime.fromisoformat(
            updated_since.replace("Z", "+00:00")
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid updated_since format. "
                "Use ISO 8601, for example: "
                "2026-10-01T00:00:00+00:00"
            ),
        )

    filtered = []

    for record in data:
        updated_at = datetime.fromisoformat(
            record["updated_at"].replace(
                "Z",
                "+00:00"
            )
        )

        if updated_at > cutoff:
            filtered.append(record)

    return filtered


class DealUpdateRequest(BaseModel):
    deal_id: int
    stage: Optional[str] = None
    deal_value: Optional[float] = None


class NewDealRequest(BaseModel):
    account_id: int
    deal_name: str
    stage: str
    deal_value: float


class NewTouchRequest(BaseModel):
    account_id: int
    touch_date: str
    touch_type: str
    touch_value: float
    sales_rep_id: int


@app.get("/")
def root():
    return {
        "service": "Sales CRM Source API",
        "version": "1.1.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/source/status")
def source_status():
    return {
        "accounts": len(accounts),
        "sales_reps": len(sales_reps),
        "deals": len(deals),
        "touches": len(touches),
        "deal_history": len(deal_history),
        "source_state": "in_memory",
    }


@app.get("/accounts")
def get_accounts(
    page: int = 1,
    page_size: int = 100,
    updated_since: Optional[str] = None,
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=400,
            detail="page_size must be greater than 0",
        )

    filtered = filter_updated_since(
        accounts,
        updated_since
    )

    return paginate(
        filtered,
        page,
        page_size,
        "/accounts",
        updated_since,
    )


@app.get("/sales-reps")
def get_sales_reps(
    page: int = 1,
    page_size: int = 100,
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=400,
            detail="page_size must be greater than 0",
        )

    return paginate(
        sales_reps,
        page,
        page_size,
        "/sales-reps",
    )


@app.get("/deals")
def get_deals(
    page: int = 1,
    page_size: int = 100,
    updated_since: Optional[str] = None,
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=400,
            detail="page_size must be greater than 0",
        )

    filtered = filter_updated_since(
        deals,
        updated_since
    )

    return paginate(
        filtered,
        page,
        page_size,
        "/deals",
        updated_since,
    )


@app.get("/touches")
def get_touches(
    page: int = 1,
    page_size: int = 100,
    updated_since: Optional[str] = None,
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=400,
            detail="page_size must be greater than 0",
        )

    filtered = filter_updated_since(
        touches,
        updated_since
    )

    return paginate(
        filtered,
        page,
        page_size,
        "/touches",
        updated_since,
    )


@app.get("/deal-history")
def get_deal_history(
    page: int = 1,
    page_size: int = 100,
    updated_since: Optional[str] = None,
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than 0",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=400,
            detail="page_size must be greater than 0",
        )

    filtered = filter_updated_since(
        deal_history,
        updated_since
    )

    return paginate(
        filtered,
        page,
        page_size,
        "/deal-history",
        updated_since,
    )


@app.post("/simulate/update-deal")
def simulate_update_deal(
    request: DealUpdateRequest
):
    updated = update_deal(
        request.deal_id,
        request.stage,
        request.deal_value,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Deal {request.deal_id} "
                "not found"
            ),
        )

    return {
        "message": "Deal updated",
        "deal": updated,
    }


@app.post("/simulate/new-deal")
def simulate_new_deal(
    request: NewDealRequest
):
    new_deal = create_deal(
        request.account_id,
        request.deal_name,
        request.stage,
        request.deal_value,
    )

    return {
        "message": "Deal created",
        "deal": new_deal,
    }


@app.post("/simulate/new-touch")
def simulate_new_touch(
    request: NewTouchRequest
):
    new_touch = create_touch(
        request.account_id,
        request.touch_date,
        request.touch_type,
        request.touch_value,
        request.sales_rep_id,
    )

    return {
        "message": "Touch created",
        "touch": new_touch,
    }


@app.get("/simulate/failure")
def simulate_failure():
    raise HTTPException(
        status_code=500,
        detail="Simulated source system failure",
    )   
