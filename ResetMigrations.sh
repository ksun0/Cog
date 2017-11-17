echo ">> Deleting old migrations" 
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
echo ">> Making migrations and migrating." 
python manage.py migrate --fake Dashboard zero
python manage.py migrate --fake-initial
python manage.py makemigrations
python manage.py migrate