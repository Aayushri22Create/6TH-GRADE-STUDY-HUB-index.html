Now the backend for daily tip and progress tracking.
Action: file_editor create /app/backend/server.py --file-text "from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title=\"Sparkleway Learning API\")
api_router = APIRouter(prefix=\"/api\")

# ----- Content (server-side mirror for future personalization/AI) -----
DAILY_TIPS = [
    {\"quote\": \"Getting stuck isn't a stop sign — it's the moment right before you learn something.\",
     \"tip\": \"When your brain feels foggy, try teaching the problem out loud to a stuffed animal. Sounds silly, works magic.\",
     \"tag\": \"Grit\"},
    {\"quote\": \"You don't have to be smart. You have to be curious. Smart shows up on the way.\",
     \"tip\": \"Today, pick ONE question you're afraid to ask. Ask it. You'll be surprised how many kids had the same one.\",
     \"tag\": \"Curiosity\"},
    {\"quote\": \"Small brave steps beat one giant scary leap.\",
     \"tip\": \"Set a 10-minute timer. Do ONE tiny piece of homework. When it dings, stretch. Then decide if you want another 10.\",
     \"tag\": \"Focus\"},
    {\"quote\": \"Mistakes are your brain doing push-ups.\",
     \"tip\": \"Redo one problem you got wrong last week — from memory. Your brain will thank you (with better grades).\",
     \"tag\": \"Growth\"},
    {\"quote\": \"Reading 10 minutes a day is like giving your brain a snack.\",
     \"tip\": \"Read anything you love — comics, cereal boxes, story apps. Words are words. All of them make you smarter.\",
     \"tag\": \"Reading\"},
    {\"quote\": \"It's okay to not be a 'math person' yet. Yet is the most important word.\",
     \"tip\": \"Draw the problem. Fractions become pizza slices. Decimals become dollars and cents.\",
     \"tag\": \"Math\"},
    {\"quote\": \"You are not behind. You are exactly where your practice has taken you.\",
     \"tip\": \"Pick one topic today. Practice it 3 different ways: read it, say it, doodle it.\",
     \"tag\": \"You've got this\"},
]

TOPIC_META = [
    {\"id\": \"fractions\",   \"subject\": \"math\",    \"title\": \"Fractions\",         \"emoji\": \"🍕\", \"quiz_count\": 4},
    {\"id\": \"decimals\",    \"subject\": \"math\",    \"title\": \"Decimals\",          \"emoji\": \"💵\", \"quiz_count\": 4},
    {\"id\": \"water-cycle\", \"subject\": \"science\", \"title\": \"The Water Cycle\",   \"emoji\": \"💧\", \"quiz_count\": 4},
    {\"id\": \"cells\",       \"subject\": \"science\", \"title\": \"Cells\",             \"emoji\": \"🔬\", \"quiz_count\": 4},
    {\"id\": \"english\",     \"subject\": \"english\", \"title\": \"English Essentials\",\"emoji\": \"📚\", \"quiz_count\": 4},
]


# ----- Models -----
class Tip(BaseModel):
    quote: str
    tip: str
    tag: str
    day_index: int


class TopicSummary(BaseModel):
    id: str
    subject: str
    title: str
    emoji: str
    quiz_count: int


class ProgressCreate(BaseModel):
    session_id: str = Field(min_length=3, max_length=64)
    topic_id: str = Field(min_length=1, max_length=64)
    stars: int = Field(ge=0, le=20)
    correct: int = Field(ge=0, le=20)
    total: int = Field(ge=1, le=20)


class ProgressEntry(BaseModel):
    model_config = ConfigDict(extra=\"ignore\")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    topic_id: str
    stars: int
    correct: int
    total: int
    updated_at: str


# ----- Routes -----
@api_router.get(\"/\")
async def root():
    return {\"service\": \"sparkleway\", \"status\": \"ok\"}


@api_router.get(\"/tips/today\", response_model=Tip)
async def get_today_tip():
    day = int(datetime.now(timezone.utc).timestamp() // 86400)
    t = DAILY_TIPS[day % len(DAILY_TIPS)]
    return Tip(day_index=day, **t)


@api_router.get(\"/topics\", response_model=List[TopicSummary])
async def list_topics():
    return [TopicSummary(**t) for t in TOPIC_META]


@api_router.post(\"/progress\", response_model=ProgressEntry)
async def upsert_progress(payload: ProgressCreate):
    if payload.correct > payload.total:
        raise HTTPException(status_code=400, detail=\"correct cannot exceed total\")

    now_iso = datetime.now(timezone.utc).isoformat()
    key = {\"session_id\": payload.session_id, \"topic_id\": payload.topic_id}
    existing = await db.progress.find_one(key, {\"_id\": 0})

    stars = max(payload.stars, existing[\"stars\"]) if existing else payload.stars
    correct = max(payload.correct, existing[\"correct\"]) if existing else payload.correct

    doc = {
        \"id\": existing[\"id\"] if existing else str(uuid.uuid4()),
        \"session_id\": payload.session_id,
        \"topic_id\": payload.topic_id,
        \"stars\": stars,
        \"correct\": correct,
        \"total\": payload.total,
        \"updated_at\": now_iso,
    }
    await db.progress.update_one(key, {\"$set\": doc}, upsert=True)
    return ProgressEntry(**doc)


@api_router.get(\"/progress/{session_id}\", response_model=List[ProgressEntry])
async def list_progress(session_id: str):
    docs = await db.progress.find(
        {\"session_id\": session_id}, {\"_id\": 0}
    ).to_list(200)
    return [ProgressEntry(**d) for d in docs]


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.on_event(\"shutdown\")
async def shutdown_db_client():
    client.close()
"
Observation: Overwrite successful: /app/backend/server.py
