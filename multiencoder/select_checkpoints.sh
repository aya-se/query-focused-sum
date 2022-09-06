for MODEL_NAME in  \
  eli5 \
  qmsum \
  qmsum_multi \
  qmsum_from_eli5 \
  qmsum_multi_from_eli5
do
  python select_checkpoints.py output/$MODEL_NAME
done