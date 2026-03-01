# GetExerciseHistoryExerciseTemplateId200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exercise_history** | [**List[ExerciseHistoryEntry]**](ExerciseHistoryEntry.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.get_exercise_history_exercise_template_id200_response import GetExerciseHistoryExerciseTemplateId200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetExerciseHistoryExerciseTemplateId200Response from a JSON string
get_exercise_history_exercise_template_id200_response_instance = GetExerciseHistoryExerciseTemplateId200Response.from_json(json)
# print the JSON string representation of the object
print(GetExerciseHistoryExerciseTemplateId200Response.to_json())

# convert the object into a dict
get_exercise_history_exercise_template_id200_response_dict = get_exercise_history_exercise_template_id200_response_instance.to_dict()
# create an instance of GetExerciseHistoryExerciseTemplateId200Response from a dict
get_exercise_history_exercise_template_id200_response_from_dict = GetExerciseHistoryExerciseTemplateId200Response.from_dict(get_exercise_history_exercise_template_id200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


