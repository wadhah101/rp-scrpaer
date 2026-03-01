# ExerciseHistorySet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**day_exercise_id** | **int** |  | [optional] 
**position** | **int** |  | [optional] 
**set_type** | **str** |  | [optional] 
**weight** | **float** |  | [optional] 
**weight_target** | **float** |  | [optional] 
**weight_target_min** | **float** |  | [optional] 
**weight_target_max** | **float** |  | [optional] 
**reps** | **int** |  | [optional] 
**reps_target** | **int** |  | [optional] 
**bodyweight** | **float** |  | [optional] 
**unit** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**finished_at** | **datetime** |  | [optional] 
**week** | **int** |  | [optional] 
**day** | **int** |  | [optional] 

## Example

```python
from api_service_rp.models.exercise_history_set import ExerciseHistorySet

# TODO update the JSON string below
json = "{}"
# create an instance of ExerciseHistorySet from a JSON string
exercise_history_set_instance = ExerciseHistorySet.from_json(json)
# print the JSON string representation of the object
print(ExerciseHistorySet.to_json())

# convert the object into a dict
exercise_history_set_dict = exercise_history_set_instance.to_dict()
# create an instance of ExerciseHistorySet from a dict
exercise_history_set_from_dict = ExerciseHistorySet.from_dict(exercise_history_set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


