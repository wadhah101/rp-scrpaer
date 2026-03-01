# PostWorkoutsRequestSet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the set. | [optional] 
**weight_kg** | **float** | The weight in kilograms. | [optional] 
**reps** | **int** | The number of repetitions. | [optional] 
**distance_meters** | **int** | The distance in meters. | [optional] 
**duration_seconds** | **int** | The duration in seconds. | [optional] 
**custom_metric** | **float** | A custom metric for the set. Currently used for steps and floors. | [optional] 
**rpe** | **float** | The Rating of Perceived Exertion (RPE). | [optional] 

## Example

```python
from hevy_api_service.models.post_workouts_request_set import PostWorkoutsRequestSet

# TODO update the JSON string below
json = "{}"
# create an instance of PostWorkoutsRequestSet from a JSON string
post_workouts_request_set_instance = PostWorkoutsRequestSet.from_json(json)
# print the JSON string representation of the object
print(PostWorkoutsRequestSet.to_json())

# convert the object into a dict
post_workouts_request_set_dict = post_workouts_request_set_instance.to_dict()
# create an instance of PostWorkoutsRequestSet from a dict
post_workouts_request_set_from_dict = PostWorkoutsRequestSet.from_dict(post_workouts_request_set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


