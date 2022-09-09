#$ -l rt_AG.small=1
#$ -l h_rt=24:00:00
#$ -o logs/train_qmsum.out
#$ -j y
#$ -cwd

source ~/.bashrc
conda activate qfsum

NAME=relreg-qmsum

python -u ../multiencoder/train.py \
--train_file output-relreg-utt/train.csv \
--validation_file output-relreg-utt/val.csv \
--do_train \
--do_eval \
--learning_rate 0.000005 \
--model_name_or_path facebook/bart-large \
--metric_for_best_model eval_mean_rouge \
--output_dir output/${NAME} \
--per_device_train_batch_size 4 \
--max_source_length 1024 \
--generation_max_len 256 \
--val_max_target_length 256 \
--overwrite_output_dir \
--per_device_eval_batch_size 4 \
--predict_with_generate \
--evaluation_strategy epoch \
--num_train_epochs 10 \
--save_strategy epoch \
--logging_strategy epoch \
--load_best_model_at_end \
--compute_rouge_for_train True \
--fp16
