"""
 * Copyright (c) 2021, salesforce.com, inc.
 * All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 * For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
"""

import argparse # Python標準のargparseライブラリ
import json
from pathlib import Path

import tqdm


def main():
    parser = argparse.ArgumentParser('preprocess')
    parser.add_argument("--input_dir", type=str, help="inp directory", default="../data/") # 変換元
    parser.add_argument("--output_dir", type=str, help="out directory", default="data/qmsum/preprocessed") # 変換先
    args = parser.parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    for split in ["test", "val", "train"]:
        print(f"\nProcessing {split}")
        input_path_meetings = Path(args.input_dir, f"{split}-meetings.jsonl")
        meeting_lookup = {}
        print('Loading meetings')
        with open(input_path_meetings) as f:
            for line in tqdm.tqdm(f):
                data = json.loads(line)
                meeting_id = data['meeting_id']
                source = ' '.join(data['meeting_transcripts'])
                meeting_lookup[meeting_id] = source
        input_path = Path(args.input_dir, f"{split}.jsonl")
        output_path = Path(args.output_dir, f"{split}.jsonl")
        print('Loading queries')
        with open(input_path) as inp, \
            open(output_path, 'w') as out:
            for line in tqdm.tqdm(inp):
                data = json.loads(line)
                meeting_id = data['meeting_id']
                source = meeting_lookup[meeting_id]
                query = data['query']
                target = data['answer']
                # 1つのクエリ・参照要約に対して1つずつ対話スクリプトをコピー
                # 1つ1つのjsonが1個のモデルに対する入力となるように加工
                out.write(
                    json.dumps(
                        {
                            'source': source, # 対話スクリプトをフォーマット変換して格納
                            'query': query, # クエリ
                            'target': target # 参照要約
                        }
                    ) + '\n'
                )


if __name__ == '__main__':
    main()
