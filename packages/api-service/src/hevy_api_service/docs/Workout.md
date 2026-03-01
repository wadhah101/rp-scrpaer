# Workout


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The workout ID. | [optional] 
**title** | **str** | The workout title. | [optional] 
**routine_id** | **str** | The ID of the routine that this workout belongs to. | [optional] 
**description** | **str** | The workout description. | [optional] 
**start_time** | **str** | ISO 8601 timestamp of when the workout was recorded to have started. | [optional] 
**end_time** | **str** | ISO 8601 timestamp of when the workout was recorded to have ended. | [optional] 
**updated_at** | **str** | ISO 8601 timestamp of when the workout was last updated. | [optional] 
**created_at** | **str** | ISO 8601 timestamp of when the workout was created. | [optional] 
**exercises** | [**List[WorkoutExercisesInner]**](WorkoutExercisesInner.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.workout import Workout

# TODO update the JSON string below
json = "{}"
# create an instance of Workout from a JSON string
workout_instance = Workout.from_json(json)
# print the JSON string representation of the object
print(Workout.to_json())

# convert the object into a dict
workout_dict = workout_instance.to_dict()
# create an instance of Workout from a dict
workout_from_dict = Workout.from_dict(workout_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


