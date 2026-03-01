# PostRoutinesRequestBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**routine** | [**PostRoutinesRequestBodyRoutine**](PostRoutinesRequestBodyRoutine.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_routines_request_body import PostRoutinesRequestBody

# TODO update the JSON string below
json = "{}"
# create an instance of PostRoutinesRequestBody from a JSON string
post_routines_request_body_instance = PostRoutinesRequestBody.from_json(json)
# print the JSON string representation of the object
print(PostRoutinesRequestBody.to_json())

# convert the object into a dict
post_routines_request_body_dict = post_routines_request_body_instance.to_dict()
# create an instance of PostRoutinesRequestBody from a dict
post_routines_request_body_from_dict = PostRoutinesRequestBody.from_dict(post_routines_request_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


