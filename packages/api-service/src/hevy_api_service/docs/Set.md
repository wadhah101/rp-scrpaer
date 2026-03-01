# Set


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** | Index indicating the order of the set in the workout. | [optional] 
**type** | **str** | The type of set. This can be one of &#39;normal&#39;, &#39;warmup&#39;, &#39;dropset&#39;, &#39;failure&#39; | [optional] 
**weight_kg** | **float** | Weight lifted in kilograms. | [optional] 
**reps** | **float** | Number of reps logged for the set | [optional] 
**distance_meters** | **float** | Number of meters logged for the set | [optional] 
**duration_seconds** | **float** | Number of seconds logged for the set | [optional] 
**rpe** | **float** | RPE (Relative perceived exertion) value logged for the set | [optional] 
**custom_metric** | **float** | Custom metric logged for the set (Currently only used to log floors or steps for stair machine exercises) | [optional] 

## Example

```python
from hevy_api_service.models.set import Set

# TODO update the JSON string below
json = "{}"
# create an instance of Set from a JSON string
set_instance = Set.from_json(json)
# print the JSON string representation of the object
print(Set.to_json())

# convert the object into a dict
set_dict = set_instance.to_dict()
# create an instance of Set from a dict
set_from_dict = Set.from_dict(set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


