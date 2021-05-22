import json

import pandas as pd

JSON_DIR = 'manga.json'
DATA_TABLE = pd.read_json(JSON_DIR, orient='records')

def match_tokens(query_tokens, tokens):
    return list(filter(lambda token: token in query_tokens, tokens))

def serach_by_query(query_tokens):
    DATA_TABLE['matched_tokens'] = DATA_TABLE['tokens'].apply(lambda tokens: match_tokens(query_tokens, tokens))
    DATA_TABLE['matched_token_length'] = DATA_TABLE['matched_tokens'].apply(lambda tokens: len(tokens))
    match_df = DATA_TABLE[DATA_TABLE['matched_tokens'].apply(lambda r: len(r)) > 0]
    match_df.sort_values('matched_token_length', ascending=False)
    return match_df[['title', 'matched_tokens']].to_json(force_ascii=False, orient='records')

