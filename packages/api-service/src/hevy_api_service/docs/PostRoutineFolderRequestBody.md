# PostRoutineFolderRequestBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**routine_folder** | [**PostRoutineFolderRequestBodyRoutineFolder**](PostRoutineFolderRequestBodyRoutineFolder.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_routine_folder_request_body import PostRoutineFolderRequestBody

# TODO update the JSON string below
json = "{}"
# create an instance of PostRoutineFolderRequestBody from a JSON string
post_routine_folder_request_body_instance = PostRoutineFolderRequestBody.from_json(json)
# print the JSON string representation of the object
print(PostRoutineFolderRequestBody.to_json())

# convert the object into a dict
post_routine_folder_request_body_dict = post_routine_folder_request_body_instance.to_dict()
# create an instance of PostRoutineFolderRequestBody from a dict
post_routine_folder_request_body_from_dict = PostRoutineFolderRequestBody.from_dict(post_routine_folder_request_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


