cd druud && \
env SECRET_KEY=`heroku config:get SECRET_KEY --app=druud` \
    AWS_SECRET_ACCESS_KEY=`heroku config:get AWS_SECRET_ACCESS_KEY --app=druud` \
    AWS_ACCESS_KEY_ID=`heroku config:get AWS_ACCESS_KEY_ID --app=druud` \
    AWS_STORAGE_BUCKET_NAME=`heroku config:get AWS_STORAGE_BUCKET_NAME --app=druud` \
    STATIC_ROOT='/vagrant/assets' \
    /usr/bin/python manage.py collectstatic --settings=druud.settings.heroku
cd ..