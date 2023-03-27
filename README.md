# Quant API Service #

This application is a light-weight Backend API service, built with Python and Flask framework.


## Prerequisite

* Download and install Python 3.
* Ensure you have the `venv` module installed.


## Setting Up Development

1. Create a virtual environment with `python3 -m venv <name_of_venv>`

2. Download all libraries with `pip3 install -r app/requirements.txt`

3. Activate virtual environment with `source <name_of_venv>/bin/activate`

4. Change to workspace dir `cd /app` and Create the `.env` file using the `.env.example` - config your real falcon lib path here


## Running Project
Make sure all the following commands are run under work dir `/app`, if not, run `cd /app` first.

There are many ways to run/debug the server, including 
- from command line directly (easiest)
- by PyCharm Run configurations (recommend)
- from docker (optional)

### Command line running
Open file `main_app.py` on PyCharm and then right-click, select `Debug Flask (app/main_app.py)`

or just run the following command on terminal:
```bash
$ python3 main_app.py
```

### PyCharm Run configurations
reference [Run/Debug Configuration: Python](https://www.jetbrains.com/help/pycharm/run-debug-configuration-python.html)

1. open the Run/Debug Configuration add a python configuration
2. specify *script path* to `<your-real-path-to>/app/main_app`
3. [optional] add an environment variable: `FLASK_DEBUG=True`

done

### Docker Run
Need docker daemon installed, pass here


## Testing API
we can use a GUI client such as `postman` to test with api, the url is `http://127.0.0.1:5000` by default, make sure to add
an authorization header with key: `X-Api-Key` and the value defined in your .env

here is an example with built-in curl command:
```shell
curl -i -X GET \
  -H "X-Api-Key:C75BDA2B0F854B26BC55B15150ABCDB0" \
  'http://127.0.0.1:5000/'
```

there is a chrome plugin [Talend API Tester](https://chrome.google.com/webstore/detail/talend-api-tester-free-ed/aejoelaoggembcahagimdiliamlcdmfm)
we can use to test apis in a GUI way.

## Set up PyCharm external falcon lib
Cause falcon is an external lib out of our project, so pycharm code intelligent can’t detect that, but we can add it manually

1. Focus on the left block of PyCharm, on the project tab, expand to `External Libraries > Python 3.x.. > site-packages`, right-click
on the `site-packages`, then select Open in Terminal
2. On the opened terminal, run 
    ```shell
    ln -s <REAL_PATH_TO_YOUR_FALCON_LIB> ./falcon
    ```
    remember to replace <REAL_PATH_TO_YOUR_FALCON_LIB> here to your real path such as
    `/home/falcon`
