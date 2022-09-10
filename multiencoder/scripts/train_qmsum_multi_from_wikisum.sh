NAME=qmsum_multi_from_wikisum
DATA=qmsum

python -u train.py \
--train_file data/${DATA}/train.json \
--validation_file data/${DATA}/val.json \
--do_train \
--do_eval \
--learning_rate 0.000005 \
--gradient_checkpointing \
--model_name_or_path output/bart-wikisum \
--metric_for_best_model eval_mean_rouge \
--output_dir output/${NAME} \
--per_device_train_batch_size 1 \
--max_source_length 512 \
--generation_max_len 256 \
--val_max_target_length 256 \
--overwrite_output_dir \
--per_device_eval_batch_size 1 \
--multiencoder_type bart \
--multiencoder_max_num_chunks 32 \
--multiencoder_stride \
--predict_with_generate \
--evaluation_strategy epoch \
--num_train_epochs 10 \
--save_strategy epoch \
--logging_strategy epoch \
--load_best_model_at_end \
--compute_rouge_for_train True \
--fp16