# PostRoutinesRequestSetRepRange

Range of reps for the set, if applicable

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** | Starting rep count for the range | [optional] 
**end** | **float** | Ending rep count for the range | [optional] 

## Example

```python
from hevy_api_service.models.post_routines_request_set_rep_range import PostRoutinesRequestSetRepRange

# TODO update the JSON string below
json = "{}"
# create an instance of PostRoutinesRequestSetRepRange from a JSON string
post_routines_request_set_rep_range_instance = PostRoutinesRequestSetRepRange.from_json(json)
# print the JSON string representation of the object
print(PostRoutinesRequestSetRepRange.to_json())

# convert the object into a dict
post_routines_request_set_rep_range_dict = post_routines_request_set_rep_range_instance.to_dict()
# create an instance of PostRoutinesRequestSetRepRange from a dict
post_routines_request_set_rep_range_from_dict = PostRoutinesRequestSetRepRange.from_dict(post_routines_request_set_rep_range_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


