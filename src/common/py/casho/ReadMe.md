# How to publish

# Create the dist files using the following code:
    
    pip install wheel
    python setup.py sdist bdist_wheel

# Upload the dist folder to PYPI using Twine:
  
    pip install twine
    twine upload dist/*                                                                                               
# casho

casho is a django library that provides custom error handling functionality for Django applications.

## Installation

# You can install casho using pip:

shell
pip install casho

# After installing add in the Setting.py

 settings.py

INSTALLED_APPS = [
    <!-- # Other apps... -->
    'casho',
]

# To use the middlewares 
 
settings.py

MIDDLEWARE = [
    # Other apps...
    'casho.ErrorHandlingMiddleware',
    'casho.HealthCheckMiddleware'
]

# To use other classes 

Import casho

casho.IErrorStruct
casho.DatabaseConnectionError
casho.CustomError

# To create Kafka consumer and producer 

producer = casho.ProducerFactory.get_producer( metadata: IProducerConfiguration)
producer.send_message( metadata: IMetadata, message: IEvent)

consumer = casho.ConsumerFactory.get_consumer(metadata: ConsumerConfiguration)
consumer.subscribe( topic: str, callback: Callable[[IEvent], None])