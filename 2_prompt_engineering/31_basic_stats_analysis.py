import pandas as pd
from rich.console import Console
from rich.markdown import Markdown

console = Console()

# for CSV File
# try:
#     df_results = pd.read_csv("2_prompt_engineering/29_storing_experiment_data/experiment_results.csv")
#     print(df_results.head())
#     console.print(Markdown(f"\nLoaded: {len(df_results)}"))
# except FileNotFoundError:
#     print("experiment_results.csv not found. Run batch_tester.py first.")
#     df_results = pd.DataFrame()



# for JSON File
try:
    df_results = pd.read_json("2_prompt_engineering/25_cli_batch_test_data_result/experiment_result.jsonl")
    print(df_results.head())
    console.print(Markdown(f"\nLoaded: {len(df_results)}"))
except FileNotFoundError:
    print("experiment_result.json not found. Run batch_tester.py first.")
    df_results = pd.DataFrame()