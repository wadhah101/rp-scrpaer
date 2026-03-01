# hevy_api_service.ExerciseTemplatesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_exercise_templates**](ExerciseTemplatesApi.md#get_exercise_templates) | **GET** /v1/exercise_templates | Get a paginated list of exercise templates available on the account.
[**get_exercise_templates_exercise_template_id**](ExerciseTemplatesApi.md#get_exercise_templates_exercise_template_id) | **GET** /v1/exercise_templates/{exerciseTemplateId} | Get a single exercise template by id.
[**post_exercise_templates**](ExerciseTemplatesApi.md#post_exercise_templates) | **POST** /v1/exercise_templates | Create a new custom exercise template.


# **get_exercise_templates**
> GetExerciseTemplates200Response get_exercise_templates(api_key, page=page, page_size=page_size)

Get a paginated list of exercise templates available on the account.

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_exercise_templates200_response import GetExerciseTemplates200Response
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.ExerciseTemplatesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    page = 1 # int | Page number (Must be 1 or greater) (optional) (default to 1)
    page_size = 5 # int | Number of items on the requested page (Max 100) (optional) (default to 5)

    try:
        # Get a paginated list of exercise templates available on the account.
        api_response = await api_instance.get_exercise_templates(api_key, page=page, page_size=page_size)
        print("The response of ExerciseTemplatesApi->get_exercise_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExerciseTemplatesApi->get_exercise_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **page** | **int**| Page number (Must be 1 or greater) | [optional] [default to 1]
 **page_size** | **int**| Number of items on the requested page (Max 100) | [optional] [default to 5]

### Return type

[**GetExerciseTemplates200Response**](GetExerciseTemplates200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paginated list of exercise templates |  -  |
**400** | Invalid page size |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_exercise_templates_exercise_template_id**
> ExerciseTemplate get_exercise_templates_exercise_template_id(api_key, exercise_template_id)

Get a single exercise template by id.

### Example


```python
import hevy_api_service
from hevy_api_service.models.exercise_template import ExerciseTemplate
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.ExerciseTemplatesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    exercise_template_id = 'exercise_template_id_example' # str | The id of the exercise template

    try:
        # Get a single exercise template by id.
        api_response = await api_instance.get_exercise_templates_exercise_template_id(api_key, exercise_template_id)
        print("The response of ExerciseTemplatesApi->get_exercise_templates_exercise_template_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExerciseTemplatesApi->get_exercise_templates_exercise_template_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **exercise_template_id** | **str**| The id of the exercise template | 

### Return type

[**ExerciseTemplate**](ExerciseTemplate.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Exercise template not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_exercise_templates**
> PostExerciseTemplates200Response post_exercise_templates(api_key, create_custom_exercise_request_body)

Create a new custom exercise template.

### Example


```python
import hevy_api_service
from hevy_api_service.models.create_custom_exercise_request_body import CreateCustomExerciseRequestBody
from hevy_api_service.models.post_exercise_templates200_response import PostExerciseTemplates200Response
from hevy_api_service.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = hevy_api_service.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
async with hevy_api_service.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = hevy_api_service.ExerciseTemplatesApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    create_custom_exercise_request_body = hevy_api_service.CreateCustomExerciseRequestBody() # CreateCustomExerciseRequestBody | The exercise template to create.

    try:
        # Create a new custom exercise template.
        api_response = await api_instance.post_exercise_templates(api_key, create_custom_exercise_request_body)
        print("The response of ExerciseTemplatesApi->post_exercise_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExerciseTemplatesApi->post_exercise_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **create_custom_exercise_request_body** | [**CreateCustomExerciseRequestBody**](CreateCustomExerciseRequestBody.md)| The exercise template to create. | 

### Return type

[**PostExerciseTemplates200Response**](PostExerciseTemplates200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The exercise template was successfully created |  -  |
**400** | Invalid request body |  -  |
**403** | Exceeds custom exercise limit |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

