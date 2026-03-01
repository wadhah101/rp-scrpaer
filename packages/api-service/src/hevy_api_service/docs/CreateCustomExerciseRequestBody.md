# CreateCustomExerciseRequestBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exercise** | [**CreateCustomExerciseRequestBodyExercise**](CreateCustomExerciseRequestBodyExercise.md) |  | 

## Example

```python
from hevy_api_service.models.create_custom_exercise_request_body import CreateCustomExerciseRequestBody

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCustomExerciseRequestBody from a JSON string
create_custom_exercise_request_body_instance = CreateCustomExerciseRequestBody.from_json(json)
# print the JSON string representation of the object
print(CreateCustomExerciseRequestBody.to_json())

# convert the object into a dict
create_custom_exercise_request_body_dict = create_custom_exercise_request_body_instance.to_dict()
# create an instance of CreateCustomExerciseRequestBody from a dict
create_custom_exercise_request_body_from_dict = CreateCustomExerciseRequestBody.from_dict(create_custom_exercise_request_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


