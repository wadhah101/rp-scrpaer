# hevy_api_service.WorkoutsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_workouts**](WorkoutsApi.md#get_workouts) | **GET** /v1/workouts | Get a paginated list of workouts
[**get_workouts_count**](WorkoutsApi.md#get_workouts_count) | **GET** /v1/workouts/count | Get the total number of workouts on the account
[**get_workouts_events**](WorkoutsApi.md#get_workouts_events) | **GET** /v1/workouts/events | Retrieve a paged list of workout events (updates or deletes) since a given date. Events are ordered from newest to oldest. The intention is to allow clients to keep their local cache of workouts up to date without having to fetch the entire list of workouts.
[**get_workouts_workout_id**](WorkoutsApi.md#get_workouts_workout_id) | **GET** /v1/workouts/{workoutId} | Get a single workout’s complete details by the workoutId
[**post_workouts**](WorkoutsApi.md#post_workouts) | **POST** /v1/workouts | Create a new workout
[**put_workouts_workout_id**](WorkoutsApi.md#put_workouts_workout_id) | **PUT** /v1/workouts/{workoutId} | Update an existing workout


# **get_workouts**
> GetWorkouts200Response get_workouts(api_key, page=page, page_size=page_size)

Get a paginated list of workouts

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_workouts200_response import GetWorkouts200Response
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
    api_instance = hevy_api_service.WorkoutsApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    page = 1 # int | Page number (Must be 1 or greater) (optional) (default to 1)
    page_size = 5 # int | Number of items on the requested page (Max 10) (optional) (default to 5)

    try:
        # Get a paginated list of workouts
        api_response = await api_instance.get_workouts(api_key, page=page, page_size=page_size)
        print("The response of WorkoutsApi->get_workouts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->get_workouts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **page** | **int**| Page number (Must be 1 or greater) | [optional] [default to 1]
 **page_size** | **int**| Number of items on the requested page (Max 10) | [optional] [default to 5]

### Return type

[**GetWorkouts200Response**](GetWorkouts200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paginated list of workouts |  -  |
**400** | Invalid page size |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workouts_count**
> GetWorkoutsCount200Response get_workouts_count(api_key)

Get the total number of workouts on the account

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_workouts_count200_response import GetWorkoutsCount200Response
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
    api_instance = hevy_api_service.WorkoutsApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Get the total number of workouts on the account
        api_response = await api_instance.get_workouts_count(api_key)
        print("The response of WorkoutsApi->get_workouts_count:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->get_workouts_count: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 

### Return type

[**GetWorkoutsCount200Response**](GetWorkoutsCount200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The total count of workouts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workouts_events**
> PaginatedWorkoutEvents get_workouts_events(api_key, page=page, page_size=page_size, since=since)

Retrieve a paged list of workout events (updates or deletes) since a given date. Events are ordered from newest to oldest. The intention is to allow clients to keep their local cache of workouts up to date without having to fetch the entire list of workouts.

Returns a paginated array of workout events, indicating updates or deletions.

### Example


```python
import hevy_api_service
from hevy_api_service.models.paginated_workout_events import PaginatedWorkoutEvents
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
    api_instance = hevy_api_service.WorkoutsApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    page = 1 # int | Page number (Must be 1 or greater) (optional) (default to 1)
    page_size = 5 # int | Number of items on the requested page (Max 10) (optional) (default to 5)
    since = '1970-01-01T00:00:00Z' # str |  (optional) (default to '1970-01-01T00:00:00Z')

    try:
        # Retrieve a paged list of workout events (updates or deletes) since a given date. Events are ordered from newest to oldest. The intention is to allow clients to keep their local cache of workouts up to date without having to fetch the entire list of workouts.
        api_response = await api_instance.get_workouts_events(api_key, page=page, page_size=page_size, since=since)
        print("The response of WorkoutsApi->get_workouts_events:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->get_workouts_events: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **page** | **int**| Page number (Must be 1 or greater) | [optional] [default to 1]
 **page_size** | **int**| Number of items on the requested page (Max 10) | [optional] [default to 5]
 **since** | **str**|  | [optional] [default to &#39;1970-01-01T00:00:00Z&#39;]

### Return type

[**PaginatedWorkoutEvents**](PaginatedWorkoutEvents.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paginated list of workout events |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workouts_workout_id**
> Workout get_workouts_workout_id(api_key, workout_id)

Get a single workout’s complete details by the workoutId

### Example


```python
import hevy_api_service
from hevy_api_service.models.workout import Workout
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
    api_instance = hevy_api_service.WorkoutsApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    workout_id = 'workout_id_example' # str | The id of the workout

    try:
        # Get a single workout’s complete details by the workoutId
        api_response = await api_instance.get_workouts_workout_id(api_key, workout_id)
        print("The response of WorkoutsApi->get_workouts_workout_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->get_workouts_workout_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **workout_id** | **str**| The id of the workout | 

### Return type

[**Workout**](Workout.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Workout not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_workouts**
> Workout post_workouts(api_key, post_workouts_request_body)

Create a new workout

### Example


```python
import hevy_api_service
from hevy_api_service.models.post_workouts_request_body import PostWorkoutsRequestBody
from hevy_api_service.models.workout import Workout
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
    api_instance = hevy_api_service.WorkoutsApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    post_workouts_request_body = hevy_api_service.PostWorkoutsRequestBody() # PostWorkoutsRequestBody | 

    try:
        # Create a new workout
        api_response = await api_instance.post_workouts(api_key, post_workouts_request_body)
        print("The response of WorkoutsApi->post_workouts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->post_workouts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **post_workouts_request_body** | [**PostWorkoutsRequestBody**](PostWorkoutsRequestBody.md)|  | 

### Return type

[**Workout**](Workout.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The workout was successfully created |  -  |
**400** | Invalid request body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_workouts_workout_id**
> Workout put_workouts_workout_id(api_key, workout_id, post_workouts_request_body)

Update an existing workout

### Example


```python
import hevy_api_service
from hevy_api_service.models.post_workouts_request_body import PostWorkoutsRequestBody
from hevy_api_service.models.workout import Workout
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
    api_instance = hevy_api_service.WorkoutsApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    workout_id = 'workout_id_example' # str | The id of the workout
    post_workouts_request_body = hevy_api_service.PostWorkoutsRequestBody() # PostWorkoutsRequestBody | 

    try:
        # Update an existing workout
        api_response = await api_instance.put_workouts_workout_id(api_key, workout_id, post_workouts_request_body)
        print("The response of WorkoutsApi->put_workouts_workout_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->put_workouts_workout_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **workout_id** | **str**| The id of the workout | 
 **post_workouts_request_body** | [**PostWorkoutsRequestBody**](PostWorkoutsRequestBody.md)|  | 

### Return type

[**Workout**](Workout.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The workout was successfully updated |  -  |
**400** | Invalid request body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

