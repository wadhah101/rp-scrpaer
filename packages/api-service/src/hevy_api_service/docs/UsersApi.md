# hevy_api_service.UsersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_info**](UsersApi.md#get_user_info) | **GET** /v1/user/info | Get user info


# **get_user_info**
> UserInfoResponse get_user_info(api_key)

Get user info

### Example


```python
import hevy_api_service
from hevy_api_service.models.user_info_response import UserInfoResponse
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
    api_instance = hevy_api_service.UsersApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Get user info
        api_response = await api_instance.get_user_info(api_key)
        print("The response of UsersApi->get_user_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 

### Return type

[**UserInfoResponse**](UserInfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The authenticated user&#39;s info |  -  |
**404** | User not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

