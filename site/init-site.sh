site=$1
pip install django
django-admin createproject $site
pushd $site
python manage.py migrate
