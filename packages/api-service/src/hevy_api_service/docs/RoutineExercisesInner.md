# RoutineExercisesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** | Index indicating the order of the exercise in the routine. | [optional] 
**title** | **str** | Title of the exercise | [optional] 
**rest_seconds** | **str** | The rest time in seconds between sets of the exercise | [optional] 
**notes** | **str** | Routine notes on the exercise | [optional] 
**exercise_template_id** | **str** | The id of the exercise template. This can be used to fetch the exercise template. | [optional] 
**supersets_id** | **float** | The id of the superset that the exercise belongs to. A value of null indicates the exercise is not part of a superset. | [optional] 
**sets** | [**List[RoutineExercisesInnerSetsInner]**](RoutineExercisesInnerSetsInner.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.routine_exercises_inner import RoutineExercisesInner

# TODO update the JSON string below
json = "{}"
# create an instance of RoutineExercisesInner from a JSON string
routine_exercises_inner_instance = RoutineExercisesInner.from_json(json)
# print the JSON string representation of the object
print(RoutineExercisesInner.to_json())

# convert the object into a dict
routine_exercises_inner_dict = routine_exercises_inner_instance.to_dict()
# create an instance of RoutineExercisesInner from a dict
routine_exercises_inner_from_dict = RoutineExercisesInner.from_dict(routine_exercises_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


