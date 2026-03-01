# ActiveSubscription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **str** |  | [optional] 
**iap_id** | **int** |  | [optional] 
**iap_purchase_type** | **str** |  | [optional] 
**iap_platform_id** | **str** |  | [optional] 
**iap_name** | **str** |  | [optional] 
**is_free_trial** | **bool** |  | [optional] 
**is_intro_priced** | **bool** |  | [optional] 
**referral_id** | **int** |  | [optional] 
**referral_code** | **str** |  | [optional] 
**referral_type** | **str** |  | [optional] 
**purchase_date** | **datetime** |  | [optional] 
**expiration_date** | **datetime** |  | [optional] 
**cancellation_date** | **datetime** |  | [optional] 
**access** | **List[str]** |  | [optional] 
**subscription_id** | **str** |  | [optional] 

## Example

```python
from api_service_rp.models.active_subscription import ActiveSubscription

# TODO update the JSON string below
json = "{}"
# create an instance of ActiveSubscription from a JSON string
active_subscription_instance = ActiveSubscription.from_json(json)
# print the JSON string representation of the object
print(ActiveSubscription.to_json())

# convert the object into a dict
active_subscription_dict = active_subscription_instance.to_dict()
# create an instance of ActiveSubscription from a dict
active_subscription_from_dict = ActiveSubscription.from_dict(active_subscription_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


