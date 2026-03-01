# hevy_api_service.RoutineFoldersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_routine_folders**](RoutineFoldersApi.md#get_routine_folders) | **GET** /v1/routine_folders | Get a paginated list of routine folders available on the account.
[**get_routine_folders_folder_id**](RoutineFoldersApi.md#get_routine_folders_folder_id) | **GET** /v1/routine_folders/{folderId} | Get a single routine folder by id.
[**post_routine_folders**](RoutineFoldersApi.md#post_routine_folders) | **POST** /v1/routine_folders | Create a new routine folder. The folder will be created at index 0, and all other folders will have their indexes incremented.


# **get_routine_folders**
> GetRoutineFolders200Response get_routine_folders(api_key, page=page, page_size=page_size)

Get a paginated list of routine folders available on the account.

### Example


```python
import hevy_api_service
from hevy_api_service.models.get_routine_folders200_response import GetRoutineFolders200Response
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
    api_instance = hevy_api_service.RoutineFoldersApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    page = 1 # int | Page number (Must be 1 or greater) (optional) (default to 1)
    page_size = 5 # int | Number of items on the requested page (Max 10) (optional) (default to 5)

    try:
        # Get a paginated list of routine folders available on the account.
        api_response = await api_instance.get_routine_folders(api_key, page=page, page_size=page_size)
        print("The response of RoutineFoldersApi->get_routine_folders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutineFoldersApi->get_routine_folders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **page** | **int**| Page number (Must be 1 or greater) | [optional] [default to 1]
 **page_size** | **int**| Number of items on the requested page (Max 10) | [optional] [default to 5]

### Return type

[**GetRoutineFolders200Response**](GetRoutineFolders200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paginated list of routine folders |  -  |
**400** | Invalid page size |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_routine_folders_folder_id**
> RoutineFolder get_routine_folders_folder_id(api_key, folder_id)

Get a single routine folder by id.

### Example


```python
import hevy_api_service
from hevy_api_service.models.routine_folder import RoutineFolder
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
    api_instance = hevy_api_service.RoutineFoldersApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    folder_id = 'folder_id_example' # str | The id of the routine folder

    try:
        # Get a single routine folder by id.
        api_response = await api_instance.get_routine_folders_folder_id(api_key, folder_id)
        print("The response of RoutineFoldersApi->get_routine_folders_folder_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutineFoldersApi->get_routine_folders_folder_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **folder_id** | **str**| The id of the routine folder | 

### Return type

[**RoutineFolder**](RoutineFolder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**404** | Routine folder not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_routine_folders**
> RoutineFolder post_routine_folders(api_key, post_routine_folder_request_body)

Create a new routine folder. The folder will be created at index 0, and all other folders will have their indexes incremented.

### Example


```python
import hevy_api_service
from hevy_api_service.models.post_routine_folder_request_body import PostRoutineFolderRequestBody
from hevy_api_service.models.routine_folder import RoutineFolder
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
    api_instance = hevy_api_service.RoutineFoldersApi(api_client)
    api_key = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    post_routine_folder_request_body = hevy_api_service.PostRoutineFolderRequestBody() # PostRoutineFolderRequestBody | 

    try:
        # Create a new routine folder. The folder will be created at index 0, and all other folders will have their indexes incremented.
        api_response = await api_instance.post_routine_folders(api_key, post_routine_folder_request_body)
        print("The response of RoutineFoldersApi->post_routine_folders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RoutineFoldersApi->post_routine_folders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **UUID**|  | 
 **post_routine_folder_request_body** | [**PostRoutineFolderRequestBody**](PostRoutineFolderRequestBody.md)|  | 

### Return type

[**RoutineFolder**](RoutineFolder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The routine folder was successfully created |  -  |
**400** | Invalid request body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

