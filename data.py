from datetime import datetime, timedelta, timezone
import copy
import random


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SEED = 20261001

random.seed(SEED)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def utc_now():
    """
    Return the current UTC timestamp without microseconds.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def random_date(start_date, end_date):
    """
    Generate a random date between two dates.
    """
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    return (start_date + timedelta(days=random_days)).date().isoformat()


# ---------------------------------------------------------
# Reference data
# ---------------------------------------------------------

industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Retail",
    "Manufacturing",
    "Logistics",
]

countries = [
    "Egypt",
    "UAE",
    "Saudi Arabia",
    "United Kingdom",
    "United States",
]

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central",
]

stages = [
    "Lead",
    "Qualified",
    "Proposal",
    "Negotiation",
    "Won",
    "Lost",
]

touch_types = [
    "Call",
    "Email",
    "Meeting",
    "Demo",
]


# ---------------------------------------------------------
# Sales Representatives
# ---------------------------------------------------------

sales_reps = []

for rep_id in range(1, 6):

    sales_reps.append({
        "sales_rep_id": rep_id,
        "rep_name": f"Sales Rep {rep_id}",
        "region": regions[(rep_id - 1) % len(regions)],
        "updated_at": "2026-09-01T08:00:00+00:00",
    })


# ---------------------------------------------------------
# Accounts
# ---------------------------------------------------------

accounts = []

account_start = datetime(2025, 1, 1)
account_end = datetime(2026, 9, 30)

for account_id in range(1, 101):

    accounts.append({
        "account_id": account_id,
        "account_name": f"Account {account_id}",
        "industry": random.choice(industries),
        "country": random.choice(countries),
        "created_date": random_date(
            account_start,
            account_end
        ),
        "sales_rep_id": random.randint(1, 5),
        "updated_at": random_date(
            datetime(2026, 1, 1),
            datetime(2026, 9, 30)
        ) + "T08:00:00+00:00",
    })


# ---------------------------------------------------------
# Deals
# ---------------------------------------------------------

deals = []

deal_id = 1

for account in accounts:

    number_of_deals = random.randint(1, 5)

    for deal_number in range(1, number_of_deals + 1):

        open_date = datetime(
            2025,
            random.randint(1, 12),
            random.randint(1, 28)
        )

        stage = random.choice(stages)

        close_date = None

        if stage in ["Won", "Lost"]:
            close_date = (
                open_date
                + timedelta(days=random.randint(15, 180))
            ).date().isoformat()

        deals.append({
            "deal_id": deal_id,
            "account_id": account["account_id"],
            "deal_name": (
                f"Deal {deal_id} - "
                f"{account['account_name']}"
            ),
            "stage": stage,
            "deal_value": round(
                random.uniform(5000, 250000),
                2
            ),
            "open_date": open_date.date().isoformat(),
            "close_date": close_date,
            "updated_at": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 9, 30)
            ) + "T08:00:00+00:00",
        })

        deal_id += 1


# ---------------------------------------------------------
# Touches
# ---------------------------------------------------------

touches = []

touch_id = 1

for account in accounts:

    number_of_touches = random.randint(5, 20)

    for _ in range(number_of_touches):

        touches.append({
            "touch_id": touch_id,
            "account_id": account["account_id"],
            "touch_date": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 9, 30)
            ),
            "touch_type": random.choice(touch_types),
            "touch_value": round(
                random.uniform(100, 5000),
                2
            ),
            "sales_rep_id": random.randint(1, 5),
            "updated_at": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 9, 30)
            ) + "T08:00:00+00:00",
        })

        touch_id += 1


# ---------------------------------------------------------
# Intentional data-quality issues
# ---------------------------------------------------------

# 1. Duplicate touch
if len(touches) >= 2:

    duplicate_touch = copy.deepcopy(touches[0])

    duplicate_touch["touch_id"] = touches[-1]["touch_id"] + 1

    touches.append(duplicate_touch)


# 2. Missing account_id
touches.append({
    "touch_id": len(touches) + 1,
    "account_id": None,
    "touch_date": "2026-09-15",
    "touch_type": "Email",
    "touch_value": 500,
    "sales_rep_id": 1,
    "updated_at": "2026-09-15T08:00:00+00:00",
})


# 3. Invalid date
touches.append({
    "touch_id": len(touches) + 1,
    "account_id": 10,
    "touch_date": "NOT_A_DATE",
    "touch_type": "Call",
    "touch_value": 300,
    "sales_rep_id": 2,
    "updated_at": "2026-09-16T08:00:00+00:00",
})


# 4. Negative value
touches.append({
    "touch_id": len(touches) + 1,
    "account_id": 20,
    "touch_date": "2026-09-17",
    "touch_type": "Meeting",
    "touch_value": -1000,
    "sales_rep_id": 3,
    "updated_at": "2026-09-17T08:00:00+00:00",
})


# ---------------------------------------------------------
# Deal history
# ---------------------------------------------------------

deal_history = []

history_id = 1

for deal in deals:

    number_of_history_records = random.randint(1, 3)

    previous_stage = "Lead"

    for history_number in range(
        number_of_history_records
    ):

        new_stage = random.choice(stages)

        deal_history.append({
            "history_id": history_id,
            "deal_id": deal["deal_id"],
            "old_stage": previous_stage,
            "new_stage": new_stage,
            "change_date": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 9, 30)
            ),
            "updated_at": random_date(
                datetime(2026, 1, 1),
                datetime(2026, 9, 30)
            ) + "T08:00:00+00:00",
        })

        previous_stage = new_stage
        history_id += 1


# ---------------------------------------------------------
# Source-change simulation
# ---------------------------------------------------------

def update_deal(
    deal_id,
    new_stage=None,
    new_value=None
):
    """
    Update an existing deal and change updated_at.

    This simulates a CRM record being modified after
    the previous pipeline run.
    """

    for deal in deals:

        if deal["deal_id"] == deal_id:

            if new_stage is not None:
                deal["stage"] = new_stage

            if new_value is not None:
                deal["deal_value"] = new_value

            deal["updated_at"] = utc_now()

            return copy.deepcopy(deal)

    return None


def create_deal(
    account_id,
    deal_name,
    stage,
    deal_value
):
    """
    Create a new CRM deal.

    The new record receives a new ID and the current
    updated_at timestamp.
    """

    existing_ids = [
        deal["deal_id"]
        for deal in deals
    ]

    next_id = (
        max(existing_ids) + 1
        if existing_ids
        else 1
    )

    now = utc_now()

    new_deal = {
        "deal_id": next_id,
        "account_id": account_id,
        "deal_name": deal_name,
        "stage": stage,
        "deal_value": deal_value,
        "open_date": now[:10],
        "close_date": None,
        "updated_at": now,
    }

    deals.append(new_deal)

    return copy.deepcopy(new_deal)


def create_touch(
    account_id,
    touch_date,
    touch_type,
    touch_value,
    sales_rep_id
):
    """
    Create a new CRM touch.
    """

    existing_ids = [
        touch["touch_id"]
        for touch in touches
    ]

    next_id = (
        max(existing_ids) + 1
        if existing_ids
        else 1
    )

    new_touch = {
        "touch_id": next_id,
        "account_id": account_id,
        "touch_date": touch_date,
        "touch_type": touch_type,
        "touch_value": touch_value,
        "sales_rep_id": sales_rep_id,
        "updated_at": utc_now(),
    }

    touches.append(new_touch)

    return copy.deepcopy(new_touch)
