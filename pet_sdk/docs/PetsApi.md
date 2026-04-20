# openapi_client.PetsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_pet_pets_post**](PetsApi.md#add_pet_pets_post) | **POST** /pets/ | Add Pet
[**adopt_pet_pets_id_adopt_post**](PetsApi.md#adopt_pet_pets_id_adopt_post) | **POST** /pets/{id}/adopt | Adopt Pet
[**list_pets_pets_get**](PetsApi.md#list_pets_pets_get) | **GET** /pets/ | List Pets


# **add_pet_pets_post**
> PetResponse add_pet_pets_post(pet_create)

Add Pet

### Example


```python
import openapi_client
from openapi_client.models.pet_create import PetCreate
from openapi_client.models.pet_response import PetResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.PetsApi(api_client)
    pet_create = openapi_client.PetCreate() # PetCreate | 

    try:
        # Add Pet
        api_response = api_instance.add_pet_pets_post(pet_create)
        print("The response of PetsApi->add_pet_pets_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PetsApi->add_pet_pets_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pet_create** | [**PetCreate**](PetCreate.md)|  | 

### Return type

[**PetResponse**](PetResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **adopt_pet_pets_id_adopt_post**
> PetResponse adopt_pet_pets_id_adopt_post(id)

Adopt Pet

### Example


```python
import openapi_client
from openapi_client.models.pet_response import PetResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.PetsApi(api_client)
    id = 56 # int | 

    try:
        # Adopt Pet
        api_response = api_instance.adopt_pet_pets_id_adopt_post(id)
        print("The response of PetsApi->adopt_pet_pets_id_adopt_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PetsApi->adopt_pet_pets_id_adopt_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**PetResponse**](PetResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_pets_pets_get**
> List[PetResponse] list_pets_pets_get()

List Pets

### Example


```python
import openapi_client
from openapi_client.models.pet_response import PetResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.PetsApi(api_client)

    try:
        # List Pets
        api_response = api_instance.list_pets_pets_get()
        print("The response of PetsApi->list_pets_pets_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PetsApi->list_pets_pets_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PetResponse]**](PetResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

