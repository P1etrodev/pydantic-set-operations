from src.pydantic_set_operations import ExtendedBaseModel


class ExampleA(ExtendedBaseModel):
	id: int
	name: str


class ExampleB(ExampleA.pick('ExampleB', 'id')):
	...