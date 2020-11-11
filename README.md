## Technology

- Python
    - `requests` to consume API
    - `enum` for an alternate construction of `originAccount` and `targetAccount`
- Flask: 
    - `jsonify` to send response as json after manipulating data in Python

## To run locally

- `conda create -n ellevest` (or any virtual environment)
- `conda install flask`
- `flask run`
- `http://127.0.0.1:5000/feed`