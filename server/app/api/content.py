import random
from fastapi import APIRouter, Query
from typing import List
from app.database import database

all_names = set(entry["name"] for entry in database)

router = APIRouter()


@router.get("/content")
async def get_content(seen: str = ""):
    print("Received request for content with seen names:", seen)
    # Parse seen names from query param
    seen_names = set(name.strip() for name in seen.split(",") if name.strip())
    # Compute unseen names
    unseen_names = all_names - seen_names
    seen_all = False
    if unseen_names:
        # Pick a random unseen name
        chosen_name = random.choice(list(unseen_names))
    else:
        # All have been seen, pick any
        last_seen_name = [name.strip() for name in seen.split(",") if name.strip()][-1]
        selectable_names = all_names - {last_seen_name}
        chosen_name = random.choice(list(selectable_names))
        seen_all = True
    # Find the entry for the chosen name
    print(f'Returning {chosen_name} from database')
    entry = next(e for e in database if e["name"] == chosen_name)
    # Add seen_all to the response
    response = dict(entry)
    response["seen_all"] = seen_all
    return response
