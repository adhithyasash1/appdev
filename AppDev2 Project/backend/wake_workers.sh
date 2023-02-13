echo "======================================================================"
echo "Welcome to the local workers setup for Minimal Kanban App"
echo "This will setup the local celery workers."
echo "Workers will be listening for tasks to be run."
echo "======================================================================"

#if [ -d ".env" ];
#then
#    echo "Enabling virtual env"
#else
#    echo "No Virtual env. Please run tools.sh first"
#    # shellcheck disable=SC2242
#    exit N
#fi

. venv/bin/activate
export ENV=development
celery -A main.celery worker -l info
deactivate
