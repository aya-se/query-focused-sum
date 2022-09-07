#$ -l rt_AG.small=1
#$ -l h_rt=24:00:00
#$ -o logs/predict_eli5.out
#$ -j y
#$ -cwd

source ~/.bashrc
conda activate qfsum
bash scripts/predict_eli5.sh
