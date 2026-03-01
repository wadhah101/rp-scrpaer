# UserSubscriptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_subscriptions** | [**List[ActiveSubscription]**](ActiveSubscription.md) |  | [optional] 
**consumed_iaps** | [**List[ConsumedIap]**](ConsumedIap.md) |  | [optional] 
**stripe_ids** | **List[str]** |  | [optional] 
**training_last_access_added_at** | **datetime** |  | [optional] 

## Example

```python
from api_service_rp.models.user_subscriptions import UserSubscriptions

# TODO update the JSON string below
json = "{}"
# create an instance of UserSubscriptions from a JSON string
user_subscriptions_instance = UserSubscriptions.from_json(json)
# print the JSON string representation of the object
print(UserSubscriptions.to_json())

# convert the object into a dict
user_subscriptions_dict = user_subscriptions_instance.to_dict()
# create an instance of UserSubscriptions from a dict
user_subscriptions_from_dict = UserSubscriptions.from_dict(user_subscriptions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


