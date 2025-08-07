
from langsmith import Client 
from dotenv import load_dotenv
load_dotenv()
client = Client() 

run_id = "080536bc-b8da-4af1-b14d-388c012c5e22"

client.create_feedback( 
    run_id=run_id, 
    key="user_score",  
    score=1, 
    comment="User clicked the 'looks good' button.",
    feedback_source="user",  # or "model", "heuristic", etc.
    correction=None
)   