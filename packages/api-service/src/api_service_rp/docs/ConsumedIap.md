# ConsumedIap


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **str** |  | [optional] 
**purchase_type** | **str** |  | [optional] 
**platform_id** | **str** |  | [optional] 
**subscription_group_id** | **str** |  | [optional] 
**subscription_group_key** | **str** |  | [optional] 
**access** | **List[str]** |  | [optional] 
**access_ends_at** | **datetime** |  | [optional] 

## Example

```python
from api_service_rp.models.consumed_iap import ConsumedIap

# TODO update the JSON string below
json = "{}"
# create an instance of ConsumedIap from a JSON string
consumed_iap_instance = ConsumedIap.from_json(json)
# print the JSON string representation of the object
print(ConsumedIap.to_json())

# convert the object into a dict
consumed_iap_dict = consumed_iap_instance.to_dict()
# create an instance of ConsumedIap from a dict
consumed_iap_from_dict = ConsumedIap.from_dict(consumed_iap_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


