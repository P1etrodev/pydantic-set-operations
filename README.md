﻿# Pydantic-Set-Operations

The `Pydantic-Set-Operations` package provides an enhanced version of Pydantic's `BaseModel`, allowing for advanced model manipulations, such as field unions, exclusions, and intersections. This subclass of `BaseModel` introduces bitwise operations (like `|`, `&`, and `-`) for combining, intersecting, and excluding fields between models.

### Key Model Features

1. **Field Union (`union` method)**: Combines fields from two models, prioritizing fields from the initiating model if overlaps exist.
2. **Field Exclusion (`omit` method)**: Creates a new model excluding specified fields or fields present in another model.
3. **Field Intersection (`pick` method)**: Creates a model containing only fields shared between two models.

### Key Instance Features

1. **Field Union (`|` operator)**: Returns an instance combining fields from both instances.
2. **Field Exclusion (`-` operator)**: Returns an instance excluding fields present in another instance.
3. **Field Intersection (`&` operator)**: Returns an instance containing only fields shared between two instances.

## API Methods

### `union`

Creates a new model by merging fields from the current model (`self`) and another `ExtendedBaseModel`. In cases of field overlap, fields from the current model are prioritized.

**Parameters**

- `_name` (`str`): The name for the resulting model.
- `other` (`ExtendedBaseModel`): The model to merge fields with.

**Returns**

`BaseModel`: A new model containing fields from both models.

**Example usage**

```py
from pydantic_set_operations import ExtendedBaseModel


class ModelA(ExtendedBaseModel):
	name: str
	age: int


class ModelB(ExtendedBaseModel):
	age: float
	location: str


MergedModel = ModelA.union("MergedModel", ModelB)
merged_instance = MergedModel(name="Alice", age=30, location="Paris")
print(merged_instance.model_dump())
# Output: {'name': 'Alice', 'age': 30, 'location': 'Paris'}
```

### `omit`

Creates a new model by excluding specified fields from the current model.

**Parameters**

- `_name` (`str`): The name for the resulting model.
- `*excluded_fields` (`str`): Fields to exclude from the model.

**Returns**

`BaseModel`: A new model without the specified fields.

**Example usage**

```py
from pydantic_set_operations import ExtendedBaseModel


class Model(ExtendedBaseModel):
	id: int
	name: str
	email: str


NoEmailModel = Model.omit("NoEmailModel", "email")
no_email_instance = NoEmailModel(id=1, name="Alice")
print(no_email_instance.model_dump())
# Output: {'id': 1, 'name': 'Alice'}
```

### `pick`

Creates a new model containing only the specified fields.

**Parameters**

- `_name` (`str`): The name for the resulting model.
- `*included_fields` (`str`): Fields to include in the model.

**Returns**

- `BaseModel`: A new model containing only the specified fields.

**Example usage**

```py
from pydantic_set_operations import ExtendedBaseModel


class Model(ExtendedBaseModel):
	username: str
	password: str
	email: str


UsernameEmailModel = Model.pick("UsernameEmailModel", "username", "email")
user_instance = UsernameEmailModel(username="alice", email="alice@example.com")
print(user_instance.model_dump())
# Output: {'username': 'alice', 'email': 'alice@example.com'}
```

### `&` Operator (intersection)

The `&` operator between two `ExtendedBaseModel` instances creates a model containing only fields common to both instances, taking values from the initiating model.

**Example usage**

```py
from pydantic_set_operations import ExtendedBaseModel


class ModelA(ExtendedBaseModel):
	name: str
	age: int


class ModelB(ExtendedBaseModel):
	age: int
	location: str


intersection = ModelA(name="Alice", age=30) & ModelB(age=25, location="Paris")
print(intersection.model_dump())
# Output: {'age': 30}
```

### `-` Operator (exclusion)

The `-` operator excludes fields present in another instance of `ExtendedBaseModel`.

**Example usage**

```py
from pydantic_set_operations import ExtendedBaseModel


class ModelA(ExtendedBaseModel):
	id: int
	username: str
	password: str


class ModelB(ExttendedBaseModel):
	password: str


exclusion = ModelA(id=1, username="user123", password="pass") - ModelB(password="pass")
print(exclusion.model_dump())
# Output: {'id': 1, 'username': 'user123'}
```

### `|` Operator (union)

The `|` operator merges fields from two models, prioritizing values from the initiating model.

**Example usage**

```py
from pydantic_set_operations import ExtendedBaseModel


class ModelA(ExtendedBaseModel):
	first_name: str
	last_name: str


class ModelB(ExtendedBaseModel):
	last_name: str
	age: int


union = ModelA(first_name="Alice", last_name="Johnson") | ModelB(last_name="Smith", age=30)
print(union.model_dump())
# Output: {'first_name': 'Alice', 'last_name': 'Johnson', 'age': 30}
```

**Summary**

`Pydantic-Set-Operations` offers a flexible way to perform advanced model operations, enabling complex field manipulations through familiar bitwise operators. With features like union, exclusion, and intersection, this package is ideal for projects that require dynamic model restructuring or filtering based on specific fields.