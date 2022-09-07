#$ -l rt_AG.small=1
#$ -l h_rt=24:00:00
#$ -o logs/train_qmsum_from_eli5.out
#$ -j y
#$ -cwd

source ~/.bashrc
conda activate qfsum
bash scripts/train_qmsum_from_eli5.sh
