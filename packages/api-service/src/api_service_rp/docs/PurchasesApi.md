# api_service_rp.PurchasesApi

All URIs are relative to *https://training.rpstrength.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**complete_purchase**](PurchasesApi.md#complete_purchase) | **POST** /purchase/complete/{id} | Complete a purchase
[**enter_referral**](PurchasesApi.md#enter_referral) | **POST** /referrals/enter/{code} | Enter a referral code
[**start_checkout**](PurchasesApi.md#start_checkout) | **POST** /purchase/checkout | Start checkout flow
[**verify_transactions**](PurchasesApi.md#verify_transactions) | **POST** /apps/training/{platform}/verifyTransactions | Verify IAP transactions


# **complete_purchase**
> complete_purchase(id, body=body)

Complete a purchase

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
    api_instance = api_service_rp.PurchasesApi(api_client)
    id = 'id_example' # str | 
    body = None # object |  (optional)

    try:
        # Complete a purchase
        await api_instance.complete_purchase(id, body=body)
    except Exception as e:
        print("Exception when calling PurchasesApi->complete_purchase: %s\n" % e)
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
**200** | Purchase completed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enter_referral**
> enter_referral(code, is_user_entry=is_user_entry, associate_only=associate_only, body=body)

Enter a referral code

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
    api_instance = api_service_rp.PurchasesApi(api_client)
    code = 'code_example' # str | 
    is_user_entry = 56 # int |  (optional)
    associate_only = 56 # int |  (optional)
    body = None # object |  (optional)

    try:
        # Enter a referral code
        await api_instance.enter_referral(code, is_user_entry=is_user_entry, associate_only=associate_only, body=body)
    except Exception as e:
        print("Exception when calling PurchasesApi->enter_referral: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**|  | 
 **is_user_entry** | **int**|  | [optional] 
 **associate_only** | **int**|  | [optional] 
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
**200** | Referral applied |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_checkout**
> start_checkout(redirect=redirect, body=body)

Start checkout flow

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
    api_instance = api_service_rp.PurchasesApi(api_client)
    redirect = 'redirect_example' # str |  (optional)
    body = None # object |  (optional)

    try:
        # Start checkout flow
        await api_instance.start_checkout(redirect=redirect, body=body)
    except Exception as e:
        print("Exception when calling PurchasesApi->start_checkout: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **redirect** | **str**|  | [optional] 
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
**200** | Checkout started |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verify_transactions**
> verify_transactions(platform, body=body)

Verify IAP transactions

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
    api_instance = api_service_rp.PurchasesApi(api_client)
    platform = 'platform_example' # str | 
    body = None # object |  (optional)

    try:
        # Verify IAP transactions
        await api_instance.verify_transactions(platform, body=body)
    except Exception as e:
        print("Exception when calling PurchasesApi->verify_transactions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform** | **str**|  | 
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
**200** | Verification result |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

