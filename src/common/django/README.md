# Common module for code sharing.

Increment version in setup.py file `major.minor.patch`

## Build

```
pip install wheel
python3 setup.py bdist_wheel
```

## How to install

copy .whl to packages folder.

## How to use middlewares

#### To use error handler middleware
- add it to the middlewares in settings.py of you project as
```
'shared.middleware.ErrorHandlingMiddleware'
```
#### To use Ipinfo middleware
 - install the ipinfo-django library to your project.
- create a instance of ipinfo handler and save it to a variable as
```
IPINFO_HANDLER = ipinfo.getHandler('your_token')
```
- add the middleware to the middlewares list as
```
'shared.middleware.IpToGeoMiddleware'
```