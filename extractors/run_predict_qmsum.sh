#$ -l rt_AG.small=1
#$ -l h_rt=24:00:00
#$ -o logs/predict_qmsum.out
#$ -j y
#$ -cwd

source ~/.bashrc
conda activate qfsum

NAME=relreg-qmsum

for SPLIT in \
  "val" \
  "test"
do
  OUTPUT_DIR=predicts/${NAME}/${SPLIT}

  python -u ../multiencoder/train.py \
  --test_file output-relreg-utt/${SPLIT}.csv \
  --do_predict \
  --model_name_or_path output/${NAME}/selected_checkpoint \
  --output_dir ${OUTPUT_DIR} \
  --prediction_path ${OUTPUT_DIR}/predictions.txt \
  --max_source_length 1024 \
  --generation_max_len 256 \
  --val_max_target_length 256 \
  --overwrite_output_dir \
  --per_device_eval_batch_size 4 \
  --predict_with_generate
done
