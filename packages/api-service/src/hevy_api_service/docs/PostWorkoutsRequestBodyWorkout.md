# PostWorkoutsRequestBodyWorkout


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The title of the workout. | [optional] 
**description** | **str** | A description for the workout workout. | [optional] 
**start_time** | **str** | The time the workout started. | [optional] 
**end_time** | **str** | The time the workout ended. | [optional] 
**is_private** | **bool** | A boolean indicating if the workout is private. | [optional] 
**exercises** | [**List[PostWorkoutsRequestExercise]**](PostWorkoutsRequestExercise.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.post_workouts_request_body_workout import PostWorkoutsRequestBodyWorkout

# TODO update the JSON string below
json = "{}"
# create an instance of PostWorkoutsRequestBodyWorkout from a JSON string
post_workouts_request_body_workout_instance = PostWorkoutsRequestBodyWorkout.from_json(json)
# print the JSON string representation of the object
print(PostWorkoutsRequestBodyWorkout.to_json())

# convert the object into a dict
post_workouts_request_body_workout_dict = post_workouts_request_body_workout_instance.to_dict()
# create an instance of PostWorkoutsRequestBodyWorkout from a dict
post_workouts_request_body_workout_from_dict = PostWorkoutsRequestBodyWorkout.from_dict(post_workouts_request_body_workout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


