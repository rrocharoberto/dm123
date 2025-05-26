pip install -r requirements.txt --upgrade -t python/
zip -r python_lib_layer.zip python/

export DEPLOY_PROFILE=deploy-profile

aws lambda publish-layer-version \
    --layer-name dm123-layer \
    --zip-file fileb://python_lib_layer.zip \
    --compatible-runtimes python3.13 \
    --profile $DEPLOY_PROFILE

