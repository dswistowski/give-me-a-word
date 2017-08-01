SOURCES := $(shell find . -name '*.py' -not -path '*/\.*' -not -path './tests/*')

test:
		pytest tests

publish: lambda.zip
		aws lambda update-function-code --function-name ${FUNCTION_NAME} --zip-file fileb://dist/lambda.zip  --publish

lambda.zip: $(SOURCES) 
		rm -rf dist
		mkdir dist
		zip dist/lambda.zip $(SOURCES) 
