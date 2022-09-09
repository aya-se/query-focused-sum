"""
 * Copyright (c) 2021, salesforce.com, inc.
 * All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 * For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
"""

import sys
import os
import csv
import json



if __name__ == "__main__":
    do_chunks = int(sys.argv[1])
    output_dir = sys.argv[2]


    totals = {"train": 1257, "val": 272, "test": 281}
    for split in ["train", "val", "test"]:
        pred_file = f"{output_dir}-{split}/predict_results_None.txt" # 修正：正しい出力先ファイル名に変更
        preds = []
        with open(pred_file) as f_pred:
            next(f_pred)
            for line in f_pred:
                score = float(line.strip().split()[-1])
                preds.append(score)

        id2meetingsrc = {}
        if do_chunks:
            fname = os.path.join(os.path.dirname( __file__ ), "..", "data", f"{split}.rouge.chunks.jsonl")
        else:
            fname = os.path.join(os.path.dirname( __file__ ), "..", "data", f'{split}-meetings.jsonl')
        with open(fname) as f:
            for line in f:
                meeting_data = json.loads(line)
                if do_chunks:
                    meeting_source = meeting_data['chunks']
                else:
                    meeting_source = meeting_data['meeting_transcripts']
                id2meetingsrc[meeting_data['meeting_id']] = meeting_source # ソース文の配列を取得
        
        fname = os.path.join(os.path.dirname( __file__ ), "..", "data", f'{split}.jsonl') # 修正：クエリ入りのデータを取得

        chunk_counter = 0
        with open(fname) as f, open(f"{output_dir}/{split}.csv", "w") as out, \
            open(f"{output_dir}/{split}.source", "w") as outs, \
            open(f"{output_dir}/{split}.target", "w") as outt, \
                open(f"{output_dir}/{split}.locator.jsonl", "w") as outl:
            writer = csv.DictWriter(out, fieldnames=["source", "query", "target"])
            writer.writeheader()
            for line in f:
                data = json.loads(line)

                meeting_utterances = id2meetingsrc[data['meeting_id']]
                cur_preds = preds[chunk_counter: chunk_counter + len(meeting_utterances)]
                chunk_counter += len(meeting_utterances)

                indices = sorted(list(range(len(cur_preds))), key = \
                    lambda x: cur_preds[x], reverse=True)
                sorted_chunks = [meeting_utterances[x] for x in indices]
                scores = [cur_preds[x] for x in indices]

                assert len(meeting_utterances) == len(indices)

                data["indices"] = indices
                data["scores"] = scores
                json.dump(data, outl)
                outl.write("\n")

                utts_ordered = [meeting_utterances[x] for x in indices]
                source = " ".join(utts_ordered)
                query = data["query"]
                target = data["answer"]
                cur_data = {"source": source, "query": query, "target": target}
                writer.writerow(cur_data)

                outs.write(source + "\n")
                outt.write(target + "\n")
