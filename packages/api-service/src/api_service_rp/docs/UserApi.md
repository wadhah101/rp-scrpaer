# api_service_rp.UserApi

All URIs are relative to *https://training.rpstrength.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_profile**](UserApi.md#get_user_profile) | **GET** /user/profile | Get user profile
[**get_user_subscriptions**](UserApi.md#get_user_subscriptions) | **GET** /user/subscriptions | Get user subscriptions
[**update_user_profile**](UserApi.md#update_user_profile) | **PUT** /user/{id} | Update user profile


# **get_user_profile**
> UserProfile get_user_profile()

Get user profile

Profile data (email, name, photo, Google/Apple/Facebook IDs, role, attributes, preferences)

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.user_profile import UserProfile
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
    api_instance = api_service_rp.UserApi(api_client)

    try:
        # Get user profile
        api_response = await api_instance.get_user_profile()
        print("The response of UserApi->get_user_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_user_profile: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserProfile**](UserProfile.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User profile |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_subscriptions**
> UserSubscriptions get_user_subscriptions()

Get user subscriptions

Active subscriptions, purchase history, Stripe customer IDs, consumed IAPs

### Example

* Bearer Authentication (BearerAuth):

```python
import api_service_rp
from api_service_rp.models.user_subscriptions import UserSubscriptions
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
    api_instance = api_service_rp.UserApi(api_client)

    try:
        # Get user subscriptions
        api_response = await api_instance.get_user_subscriptions()
        print("The response of UserApi->get_user_subscriptions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_user_subscriptions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserSubscriptions**](UserSubscriptions.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User subscriptions |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_profile**
> update_user_profile(id, body=body)

Update user profile

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
    api_instance = api_service_rp.UserApi(api_client)
    id = 'id_example' # str | 
    body = None # object |  (optional)

    try:
        # Update user profile
        await api_instance.update_user_profile(id, body=body)
    except Exception as e:
        print("Exception when calling UserApi->update_user_profile: %s\n" % e)
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
**200** | Updated user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

