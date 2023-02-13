echo "======================================================================"
echo "Welcome to the local beat setup for Minimal Kanban App"
echo "This will setup the local celery beat scheduler."
echo "Interval scheduled tasks for Minimal Kanban will be run by this."
echo "======================================================================"

#if [ -d "venv" ];
#then
#    echo "Enabling virtual env"
#else
#    echo "No Virtual env. Please do the required configuration"
#    # shellcheck disable=SC2242
#    exit N
#fi

# export ENV=development gets read at main.py inside create_app(), can change it to any environment we want
# Activate virtual env

. venv/bin/activate
export ENV=development
celery -A main.celery beat --max-interval 1 -l info
deactivate