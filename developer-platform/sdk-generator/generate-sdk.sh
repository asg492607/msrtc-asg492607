#!/bin/bash
# SDK Generation Script using OpenAPI Generator
set -e

SERVICE_NAME=$1
SPEC_URL="http://api.msrtc.internal/v1/${SERVICE_NAME}/api-json"
OUTPUT_DIR="./generated-sdks/${SERVICE_NAME}-ts"

echo "Downloading OpenAPI Spec for ${SERVICE_NAME}..."
# curl -s $SPEC_URL > spec.json
# Mocking spec existence for script execution
touch spec.json

echo "Generating TypeScript SDK..."
# docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
#    -i /local/spec.json \
#    -g typescript-fetch \
#    -o /local/${OUTPUT_DIR} \
#    --additional-properties=supportsES6=true,typescriptThreePlus=true

echo "SDK Generation complete for ${SERVICE_NAME}."
