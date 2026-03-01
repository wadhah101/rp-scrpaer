# ExerciseHistoryInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Mesocycle name | [optional] 
**key** | **str** | Mesocycle key | [optional] 
**set_groups** | **List[List[ExerciseHistorySet]]** |  | [optional] 

## Example

```python
from api_service_rp.models.exercise_history_inner import ExerciseHistoryInner

# TODO update the JSON string below
json = "{}"
# create an instance of ExerciseHistoryInner from a JSON string
exercise_history_inner_instance = ExerciseHistoryInner.from_json(json)
# print the JSON string representation of the object
print(ExerciseHistoryInner.to_json())

# convert the object into a dict
exercise_history_inner_dict = exercise_history_inner_instance.to_dict()
# create an instance of ExerciseHistoryInner from a dict
exercise_history_inner_from_dict = ExerciseHistoryInner.from_dict(exercise_history_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


