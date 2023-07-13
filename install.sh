# [ -d .venv ] && echo "exists." || echo "Does not exist"

[ -d .venv ] || python3 -m venv .venv 

source .venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt 


