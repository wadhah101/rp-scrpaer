# PostWorkouts400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Error message | [optional] 

## Example

```python
from hevy_api_service.models.post_workouts400_response import PostWorkouts400Response

# TODO update the JSON string below
json = "{}"
# create an instance of PostWorkouts400Response from a JSON string
post_workouts400_response_instance = PostWorkouts400Response.from_json(json)
# print the JSON string representation of the object
print(PostWorkouts400Response.to_json())

# convert the object into a dict
post_workouts400_response_dict = post_workouts400_response_instance.to_dict()
# create an instance of PostWorkouts400Response from a dict
post_workouts400_response_from_dict = PostWorkouts400Response.from_dict(post_workouts400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


