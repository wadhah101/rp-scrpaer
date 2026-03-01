# CreateWorkout400Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Error message | [optional] 

## Example

```python
from hevy_api_service.models.create_workout400_response import CreateWorkout400Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWorkout400Response from a JSON string
create_workout400_response_instance = CreateWorkout400Response.from_json(json)
# print the JSON string representation of the object
print(CreateWorkout400Response.to_json())

# convert the object into a dict
create_workout400_response_dict = create_workout400_response_instance.to_dict()
# create an instance of CreateWorkout400Response from a dict
create_workout400_response_from_dict = CreateWorkout400Response.from_dict(create_workout400_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


