# GetExerciseHistory200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exercise_history** | [**List[ExerciseHistoryEntry]**](ExerciseHistoryEntry.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.get_exercise_history200_response import GetExerciseHistory200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetExerciseHistory200Response from a JSON string
get_exercise_history200_response_instance = GetExerciseHistory200Response.from_json(json)
# print the JSON string representation of the object
print(GetExerciseHistory200Response.to_json())

# convert the object into a dict
get_exercise_history200_response_dict = get_exercise_history200_response_instance.to_dict()
# create an instance of GetExerciseHistory200Response from a dict
get_exercise_history200_response_from_dict = GetExerciseHistory200Response.from_dict(get_exercise_history200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


