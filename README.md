# From Model to Code
A tutorial for the iPraktikum SS23 @ TUM 

#### What we will do in this tutorial
- We will create an OpenAPI specification for the "Pedelec" from the course wide lecture
- We will generate a python [FastAPI](https://fastapi.tiangolo.com/lo/) server for the OpenAPI specification
- We will implement the server connecting it to an [Atlas](https://cloud.mongodb.com/) (MongoDB) database

#### In this tutorial you will learn:
- What is an OpenAPI specification
- How to create an OpenAPI specification for objects in your Analysis Object Model
- How to generate a server (or client) from an OpenAPI specification
- How to implement the generated methods

## Introduction

#### What is an OpenAPI Specification? 

OpenAPI Specification (formerly Swagger Specification) is an API description format for REST APIs.
An OpenAPI file allows you to describe your entire API, including:

- Available endpoints (/pedelecs) and operations on each endpoint (GET /pedelecs, POST /pedelecs)
- Input and Output parameters for each operation
- Authentication methods
Contact information, license, terms of use and other information.
API specifications can be written in YAML or JSON.
The complete OpenAPI Specification can be found on GitHub: [OpenAPI 3.0 Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md)

#### What Is Swagger?
Swagger is a set of open-source tools built around the OpenAPI Specification that can help you design, build, document and consume REST APIs.
Swagger tools:

- [Swagger Editor](https://editor.swagger.io/) – browser-based editor where you can write OpenAPI definitions.
- [Swagger UI](https://github.com/swagger-api/swagger-ui) – renders OpenAPI specifications as interactive documentation.
- [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) – generates server stubs and client libraries from an OpenAPI definition.

#### Why Use OpenAPI?
The ability of APIs to describe their own structure is the root of all awesomeness in OpenAPI. Once written, an OpenAPI specification and Swagger tools can drive your API development further in various ways:

- Design-first: use [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) to **generate a server** for your API
- Use [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) to **generate client s** for your API in over 40 languages
- Use [Swagger UI](https://github.com/swagger-api/swagger-ui) to **generate interactive API documentation** that lets your users try out the API calls directly in the browser 
- Use the spec to connect API-related tools to your API. For example, import the spec to SoapUI to create automated tests for your API.
- And more! Check out the open-source and commercial tools that integrate with Swagger.

Source: [Swagger](https://swagger.io/docs/specification/about/)

#### Tools to generate a server or client

There are many tools to generate server code and client code for OpenAPI specifications
- [swagger](https://editor.swagger.io/)
- [openapi-generator](https://openapi-generator.tech/)
- [fastapi-code-generator](https://github.com/koxudaxi/fastapi-code-generator)
- ...

## Interactive Tutorial

#### Create an OpenAPI Spec for the Pedelec App
Use the [Swagger Editor](https://editor.swagger.io/) to start defining the OpenAPI Spec for the pedelec app in YAML.

We start by defining Pedelec and Location with the properties from the Analysis Object Model

Location:
```yaml
Location:
      title: Location
      required:
        - latitude
        - longitude
        - altitude
      type: object
      properties:
        latitude:
          type: number
        longitude:
          type: number
        altitude:
          type: number
```
Pedelec:
```yaml
Pedelec:
      title: Pedelec
      required:
        - isAvailable
      type: object
      properties:
        charge:
          title: Charge
          maximum: 100
          minimum: 0
          type: integer
          description: Current charge level of the pedelec, expressed as percentage in (0,100)
        isAvailable:
          type: boolean
        location:
          $ref: '#/components/schemas/Location'
```
Since we will later want to identify Pedelecs we add an extension for the Pedelec that includes an ID:
```yaml
PedelecFullData:
      allOf:
        - $ref: '#/components/schemas/Pedelec'
        - type: object
          required:
            - id
          properties:
            id:
              type: string
              description: The ID of the pedelec
      description: Full data of the pedelec.
```
We can now define an endpoint to create a Pedelec.
This endpoint expects a Pedelec as input but returns a Pedelec with ID on successful creation.
```yaml
/pedelecs:
    post:
      summary: Create a new Pedelec
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Pedelec'
        required: true
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PedelecFullData'
```
Now we also define an endpoint to get all Pedelecs that returns all existing Pedelecs and their IDs:
```yaml
/pedelecs:
    get:
      summary: Retrieve all Pedelecs
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/PedelecFullData'
```
Lastly we add an endpoint to get a single Pedelec given its' ID:
```yaml
/pedelecs/{id}:
    get:
      summary: Get a specific Pedelec by ID
      parameters:
        - required: true
          schema:
            type: string
          name: id
          in: path
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PedelecFullData'
```

The full specification can be found [here](openapi.yaml)

#### Generate a server

To keep things simple we use the [fastapi-code-generator](https://github.com/koxudaxi/fastapi-code-generator).

First create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Next install [fastapi-code-generator](https://github.com/koxudaxi/fastapi-code-generator) with pip
```bash
pip install fastapi-code-generator
```

Lastly download your OpenAPI Specification from [Swagger Editor](https://editor.swagger.io/) and save it
in a file `openapi.yml`.

Then generate the FastAPI sever code with
```bash
fastapi-codegen --input openapi.yaml --output PedelecServer
```
You can find the generated code in [PedelecServerGenerated](PedelecServerGenerated).

#### Run the server

Add a `requirements.txt` with the following dependencies file in the PedelecServer folder.
```requirements.txt
fastapi
pymongo
pydantic
uvicorn[standard]
```

Install the requirements with:
```bash
pip install -r requirements.txt
```

Now you can start the server with
```bash
uvicorn main:app --reload
```

If you now go to [http://localhost:8000/docs](http://localhost:8000/docs) FastAPI shows
an interactive generated OpenAPI Specification for your running server.
So you don't have to worry about writing/extending the specification at this point.

#### Implementing the server

As you will have noticed non of the methods are actually implemented at the moment.

```python
@app.get('/pedelecs', response_model=List[PedelecFullData])
def get_pedelecs() -> List[PedelecFullData]:
    """
    Retrieve all Pedelecs
    """
    pass
```

There are many ways to implement the server at this point.

I want to provide a simple solution that uses the [Atlas](https://cloud.mongodb.com/) a MongoDB cloud database provider

On [Atlas](https://cloud.mongodb.com/) you have to:
- Create a "pedelec" DB and "pedelec" Collection on [Atlas](https://cloud.mongodb.com/)
- Create a user on [Atlas](https://cloud.mongodb.com/) to perform CRUD operations on this DB in "Database Access"
- Whitelist your IP Address on [Atlas](https://cloud.mongodb.com/) in "Network Access"
- Connect to our DB (You can find the code on [Atlas](https://cloud.mongodb.com/) under "Connect">"Driver">"Python")

Your code should then look similar to this:
```python
# Of course, you would usually set the password as environment variable and not directly in the code
uri = "mongodb+srv://<you get this during the last bullet point>"

# Create a new client and connect to the server
client = MongoClient(uri)

# get the DB and the collection
pedelec_db = client.get_database("pedelec")
pedelec_collection = pedelec_db.get_collection("pedelec")
```

You can now implement your endpoints:
```python
@app.get('/pedelecs', response_model=List[PedelecFullData])
def get_pedelecs() -> List[PedelecFullData]:
    """
    Retrieve all Pedelecs
    """
    return [PedelecFullData(**entry) for entry in pedelec_collection.find({})]


@app.post('/pedelecs', response_model=None, responses={'201': {'model': PedelecFullData}})
def post_pedelecs(pedelec: Pedelec) -> Union[None, PedelecFullData]:
    """
    Create a new Pedelec
    """
    pedelec_dict = json.loads(pedelec.json())
    # the id is added to pedelec_dict on insertion in the DB
    pedelec_collection.insert_one(pedelec_dict)
    return PedelecFullData(**pedelec_dict)


@app.get('/pedelecs/{id}', response_model=PedelecFullData)
def get_pedelecs_id(id: str) -> PedelecFullData:
    """
    Get a specific Pedelec by ID
    """
    result = pedelec_collection.find_one({"_id": ObjectId(id)})
    return PedelecFullData(**result)
```

Finally, the ObjectId generated by Atlas is not compatible with the pydantic 
BaseModel in [models.py](PedelecServerGenerated/models.py).

You need to implement a PydanticObjectId that is compatible with pydantic 
BaseModel:
```python
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
```

And adapt the id in the Pedelec + ID Model:
```python
class PedelecFullData(Pedelec):
    id: str = Field(..., description='The ID of the pedelec')
```

Have fun testing your server :)
I recommend postman or directly using the interactive OpenAPI Spec under [http://localhost:8000/docs](http://localhost:8000/docs).


#### Create an issue to leave feedback / questions :) 
