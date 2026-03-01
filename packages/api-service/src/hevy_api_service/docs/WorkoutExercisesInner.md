# WorkoutExercisesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** | Index indicating the order of the exercise in the workout. | [optional] 
**title** | **str** | Title of the exercise | [optional] 
**notes** | **str** | Notes on the exercise | [optional] 
**exercise_template_id** | **str** | The id of the exercise template. This can be used to fetch the exercise template. | [optional] 
**supersets_id** | **float** | The id of the superset that the exercise belongs to. A value of null indicates the exercise is not part of a superset. | [optional] 
**sets** | [**List[WorkoutExercisesInnerSetsInner]**](WorkoutExercisesInnerSetsInner.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.workout_exercises_inner import WorkoutExercisesInner

# TODO update the JSON string below
json = "{}"
# create an instance of WorkoutExercisesInner from a JSON string
workout_exercises_inner_instance = WorkoutExercisesInner.from_json(json)
# print the JSON string representation of the object
print(WorkoutExercisesInner.to_json())

# convert the object into a dict
workout_exercises_inner_dict = workout_exercises_inner_instance.to_dict()
# create an instance of WorkoutExercisesInner from a dict
workout_exercises_inner_from_dict = WorkoutExercisesInner.from_dict(workout_exercises_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


