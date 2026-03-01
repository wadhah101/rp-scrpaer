# MesocycleSummary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**key** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**days** | **int** |  | [optional] 
**weeks** | **int** |  | [optional] 
**unit** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from api_service_rp.models.mesocycle_summary import MesocycleSummary

# TODO update the JSON string below
json = "{}"
# create an instance of MesocycleSummary from a JSON string
mesocycle_summary_instance = MesocycleSummary.from_json(json)
# print the JSON string representation of the object
print(MesocycleSummary.to_json())

# convert the object into a dict
mesocycle_summary_dict = mesocycle_summary_instance.to_dict()
# create an instance of MesocycleSummary from a dict
mesocycle_summary_from_dict = MesocycleSummary.from_dict(mesocycle_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


