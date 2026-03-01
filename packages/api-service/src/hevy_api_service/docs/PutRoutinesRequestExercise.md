# PutRoutinesRequestExercise


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exercise_template_id** | **str** | The ID of the exercise template. | [optional] 
**superset_id** | **int** | The ID of the superset. | [optional] 
**rest_seconds** | **int** | The rest time in seconds. | [optional] 
**notes** | **str** | Additional notes for the exercise. | [optional] 
**sets** | [**List[PutRoutinesRequestSet]**](PutRoutinesRequestSet.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.put_routines_request_exercise import PutRoutinesRequestExercise

# TODO update the JSON string below
json = "{}"
# create an instance of PutRoutinesRequestExercise from a JSON string
put_routines_request_exercise_instance = PutRoutinesRequestExercise.from_json(json)
# print the JSON string representation of the object
print(PutRoutinesRequestExercise.to_json())

# convert the object into a dict
put_routines_request_exercise_dict = put_routines_request_exercise_instance.to_dict()
# create an instance of PutRoutinesRequestExercise from a dict
put_routines_request_exercise_from_dict = PutRoutinesRequestExercise.from_dict(put_routines_request_exercise_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


