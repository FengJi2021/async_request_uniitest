import io
from unittest.mock import AsyncMock, MagicMock
from aiohttp import ClientError

# mock a request
async def mock_request(status_code, _raise=False):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code
            self._raise = _raise

        def raise_for_status(self):
            if self._raise:
                raise ClientError

        async def text(self):
            # return a html template
            return '<a href="/static/assets/">example</a>'

    return MockResponse(status_code)

# mock aiofiles.open
def mock_aiofile_open(read_data=''):
    _read_data = io.StringIO(read_data)

    async def _write_side_effect(data):
        return _read_data.write(data)
    
    async def _read_side_effect():
        return _read_data.read()
    
    handle = MagicMock(name='handle')
    handle.__aenter__ = AsyncMock(name='__aenter__', return_value=handle)
    handle.__aexit__ = AsyncMock(name='__aexit__', return_value=None)
    handle.read.return_value = None
    handle.write.return_value = None

    handle.read.side_effect = _read_side_effect
    handle.write.side_effect = _write_side_effect

    mock = MagicMock(name='open')
    mock.return_value = handle
    return mock