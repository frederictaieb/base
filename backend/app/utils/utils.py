from typing import List, Dict, Any
import json

def parse_memo(memos: List[dict]) -> Dict[str, Any]:
    """
    Parse a list of XRPL memos and return a merged dictionary of all memo data.
    Each memo is expected to be a dict with a 'Memo' key containing 'MemoData' in hex.
    """
    report = {}
    if memos and len(memos) > 0:
        for memo in memos:
            memo_data_hex = memo.get("Memo", {}).get("MemoData")
            if memo_data_hex:
                try:
                    # Decode hex to utf-8 string
                    memo_data_json = bytes.fromhex(memo_data_hex).decode("utf-8")
                    # Parse JSON string to dict
                    memo_data_object = json.loads(memo_data_json)
                    # Merge into report
                    report.update(memo_data_object)
                except Exception as e:
                    print(f"Error decoding memo: {e}")
            else:
                print("No MemoData found.")
        return report
    else:
        print("No memos found in the transaction.")
        return report