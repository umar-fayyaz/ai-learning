from langsmith import Client
from dotenv import load_dotenv
load_dotenv()

def create_gmail_dataset():
    client = Client()
    
    dataset_name = "Gmail Classification (Eval V1)" 
    
    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
        print(f"Dataset '{dataset_name}' already exists with ID: {dataset.id}")
        return 
    except (Exception):
        pass

    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="A test suite for classifying emails as Primary, Spam, or Actionable"
    )

    client.create_examples(
        inputs=[
            {"email_text": "Hi Bob, can you please send me the report by EOD Friday? Thanks, Alice."}, 
            {"email_text": "URGENT: Your account has been compromised! Click here to secure it NOW!"}, 
            {"email_text": "Hey, just checking in. Hope you have a great weekend!"}, 
            {"email_text": "Confirming your dinner reservation for 2 at The Grand Bistro tonight at 8 PM."}, 
        ],
        outputs=[
            {"expected_category": "Actionable"}, 
            {"expected_category": "Spam"}, 
            {"expected_category": "Primary"}, 
            {"expected_category": "Primary"},
        ],
        dataset_id=dataset.id, 
    )

    print(f"Created dataset '{dataset_name}' & examples added.")

if __name__ == "__main__":
    create_gmail_dataset()
