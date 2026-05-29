import pandas as pd
from sqlalchemy import create_engine
from app.config import settings

def export_feedback():
    engine = create_engine(settings.DATABASE_URL)
    query = "SELECT message_text, decision, human_feedback FROM conversations WHERE human_feedback IS NOT NULL"
    df = pd.read_sql(query, engine)
    df.to_csv("feedback_data.csv", index=False)
    print(f"Exported {len(df)} feedback records.")

if __name__ == "__main__":
    export_feedback()