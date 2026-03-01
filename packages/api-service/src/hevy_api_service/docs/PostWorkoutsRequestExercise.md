# PostWorkoutsRequestExercise


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exercise_template_id** | **str** | The ID of the exercise template. | [optional] 
**superset_id** | **int** | The ID of the superset. | [optional] 
**notes** | **str** | Additional notes for the exercise. | [optional] 
**sets** | [**List[PostWorkoutsRequestSet]**](PostWorkoutsRequestSet.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_workouts_request_exercise import PostWorkoutsRequestExercise

# TODO update the JSON string below
json = "{}"
# create an instance of PostWorkoutsRequestExercise from a JSON string
post_workouts_request_exercise_instance = PostWorkoutsRequestExercise.from_json(json)
# print the JSON string representation of the object
print(PostWorkoutsRequestExercise.to_json())

# convert the object into a dict
post_workouts_request_exercise_dict = post_workouts_request_exercise_instance.to_dict()
# create an instance of PostWorkoutsRequestExercise from a dict
post_workouts_request_exercise_from_dict = PostWorkoutsRequestExercise.from_dict(post_workouts_request_exercise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


