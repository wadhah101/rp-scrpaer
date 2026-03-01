# PostWorkoutsRequestBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workout** | [**PostWorkoutsRequestBodyWorkout**](PostWorkoutsRequestBodyWorkout.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_workouts_request_body import PostWorkoutsRequestBody

# TODO update the JSON string below
json = "{}"
# create an instance of PostWorkoutsRequestBody from a JSON string
post_workouts_request_body_instance = PostWorkoutsRequestBody.from_json(json)
# print the JSON string representation of the object
print(PostWorkoutsRequestBody.to_json())

# convert the object into a dict
post_workouts_request_body_dict = post_workouts_request_body_instance.to_dict()
# create an instance of PostWorkoutsRequestBody from a dict
post_workouts_request_body_from_dict = PostWorkoutsRequestBody.from_dict(post_workouts_request_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


