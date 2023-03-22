# async_request_unittest

Do unittest for asynchroneous request with aiohttp and asynchroneous file reading with aiofiles in framework of pytest.

## How to use

Install the dependencies:

```bash
pip3 install -r requirements.txt
```

Run the following command in the root directory of the project:

```bash
python3 -m pytest
```

## What is new here

- [x] Mock a asynchroneous response to test a aiohttp request

- [x] Mock a asynchroneous file reading to test a aiofiles reading

## What to do next

- [ ] Extend the asynchroneous mock to full methods and attributes of the asynchroneous response of aiohttp

- [ ] Try out the official utils of aiohttp server links:<https://docs.aiohttp.org/en/stable/testing.html#>