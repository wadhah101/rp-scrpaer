# ExerciseHistoryEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workout_id** | **str** | The workout ID | [optional] 
**workout_title** | **str** | The workout title | [optional] 
**workout_start_time** | **str** | ISO 8601 timestamp of when the workout was recorded to have started. | [optional] 
**workout_end_time** | **str** | ISO 8601 timestamp of when the workout was recorded to have ended. | [optional] 
**exercise_template_id** | **str** | The exercise template ID | [optional] 
**weight_kg** | **float** | The weight in kilograms | [optional] 
**reps** | **int** | The number of repetitions | [optional] 
**distance_meters** | **int** | The distance in meters | [optional] 
**duration_seconds** | **int** | The duration in seconds | [optional] 
**rpe** | **float** | The Rating of Perceived Exertion | [optional] 
**custom_metric** | **float** | A custom metric for the set | [optional] 
**set_type** | **str** | The type of set (warmup, normal, failure, dropset) | [optional] 

## Example

```python
from hevy_api_service.models.exercise_history_entry import ExerciseHistoryEntry

# TODO update the JSON string below
json = "{}"
# create an instance of ExerciseHistoryEntry from a JSON string
exercise_history_entry_instance = ExerciseHistoryEntry.from_json(json)
# print the JSON string representation of the object
print(ExerciseHistoryEntry.to_json())

# convert the object into a dict
exercise_history_entry_dict = exercise_history_entry_instance.to_dict()
# create an instance of ExerciseHistoryEntry from a dict
exercise_history_entry_from_dict = ExerciseHistoryEntry.from_dict(exercise_history_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


