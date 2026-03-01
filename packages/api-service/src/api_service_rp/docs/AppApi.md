# api_service_rp.AppApi

All URIs are relative to *https://training.rpstrength.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_app_config**](AppApi.md#get_app_config) | **GET** /apps/training/rp/{version}/config.json | Get app config
[**get_products**](AppApi.md#get_products) | **GET** /products.json | Get product catalog
[**get_user_review**](AppApi.md#get_user_review) | **GET** /userReview | Get user review data
[**get_web_manifest**](AppApi.md#get_web_manifest) | **GET** /training/app.webmanifest | Get PWA web manifest
[**submit_user_review**](AppApi.md#submit_user_review) | **POST** /userReview | Submit user review


# **get_app_config**
> get_app_config(version, v=v)

Get app config

App config, version changelog, feature flags, latest client version

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
    api_instance = api_service_rp.AppApi(api_client)
    version = 'version_example' # str | 
    v = 'v_example' # str |  (optional)

    try:
        # Get app config
        await api_instance.get_app_config(version, v=v)
    except Exception as e:
        print("Exception when calling AppApi->get_app_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **version** | **str**|  | 
 **v** | **str**|  | [optional] 

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
**200** | App config |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_products**
> get_products(apps=apps)

Get product catalog

Subscription product/pricing catalog (Stripe product IDs, prices, billing periods)

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
    api_instance = api_service_rp.AppApi(api_client)
    apps = 'apps_example' # str |  (optional)

    try:
        # Get product catalog
        await api_instance.get_products(apps=apps)
    except Exception as e:
        print("Exception when calling AppApi->get_products: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **apps** | **str**|  | [optional] 

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
**200** | Product catalog |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_review**
> get_user_review()

Get user review data

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
    api_instance = api_service_rp.AppApi(api_client)

    try:
        # Get user review data
        await api_instance.get_user_review()
    except Exception as e:
        print("Exception when calling AppApi->get_user_review: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**200** | User review data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_web_manifest**
> get_web_manifest(v=v)

Get PWA web manifest

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
    api_instance = api_service_rp.AppApi(api_client)
    v = 'v_example' # str |  (optional)

    try:
        # Get PWA web manifest
        await api_instance.get_web_manifest(v=v)
    except Exception as e:
        print("Exception when calling AppApi->get_web_manifest: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **v** | **str**|  | [optional] 

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
**200** | Web manifest |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_user_review**
> submit_user_review(body=body)

Submit user review

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
    api_instance = api_service_rp.AppApi(api_client)
    body = None # object |  (optional)

    try:
        # Submit user review
        await api_instance.submit_user_review(body=body)
    except Exception as e:
        print("Exception when calling AppApi->submit_user_review: %s\n" % e)
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
**200** | Review submitted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

