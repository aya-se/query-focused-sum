NAME=qmsum_from_eli5
DATA=qmsum

for SPLIT in \
  "val" \
  "test"
do
  OUTPUT_DIR=predicts/${NAME}/${SPLIT}

  python -u train.py \
  --test_file data/${DATA}/${SPLIT}.json \
  --do_predict \
  --model_name_or_path output/${NAME}/selected_checkpoint \
  --output_dir predicts/${OUTPUT_DIR} \
  --prediction_path ${OUTPUT_DIR}/predictions.txt \
  --max_source_length 1024 \
  --generation_max_len 256 \
  --val_max_target_length 256 \
  --overwrite_output_dir \
  --per_device_eval_batch_size 1 \
  --predict_with_generate
done
