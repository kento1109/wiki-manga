import json

import pandas as pd

JSON_FILE = 'manga.json'
DATA_TABLE = pd.read_json(JSON_FILE, orient='records')
print("read data table")

def match_tokens(query_tokens, tokens):
    return list(filter(lambda token: token in query_tokens, tokens))

def serach_by_query(query_tokens):
    print(query_tokens)
    DATA_TABLE['matched_tokens'] = DATA_TABLE['tokens'].apply(lambda tokens: match_tokens(query_tokens, tokens))
    DATA_TABLE['matched_token_length'] = DATA_TABLE['matched_tokens'].apply(lambda tokens: len(tokens))
    match_df = DATA_TABLE[DATA_TABLE['matched_tokens'].apply(lambda r: len(r)) > 0]
    match_df.sort_values('matched_token_length', ascending=False, inplace=True)
    return match_df[['title', 'matched_tokens']].to_dict(orient='records')

