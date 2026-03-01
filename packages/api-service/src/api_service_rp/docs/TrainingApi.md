# api_service_rp.TrainingApi

All URIs are relative to *https://training.rpstrength.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_day_exercise**](TrainingApi.md#add_day_exercise) | **POST** /training/days/{dayId}/exercises | Add an exercise to a training day
[**add_day_note**](TrainingApi.md#add_day_note) | **POST** /training/days/{dayId}/notes | Add a note to a training day
[**add_exercise_note**](TrainingApi.md#add_exercise_note) | **POST** /training/exercises/{exerciseId}/notes | Add a note to an exercise
[**add_meso_note**](TrainingApi.md#add_meso_note) | **POST** /training/mesocycles/{key}/notes | Add a note to a mesocycle
[**add_micro_cycle**](TrainingApi.md#add_micro_cycle) | **POST** /training/mesocycles/{key}/add-micro | Add a micro-cycle (week) to a mesocycle
[**add_sets**](TrainingApi.md#add_sets) | **POST** /training/days/{dayId}/exercises/{dayExerciseId}/sets | Add sets to an exercise
[**bulk_delete_day_exercises**](TrainingApi.md#bulk_delete_day_exercises) | **POST** /training/mesocycles/{key}/day-exercises/delete | Bulk delete exercises from mesocycle days
[**create_exercise**](TrainingApi.md#create_exercise) | **POST** /training/exercises | Create a custom exercise
[**create_mesocycle**](TrainingApi.md#create_mesocycle) | **POST** /training/mesocycles | Create a new mesocycle
[**create_template**](TrainingApi.md#create_template) | **POST** /training/templates | Create a training template
[**delete_day_note**](TrainingApi.md#delete_day_note) | **DELETE** /training/days/{dayId}/notes/{noteId} | Delete a day note
[**delete_exercise**](TrainingApi.md#delete_exercise) | **DELETE** /training/exercises/{id} | Delete a custom exercise
[**delete_exercise_note**](TrainingApi.md#delete_exercise_note) | **DELETE** /training/exercises/{exerciseId}/notes/{noteId} | Delete an exercise note
[**delete_meso_note**](TrainingApi.md#delete_meso_note) | **DELETE** /training/mesocycles/{key}/notes/{noteId} | Delete a mesocycle note
[**delete_mesocycle**](TrainingApi.md#delete_mesocycle) | **DELETE** /training/mesocycles/{key} | Delete a mesocycle
[**delete_set**](TrainingApi.md#delete_set) | **DELETE** /training/sets/{setId} | Delete a set
[**delete_template**](TrainingApi.md#delete_template) | **DELETE** /training/templates/{id} | Delete a template
[**move_day_exercise**](TrainingApi.md#move_day_exercise) | **PUT** /training/days/{dayId}/exercises/{dayExerciseId}/move | Move exercise position within a day
[**remove_micro_cycle**](TrainingApi.md#remove_micro_cycle) | **DELETE** /training/mesocycles/{key}/remove-micro | Remove a micro-cycle (week)
[**track_training**](TrainingApi.md#track_training) | **POST** /training/track | Track/log a training event
[**update_day**](TrainingApi.md#update_day) | **PUT** /training/days/{dayId} | Update a training day
[**update_day_bodyweight**](TrainingApi.md#update_day_bodyweight) | **PUT** /training/days/{dayId}/bodyweight | Update bodyweight for a day
[**update_day_exercise**](TrainingApi.md#update_day_exercise) | **PUT** /training/days/{dayId}/exercises/{dayExerciseId} | Update a day exercise
[**update_day_label**](TrainingApi.md#update_day_label) | **PUT** /training/days/{dayId}/label | Update day label
[**update_exercise**](TrainingApi.md#update_exercise) | **PUT** /training/exercises/{id} | Update an exercise
[**update_exercise_note**](TrainingApi.md#update_exercise_note) | **PUT** /training/exercises/{exerciseId}/notes/{noteId} | Update an exercise note
[**update_meso_note**](TrainingApi.md#update_meso_note) | **PUT** /training/mesocycles/{key}/notes/{noteId} | Update a mesocycle note
[**update_meso_priorities**](TrainingApi.md#update_meso_priorities) | **PUT** /training/mesocycles/{key}/priorities | Update muscle group priorities
[**update_mesocycle**](TrainingApi.md#update_mesocycle) | **PUT** /training/mesocycles/{key} | Update mesocycle metadata
[**update_set**](TrainingApi.md#update_set) | **PUT** /training/sets/{setId} | Update a set (weight, reps, etc.)
[**update_template**](TrainingApi.md#update_template) | **PUT** /training/templates/{id} | Update a template
[**update_user_attributes**](TrainingApi.md#update_user_attributes) | **POST** /training/user-attributes | Update user attributes


# **add_day_exercise**
> add_day_exercise(day_id, body=body)

Add an exercise to a training day

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Add an exercise to a training day
        await api_instance.add_day_exercise(day_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->add_day_exercise: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Added exercise |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_day_note**
> add_day_note(day_id, body=body)

Add a note to a training day

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Add a note to a training day
        await api_instance.add_day_note(day_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->add_day_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created note |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_exercise_note**
> add_exercise_note(exercise_id, body=body)

Add a note to an exercise

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    exercise_id = 'exercise_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Add a note to an exercise
        await api_instance.add_exercise_note(exercise_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->add_exercise_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exercise_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created note |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_meso_note**
> add_meso_note(key, body=body)

Add a note to a mesocycle

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    body = None # object |  (optional)

    try:
        # Add a note to a mesocycle
        await api_instance.add_meso_note(key, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->add_meso_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created note |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_micro_cycle**
> add_micro_cycle(key, body=body)

Add a micro-cycle (week) to a mesocycle

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    body = None # object |  (optional)

    try:
        # Add a micro-cycle (week) to a mesocycle
        await api_instance.add_micro_cycle(key, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->add_micro_cycle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Added micro-cycle |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_sets**
> add_sets(day_id, day_exercise_id, body=body)

Add sets to an exercise

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    day_exercise_id = 'day_exercise_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Add sets to an exercise
        await api_instance.add_sets(day_id, day_exercise_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->add_sets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **day_exercise_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Added sets |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bulk_delete_day_exercises**
> bulk_delete_day_exercises(key, body=body)

Bulk delete exercises from mesocycle days

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    body = None # object |  (optional)

    try:
        # Bulk delete exercises from mesocycle days
        await api_instance.bulk_delete_day_exercises(key, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->bulk_delete_day_exercises: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Deleted exercises |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_exercise**
> create_exercise(body=body)

Create a custom exercise

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    body = None # object |  (optional)

    try:
        # Create a custom exercise
        await api_instance.create_exercise(body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->create_exercise: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created exercise |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_mesocycle**
> create_mesocycle(body=body)

Create a new mesocycle

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    body = None # object |  (optional)

    try:
        # Create a new mesocycle
        await api_instance.create_mesocycle(body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->create_mesocycle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created mesocycle |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_template**
> create_template(body=body)

Create a training template

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    body = None # object |  (optional)

    try:
        # Create a training template
        await api_instance.create_template(body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->create_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created template |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_day_note**
> delete_day_note(day_id, note_id)

Delete a day note

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    note_id = 'note_id_example' # str | 

    try:
        # Delete a day note
        await api_instance.delete_day_note(day_id, note_id)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_day_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **note_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_exercise**
> delete_exercise(id)

Delete a custom exercise

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete a custom exercise
        await api_instance.delete_exercise(id)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_exercise: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_exercise_note**
> delete_exercise_note(exercise_id, note_id)

Delete an exercise note

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    exercise_id = 'exercise_id_example' # str | 
    note_id = 'note_id_example' # str | 

    try:
        # Delete an exercise note
        await api_instance.delete_exercise_note(exercise_id, note_id)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_exercise_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exercise_id** | **str**|  | 
 **note_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_meso_note**
> delete_meso_note(key, note_id)

Delete a mesocycle note

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    note_id = 'note_id_example' # str | 

    try:
        # Delete a mesocycle note
        await api_instance.delete_meso_note(key, note_id)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_meso_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **note_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_mesocycle**
> delete_mesocycle(key)

Delete a mesocycle

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 

    try:
        # Delete a mesocycle
        await api_instance.delete_mesocycle(key)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_mesocycle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_set**
> delete_set(set_id)

Delete a set

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    set_id = 'set_id_example' # str | 

    try:
        # Delete a set
        await api_instance.delete_set(set_id)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_set: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **set_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_template**
> delete_template(id)

Delete a template

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete a template
        await api_instance.delete_template(id)
    except Exception as e:
        print("Exception when calling TrainingApi->delete_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **move_day_exercise**
> move_day_exercise(day_id, day_exercise_id, body=body)

Move exercise position within a day

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    day_exercise_id = 'day_exercise_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Move exercise position within a day
        await api_instance.move_day_exercise(day_id, day_exercise_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->move_day_exercise: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **day_exercise_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Moved exercise |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_micro_cycle**
> remove_micro_cycle(key)

Remove a micro-cycle (week)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 

    try:
        # Remove a micro-cycle (week)
        await api_instance.remove_micro_cycle(key)
    except Exception as e:
        print("Exception when calling TrainingApi->remove_micro_cycle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Removed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **track_training**
> track_training(body=body)

Track/log a training event

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    body = None # object |  (optional)

    try:
        # Track/log a training event
        await api_instance.track_training(body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->track_training: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Tracked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_day**
> update_day(day_id, body=body)

Update a training day

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update a training day
        await api_instance.update_day(day_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_day: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated day |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_day_bodyweight**
> update_day_bodyweight(day_id, body=body)

Update bodyweight for a day

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update bodyweight for a day
        await api_instance.update_day_bodyweight(day_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_day_bodyweight: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated bodyweight |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_day_exercise**
> update_day_exercise(day_id, day_exercise_id, body=body)

Update a day exercise

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    day_exercise_id = 'day_exercise_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update a day exercise
        await api_instance.update_day_exercise(day_id, day_exercise_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_day_exercise: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **day_exercise_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated exercise |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_day_label**
> update_day_label(day_id, body=body)

Update day label

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    day_id = 'day_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update day label
        await api_instance.update_day_label(day_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_day_label: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **day_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated label |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_exercise**
> update_exercise(id, body=body)

Update an exercise

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    id = 'id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update an exercise
        await api_instance.update_exercise(id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_exercise: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated exercise |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_exercise_note**
> update_exercise_note(exercise_id, note_id, body=body)

Update an exercise note

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    exercise_id = 'exercise_id_example' # str | 
    note_id = 'note_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update an exercise note
        await api_instance.update_exercise_note(exercise_id, note_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_exercise_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **exercise_id** | **str**|  | 
 **note_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated note |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_meso_note**
> update_meso_note(key, note_id, body=body)

Update a mesocycle note

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    note_id = 'note_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update a mesocycle note
        await api_instance.update_meso_note(key, note_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_meso_note: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **note_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated note |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_meso_priorities**
> update_meso_priorities(key, body=body)

Update muscle group priorities

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    body = None # object |  (optional)

    try:
        # Update muscle group priorities
        await api_instance.update_meso_priorities(key, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_meso_priorities: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated priorities |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_mesocycle**
> update_mesocycle(key, body=body)

Update mesocycle metadata

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    key = 'key_example' # str | 
    body = None # object |  (optional)

    try:
        # Update mesocycle metadata
        await api_instance.update_mesocycle(key, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_mesocycle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated mesocycle |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_set**
> update_set(set_id, body=body)

Update a set (weight, reps, etc.)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    set_id = 'set_id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update a set (weight, reps, etc.)
        await api_instance.update_set(set_id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_set: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **set_id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated set |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_template**
> update_template(id, body=body)

Update a template

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    id = 'id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update a template
        await api_instance.update_template(id, body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated template |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_attributes**
> update_user_attributes(body=body)

Update user attributes

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://training.rpstrength.com/api
# See configuration.py for a list of all supported configuration parameters.
configuration = api_service_rp.Configuration(
    host = "https://training.rpstrength.com/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = api_service_rp.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with api_service_rp.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = api_service_rp.TrainingApi(api_client)
    body = None # object |  (optional)

    try:
        # Update user attributes
        await api_instance.update_user_attributes(body=body)
    except Exception as e:
        print("Exception when calling TrainingApi->update_user_attributes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

