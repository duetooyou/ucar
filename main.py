import sqlite3
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Простой сервис отзывов")


# initialize database
def init_db():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


class ReviewRequest(BaseModel):
    text: str


class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str


def analyze_sentiment(text: str) -> str:
    text_lower = text.lower()

    sentiment_dict = {
        'positive': ('хорош', 'люблю'),
        'negative': ('плохо', 'ненавижу')
    }
    
    for word in sentiment_dict.get('positive'):
        if word in text_lower:
            return 'positive'
    
    for word in sentiment_dict.get('negative'):
        if word in text_lower:
            return 'negative'
    
    return 'neutral'


# health check
@app.get("/")
async def root():
    return {"message": "Простой сервис"}


@app.post("/reviews", response_model=ReviewResponse)
async def create_review(review: ReviewRequest):
    try:
        sentiment = analyze_sentiment(review.text)
        created_at = datetime.utcnow().isoformat()

        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
            (review.text, sentiment, created_at)
        )
        review_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return ReviewResponse(
            id=review_id,
            text=review.text,
            sentiment=sentiment,
            created_at=created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/reviews", response_model=List[ReviewResponse])
async def get_reviews(
        sentiment: Optional[str] = Query(None, description="Filter by sentiment: positive, negative, or neutral")):
    try:
        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()

        if sentiment:
            cursor.execute(
                'SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ? ORDER BY created_at DESC',
                (sentiment,)
            )
        else:
            cursor.execute(
                'SELECT id, text, sentiment, created_at FROM reviews ORDER BY created_at DESC'
            )

        rows = cursor.fetchall()
        conn.close()

        reviews = [
            ReviewResponse(
                id=row[0],
                text=row[1],
                sentiment=row[2],
                created_at=row[3]
            )
            for row in rows
        ]

        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
