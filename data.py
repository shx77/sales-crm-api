from datetime import datetime, timedelta
import random

SEED = 20261001
rng = random.Random(SEED)

START = datetime(2026, 9, 1, 8, 0, 0)

INDUSTRIES = [
    "SaaS", "Retail", "Healthcare",
    "Finance", "Logistics", "Manufacturing"
]

COUNTRIES = [
    "Egypt", "UAE", "Saudi Arabia",
    "Jordan", "United Kingdom"
]

REGIONS = ["North", "South", "East", "West"]

TOUCH_TYPES = [
    "Call", "Email", "Meeting", "Demo", "LinkedIn"
]

STAGES = [
    "Lead", "Qualified", "Proposal",
    "Negotiation", "Won", "Lost"
]


# -------------------------
# Sales reps
# -------------------------

sales_reps = [
    {
        "sales_rep_id": i,
        "rep_name": name,
        "region": REGIONS[(i - 1) % len(REGIONS)],
        "updated_at": (
            START + timedelta(days=i)
        ).isoformat()
    }
    for i, name in enumerate(
        [
            "Ahmed Hassan",
            "Maya Johnson",
            "Omar Ali",
            "Sara Smith",
            "Daniel Brown"
        ],
        start=1
    )
]


# -------------------------
# Accounts
# -------------------------

accounts = []

for account_id in range(1, 101):

    created = START + timedelta(
        days=rng.randint(0, 20)
    )

    accounts.append({
        "account_id": account_id,
        "account_name": f"Account {account_id:04d}",
        "industry": rng.choice(INDUSTRIES),
        "country": rng.choice(COUNTRIES),
        "created_date": created.date().isoformat(),
        "sales_rep_id": rng.randint(
            1,
            len(sales_reps)
        ),
        "updated_at": (
            created +
            timedelta(days=rng.randint(0, 10))
        ).isoformat()
    })


# -------------------------
# Deals
# -------------------------

deals = []
deal_history = []

deal_id = 1
history_id = 1

for account in accounts:

    for _ in range(rng.randint(1, 5)):

        open_dt = START + timedelta(
            days=rng.randint(0, 30)
        )

        stage = rng.choice(STAGES)

        value = round(
            rng.uniform(3000, 100000),
            2
        )

        updated = open_dt + timedelta(
            days=rng.randint(0, 20)
        )

        deal = {
            "deal_id": deal_id,
            "account_id": account["account_id"],
            "deal_name": f"Deal {deal_id:05d}",
            "stage": stage,
            "deal_value": value,
            "open_date": open_dt.date().isoformat(),
            "close_date": (
                (
                    open_dt +
                    timedelta(days=rng.randint(10, 90))
                ).date().isoformat()
                if stage in {"Won", "Lost"}
                else None
            ),
            "updated_at": updated.isoformat()
        }

        deals.append(deal)

        # Stage history
        if stage != "Lead":

            deal_history.append({
                "history_id": history_id,
                "deal_id": deal_id,
                "old_stage": "Lead",
                "new_stage": stage,
                "change_date": updated.date().isoformat(),
                "updated_at": updated.isoformat()
            })

            history_id += 1

        deal_id += 1


# -------------------------
# Touches
# -------------------------

touches = []
touch_id = 1

for account in accounts:

    for _ in range(rng.randint(5, 20)):

        touch_dt = START + timedelta(
            days=rng.randint(0, 45),
            hours=rng.randint(0, 9)
        )

        touches.append({
            "touch_id": touch_id,
            "account_id": account["account_id"],
            "touch_date": touch_dt.date().isoformat(),
            "touch_type": rng.choice(TOUCH_TYPES),
            "touch_value": round(
                rng.uniform(0, 5000),
                2
            ),
            "sales_rep_id": account["sales_rep_id"],
            "updated_at": (
                touch_dt +
                timedelta(hours=rng.randint(1, 48))
            ).isoformat()
        })

        touch_id += 1


# ==================================================
# INTENTIONAL TEST DATA
# ==================================================

# Duplicate
if touches:
    touches.append(dict(touches[0]))


# Missing account_id
touches.append({
    "touch_id": 999001,
    "account_id": None,
    "touch_date": "2026-10-01",
    "touch_type": "Call",
    "touch_value": 100,
    "sales_rep_id": 1,
    "updated_at": "2026-10-01T10:00:00"
})


# Invalid date
touches.append({
    "touch_id": 999002,
    "account_id": 1,
    "touch_date": "NOT_A_DATE",
    "touch_type": "Email",
    "touch_value": 200,
    "sales_rep_id": 1,
    "updated_at": "2026-10-01T11:00:00"
})


# Negative value
touches.append({
    "touch_id": 999003,
    "account_id": 1,
    "touch_date": "2026-10-01",
    "touch_type": "Meeting",
    "touch_value": -500,
    "sales_rep_id": 1,
    "updated_at": "2026-10-01T12:00:00"
})