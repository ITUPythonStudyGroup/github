#inspiration https://alestic.com/2015/11/amazon-api-gateway-aws-cli-redirect/
#base_domain=erichammond.xyz # Replace with your domain
#target_url=https://twitter.com/esh # Replace with your URL

api_name="hello world"
api_description="Test hello world python app"
resource_path=/
stage_name=dev
region=eu-central-1

#### This part is not working ####
api_id=$(aws apigateway get-rest-apis \
  --query 'items[?name==`hello world`].[id]')
echo api_id=$api_id

aws apigateway delete-rest-api \
  --rest-api-id $api_id
#### working again ####


api_id=$(aws apigateway create-rest-api \
  --region "$region" \
  --name "$api_name" \
  --description "$api_description" \
  --output text \
  --query 'id')
echo api_id=$api_id

resource_id=$(aws apigateway get-resources \
  --region "$region" \
  --rest-api-id "$api_id" \
  --output text \
  --query 'items[?path==`'$resource_path'`].[id]')
echo resource_id=$resource_id

aws apigateway put-method \
  --region "$region" \
  --rest-api-id "$api_id" \
  --resource-id "$resource_id" \
  --http-method GET \
  --authorization-type NONE \
  --no-api-key-required \
  --request-parameters '{}'
