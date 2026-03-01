# GetExerciseTemplates200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** | Current page number | [optional] [default to 1]
**page_count** | **int** | Total number of pages | [optional] [default to 5]
**exercise_templates** | [**List[ExerciseTemplate]**](ExerciseTemplate.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.get_exercise_templates200_response import GetExerciseTemplates200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetExerciseTemplates200Response from a JSON string
get_exercise_templates200_response_instance = GetExerciseTemplates200Response.from_json(json)
# print the JSON string representation of the object
print(GetExerciseTemplates200Response.to_json())

# convert the object into a dict
get_exercise_templates200_response_dict = get_exercise_templates200_response_instance.to_dict()
# create an instance of GetExerciseTemplates200Response from a dict
get_exercise_templates200_response_from_dict = GetExerciseTemplates200Response.from_dict(get_exercise_templates200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


