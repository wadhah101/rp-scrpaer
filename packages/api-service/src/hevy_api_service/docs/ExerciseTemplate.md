# ExerciseTemplate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The exercise template ID. | [optional] 
**title** | **str** | The exercise title. | [optional] 
**type** | **str** | The exercise type. | [optional] 
**primary_muscle_group** | **str** | The primary muscle group of the exercise. | [optional] 
**secondary_muscle_groups** | **List[str]** | The secondary muscle groups of the exercise. | [optional] 
**is_custom** | **bool** | A boolean indicating whether the exercise is a custom exercise. | [optional] 

## Example

```python
from hevy_api_service.models.exercise_template import ExerciseTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of ExerciseTemplate from a JSON string
exercise_template_instance = ExerciseTemplate.from_json(json)
# print the JSON string representation of the object
print(ExerciseTemplate.to_json())

# convert the object into a dict
exercise_template_dict = exercise_template_instance.to_dict()
# create an instance of ExerciseTemplate from a dict
exercise_template_from_dict = ExerciseTemplate.from_dict(exercise_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


