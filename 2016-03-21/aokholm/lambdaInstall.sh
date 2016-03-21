cd helloworld
zip -r ../helloworld.zip *
cd ..

SCRIPTPATH=`pwd -P`
FILEPATH="fileb://"$SCRIPTPATH"/helloworld.zip"

aws lambda delete-function --function-name helloworld

aws lambda create-function \
--region eu-central-1 \
--function-name helloworld \
--zip-file $FILEPATH \
--role arn:aws:iam::541147800868:role/lambda_basic_execution \
--handler hello.sweet_handler \
--runtime python2.7
