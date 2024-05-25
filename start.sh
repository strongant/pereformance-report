mkdir -p /var/www/myapp
# shellcheck disable=SC2164
cd /var/www/myapp
python -m venv venv
source venv/bin/activate
pip install pipreqs
pip install -r requirements.txt
pipreqs app.py
