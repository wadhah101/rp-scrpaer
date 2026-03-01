# hevy_api_service.ExerciseHistoryApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_exercise_history_exercise_template_id**](ExerciseHistoryApi.md#get_exercise_history_exercise_template_id) | **GET** /v1/exercise_history/{exerciseTemplateId} | Get exercise history for a specific exercise template


# **get_exercise_history_exercise_template_id**
> GetExerciseHistoryExerciseTemplateId200Response get_exercise_history_exercise_template_id(api_key, exercise_template_id, start_date=start_date, end_date=end_date)

Get exercise history for a specific exercise template

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_exercise_history_exercise_template_id200_response import GetExerciseHistoryExerciseTemplateId200Response
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
    api_instance = hevy_api_service.ExerciseHistoryApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    exercise_template_id = 'exercise_template_id_example' # str | The id of the exercise template
    start_date = '2024-01-01T00:00:00Z' # datetime | Optional start date for filtering exercise history (ISO 8601 format) (optional)
    end_date = '2024-12-31T23:59:59Z' # datetime | Optional end date for filtering exercise history (ISO 8601 format) (optional)

    try:
        # Get exercise history for a specific exercise template
        api_response = await api_instance.get_exercise_history_exercise_template_id(api_key, exercise_template_id, start_date=start_date, end_date=end_date)
        print("The response of ExerciseHistoryApi->get_exercise_history_exercise_template_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExerciseHistoryApi->get_exercise_history_exercise_template_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **exercise_template_id** | **str**| The id of the exercise template | 
 **start_date** | **datetime**| Optional start date for filtering exercise history (ISO 8601 format) | [optional] 
 **end_date** | **datetime**| Optional end date for filtering exercise history (ISO 8601 format) | [optional] 

### Return type

[**GetExerciseHistoryExerciseTemplateId200Response**](GetExerciseHistoryExerciseTemplateId200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of exercise history entries |  -  |
**400** | Invalid request parameters or date format |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

