from os import makedirs

from pydantic import BaseModel, create_model
from typing import Type


class ExtendedBaseModel(BaseModel):
	# Aquí se omite el código anterior para centrarse en la generación del archivo .pyi
	
	@classmethod
	def generate_pyi(cls, _name: str, fields: dict):
		"""
		Generate a .pyi file for the dynamically created model to provide type hints to IDEs.
		
		Args:
				_name (str): The name of the new model.
				fields (dict): A dictionary of field names and types to be included in the .pyi file.
		"""
		makedirs('types/', exist_ok=True)
		pyi_filename = f"types/{_name}.pyi"
		with open(pyi_filename, "w") as pyi_file:
			pyi_file.write(f"from pydantic import BaseModel\n\n")
			pyi_file.write(f"class {_name}(BaseModel):\n")
			
			for field, (field_type, _) in fields.items():
				pyi_file.write(f"    {field}: {field_type.__name__}\n")
	
	@classmethod
	def union(cls, _name: str, other: 'ExtendedBaseModel') -> Type[BaseModel]:
		"""
		Creates a new model that merges fields from the current class and another
		ExtendedBaseModel class. In case of overlapping fields, values and data types
		from the current model (self) take precedence.
		
		Args:
				_name (str): The name for the new model.
				other (ExtendedBaseModel): Another model to merge fields with.
		
		Returns:
				Type[BaseModel]: A new model including fields from both the current class and
				the other model.
		"""
		# Merge annotations from both models, with precedence for the current class
		fields_data = {*other.__annotations__.items(), *cls.__annotations__.items()}
		new_fields = {field: (annotation, ...) for field, annotation in fields_data}
		
		# Generate .pyi file for the new model
		cls.generate_pyi(_name, new_fields)
		
		# Return the new model
		return create_model(_name, **new_fields)
	
	@classmethod
	def omit(cls, _name: str, *excluded_fields: str) -> Type[BaseModel]:
		"""
		Exclude specified fields from the current model to create a new model with
		only the remaining fields.
		
		Args:
				_name (str): The name for the new model.
				*excluded_fields (str): Fields to exclude from the model.
		
		Returns:
				Type[BaseModel]: A new model excluding the specified fields.
		"""
		new_fields = {
			field: (cls.__annotations__[field], cls.model_fields[field])
			for field in cls.__annotations__
			if field not in excluded_fields
		}
		
		# Generate .pyi file for the new model
		cls.generate_pyi(_name, new_fields)
		
		return create_model(_name, **new_fields)
	
	@classmethod
	def pick(cls, _name: str, *included_fields: str) -> Type[BaseModel]:
		"""
		Generate a new model with only the specified fields from the current model.
		
		Args:
				_name (str): The name for the new model.
				*included_fields (str): Fields to include in the new model.
		
		Returns:
				Type[BaseModel]: A new model containing only the specified fields.
		"""
		new_fields = {
			field: (cls.__annotations__[field], cls.model_fields[field])
			for field in cls.__annotations__
			if field in included_fields
		}
		
		# Generate .pyi file for the new model
		cls.generate_pyi(_name, new_fields)
		
		return create_model(_name, **new_fields)
