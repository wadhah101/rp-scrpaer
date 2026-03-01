# api_service_rp.TrainingDataApi

All URIs are relative to *https://training.rpstrength.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_bootstrap**](TrainingDataApi.md#get_bootstrap) | **GET** /training/bootstrap | Get bootstrap data
[**get_exercise_history**](TrainingDataApi.md#get_exercise_history) | **GET** /training/exercises/{id}/history | Get exercise history
[**get_exercises**](TrainingDataApi.md#get_exercises) | **GET** /training/exercises | Get all exercises
[**get_mesocycle**](TrainingDataApi.md#get_mesocycle) | **GET** /training/mesocycles/{key} | Get full mesocycle detail
[**get_mesocycles**](TrainingDataApi.md#get_mesocycles) | **GET** /training/mesocycles | List all mesocycles
[**get_second_meso_meta**](TrainingDataApi.md#get_second_meso_meta) | **GET** /training/meta/second-meso | Get second mesocycle meta info
[**get_template**](TrainingDataApi.md#get_template) | **GET** /training/templates/{id} | Get a specific template
[**get_templates**](TrainingDataApi.md#get_templates) | **GET** /training/templates | Get all templates
[**get_user_exercise_history**](TrainingDataApi.md#get_user_exercise_history) | **GET** /training/user-exercise-history | Get user exercise history


# **get_bootstrap**
> object get_bootstrap()

Get bootstrap data

Full exercise catalog + all mesocycles (summary) + current mesocycle with complete weeks/days/exercises/sets (~235KB)

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
    api_instance = api_service_rp.TrainingDataApi(api_client)

    try:
        # Get bootstrap data
        api_response = await api_instance.get_bootstrap()
        print("The response of TrainingDataApi->get_bootstrap:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_bootstrap: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Bootstrap data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_exercise_history**
> List[ExerciseHistoryInner] get_exercise_history(id)

Get exercise history

Set history for a specific exercise across all mesocycles (grouped by meso, includes weight, reps, targets, week, day)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.exercise_history_inner import ExerciseHistoryInner
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
    api_instance = api_service_rp.TrainingDataApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get exercise history
        api_response = await api_instance.get_exercise_history(id)
        print("The response of TrainingDataApi->get_exercise_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_exercise_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**List[ExerciseHistoryInner]**](ExerciseHistoryInner.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Exercise history |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_exercises**
> List[Exercise] get_exercises()

Get all exercises

Full exercise catalog (315 exercises with name, muscleGroupId, youtubeId, exerciseType, mgSubType)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.exercise import Exercise
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
    api_instance = api_service_rp.TrainingDataApi(api_client)

    try:
        # Get all exercises
        api_response = await api_instance.get_exercises()
        print("The response of TrainingDataApi->get_exercises:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_exercises: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Exercise]**](Exercise.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Exercise catalog |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mesocycle**
> Mesocycle get_mesocycle(key)

Get full mesocycle detail

Full mesocycle detail (~150-185KB) - weeks > days > exercises > sets with weight, reps, targets, bodyweight, timestamps

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.mesocycle import Mesocycle
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
    api_instance = api_service_rp.TrainingDataApi(api_client)
    key = 'key_example' # str | 

    try:
        # Get full mesocycle detail
        api_response = await api_instance.get_mesocycle(key)
        print("The response of TrainingDataApi->get_mesocycle:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_mesocycle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**|  | 

### Return type

[**Mesocycle**](Mesocycle.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Full mesocycle |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mesocycles**
> List[MesocycleSummary] get_mesocycles()

List all mesocycles

List of all mesocycles (summary - id, key, name, days, weeks, unit, timestamps)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.mesocycle_summary import MesocycleSummary
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
    api_instance = api_service_rp.TrainingDataApi(api_client)

    try:
        # List all mesocycles
        api_response = await api_instance.get_mesocycles()
        print("The response of TrainingDataApi->get_mesocycles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_mesocycles: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[MesocycleSummary]**](MesocycleSummary.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Mesocycle summaries |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_second_meso_meta**
> SecondMesoMeta get_second_meso_meta()

Get second mesocycle meta info

Meta info about second mesocycle (key, startedAt)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.second_meso_meta import SecondMesoMeta
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
    api_instance = api_service_rp.TrainingDataApi(api_client)

    try:
        # Get second mesocycle meta info
        api_response = await api_instance.get_second_meso_meta()
        print("The response of TrainingDataApi->get_second_meso_meta:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_second_meso_meta: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SecondMesoMeta**](SecondMesoMeta.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Second meso meta |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_template**
> Template get_template(id)

Get a specific template

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.template import Template
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
    api_instance = api_service_rp.TrainingDataApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get a specific template
        api_response = await api_instance.get_template(id)
        print("The response of TrainingDataApi->get_template:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_template: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**Template**](Template.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Template detail |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_templates**
> List[Template] get_templates()

Get all templates

All training templates (113 templates with id, key, name, emphasis, sex, frequency)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.template import Template
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
    api_instance = api_service_rp.TrainingDataApi(api_client)

    try:
        # Get all templates
        api_response = await api_instance.get_templates()
        print("The response of TrainingDataApi->get_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_templates: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Template]**](Template.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Templates |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_exercise_history**
> Dict[str, datetime] get_user_exercise_history()

Get user exercise history

Map of exerciseId to last performed timestamp

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
    api_instance = api_service_rp.TrainingDataApi(api_client)

    try:
        # Get user exercise history
        api_response = await api_instance.get_user_exercise_history()
        print("The response of TrainingDataApi->get_user_exercise_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TrainingDataApi->get_user_exercise_history: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**Dict[str, datetime]**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Exercise history map |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

