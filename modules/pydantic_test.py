from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    ssn: str = None  # Optional sensitive field

# Create an instance of the Person model
person = Person(name="Alice", age=30)

# Convert to dict, excluding fields that are unset (i.e., still at their default value)
person_dict = person.dict(exclude_unset=True)
print(person_dict)  # Outputs: {'name': 'Alice', 'age': 30}

# Convert to dict, excluding fields that are None
person_dict = person.dict(exclude_none=True)
print(person_dict)  # Outputs: {'name': 'Alice', 'age': 30}
