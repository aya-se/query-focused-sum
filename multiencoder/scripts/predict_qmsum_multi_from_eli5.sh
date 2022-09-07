NAME=qmsum_multi_from_eli5
DATA=qmsum
OUTPUT_DIR=output/${NAME}/selected_checkpoint

for SPLIT in \
  "val" \
  "test"
do
  python -u train.py \
  --test_file data/${DATA}/${SPLIT}.json \
  --do_predict \
  --model_name_or_path ${OUTPUT_DIR} \
  --output_dir ${OUTPUT_DIR} \
  --prediction_path ${OUTPUT_DIR}/predictions.${SPLIT} \
  --max_source_length 512 \
  --generation_max_len 256 \
  --val_max_target_length 256 \
  --overwrite_output_dir \
  --per_device_eval_batch_size 1 \
  --multiencoder_type bart \
  --multiencoder_max_num_chunks 32 \
  --multiencoder_stride \
  --predict_with_generate
done
