# PutRoutinesRequestSetRepRange

Range of reps for the set, if applicable

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** | Starting rep count for the range | [optional] 
**end** | **float** | Ending rep count for the range | [optional] 

## Example

```python
from hevy_api_service.models.put_routines_request_set_rep_range import PutRoutinesRequestSetRepRange

# TODO update the JSON string below
json = "{}"
# create an instance of PutRoutinesRequestSetRepRange from a JSON string
put_routines_request_set_rep_range_instance = PutRoutinesRequestSetRepRange.from_json(json)
# print the JSON string representation of the object
print(PutRoutinesRequestSetRepRange.to_json())

# convert the object into a dict
put_routines_request_set_rep_range_dict = put_routines_request_set_rep_range_instance.to_dict()
# create an instance of PutRoutinesRequestSetRepRange from a dict
put_routines_request_set_rep_range_from_dict = PutRoutinesRequestSetRepRange.from_dict(put_routines_request_set_rep_range_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


