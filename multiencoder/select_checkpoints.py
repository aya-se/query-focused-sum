"""
 * Copyright (c) 2021, salesforce.com, inc.
 * All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 * For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
"""
# チェックポイントのうち、最も良い性能のものを/selected_checkpointにコピーする
# Identifies best checkpoint and copies to selected_checkpoint directory

import argparse
import glob
import json
import logging
import os
import re
import shutil
from collections import defaultdict
from operator import itemgetter
from statistics import mean
import argparse
import glob
import os
import re
import json
from collections import defaultdict
from statistics import mean, stdev
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'train_dir_prefix',
        help='prefix of output directories for training runs being reported on'
    )

    args = parser.parse_args()
    filepath = args.train_dir_prefix
    sort_func = lambda x: mean([x['eval_rouge1'], x['eval_rouge2'], x['eval_rougeLsum']])
    print(f"****** {filepath} ******")
    try:
        with open(os.path.join(filepath, "trainer_state.json")) as f:
            data = json.load(f)
            epoch_logs = [log for log in data['log_history'] if 'eval_loss' in log]
            sorted_epochs = sorted(
                epoch_logs,
                key=sort_func)
            best_epoch = sorted_epochs[-1]
            best_checkpoint = f'{filepath}/checkpoint-{best_epoch["step"]}'
            if not(os.path.exists(best_checkpoint)):
                raise ValueError(f'Checkpoint {best_checkpoint} does not exist')
            print(best_epoch)
            selected_checkpoint_dir = os.path.join(filepath, 'selected_checkpoint')
            if os.path.exists(selected_checkpoint_dir):
                print('removing', selected_checkpoint_dir)
                shutil.rmtree(selected_checkpoint_dir)
            print('Copying from', best_checkpoint, 'to', selected_checkpoint_dir)
            shutil.copytree(best_checkpoint, selected_checkpoint_dir)
    except FileNotFoundError:
        pass
