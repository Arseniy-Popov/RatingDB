npx redoc-cli bundle -o ./redoc.html spec.yaml
python swagger-yaml-to-html.py < ./spec.yaml > ./swagger.html
