# GetRoutineFolders200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** | Current page number | [optional] [default to 1]
**page_count** | **int** | Total number of pages | [optional] [default to 5]
**routine_folders** | [**List[RoutineFolder]**](RoutineFolder.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.get_routine_folders200_response import GetRoutineFolders200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetRoutineFolders200Response from a JSON string
get_routine_folders200_response_instance = GetRoutineFolders200Response.from_json(json)
# print the JSON string representation of the object
print(GetRoutineFolders200Response.to_json())

# convert the object into a dict
get_routine_folders200_response_dict = get_routine_folders200_response_instance.to_dict()
# create an instance of GetRoutineFolders200Response from a dict
get_routine_folders200_response_from_dict = GetRoutineFolders200Response.from_dict(get_routine_folders200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


