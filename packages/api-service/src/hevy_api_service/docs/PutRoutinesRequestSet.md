# PutRoutinesRequestSet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the set. | [optional] 
**weight_kg** | **float** | The weight in kilograms. | [optional] 
**reps** | **int** | The number of repetitions. | [optional] 
**distance_meters** | **int** | The distance in meters. | [optional] 
**duration_seconds** | **int** | The duration in seconds. | [optional] 
**custom_metric** | **float** | A custom metric for the set. Currently used for steps and floors. | [optional] 
**rep_range** | [**PutRoutinesRequestSetRepRange**](PutRoutinesRequestSetRepRange.md) |  | [optional] 

## Example

```python
from hevy_api_service.models.put_routines_request_set import PutRoutinesRequestSet

# TODO update the JSON string below
json = "{}"
# create an instance of PutRoutinesRequestSet from a JSON string
put_routines_request_set_instance = PutRoutinesRequestSet.from_json(json)
# print the JSON string representation of the object
print(PutRoutinesRequestSet.to_json())

# convert the object into a dict
put_routines_request_set_dict = put_routines_request_set_instance.to_dict()
# create an instance of PutRoutinesRequestSet from a dict
put_routines_request_set_from_dict = PutRoutinesRequestSet.from_dict(put_routines_request_set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


