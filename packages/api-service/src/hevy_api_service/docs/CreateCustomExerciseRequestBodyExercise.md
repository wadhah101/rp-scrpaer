# CreateCustomExerciseRequestBodyExercise


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | The title of the exercise template. | [optional] 
**exercise_type** | [**CustomExerciseType**](CustomExerciseType.md) |  | [optional] 
**equipment_category** | [**EquipmentCategory**](EquipmentCategory.md) | The equipment category of the exercise template. | [optional] 
**muscle_group** | [**MuscleGroup**](MuscleGroup.md) | The muscle group of the exercise template. | [optional] 
**other_muscles** | [**List[MuscleGroup]**](MuscleGroup.md) | The other muscles of the exercise template. | [optional] 

## Example

```python
from hevy_api_service.models.create_custom_exercise_request_body_exercise import CreateCustomExerciseRequestBodyExercise

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCustomExerciseRequestBodyExercise from a JSON string
create_custom_exercise_request_body_exercise_instance = CreateCustomExerciseRequestBodyExercise.from_json(json)
# print the JSON string representation of the object
print(CreateCustomExerciseRequestBodyExercise.to_json())

# convert the object into a dict
create_custom_exercise_request_body_exercise_dict = create_custom_exercise_request_body_exercise_instance.to_dict()
# create an instance of CreateCustomExerciseRequestBodyExercise from a dict
create_custom_exercise_request_body_exercise_from_dict = CreateCustomExerciseRequestBodyExercise.from_dict(create_custom_exercise_request_body_exercise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


