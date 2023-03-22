import pytest
from unittest.mock import patch, call
from aiohttp import ClientSession, ClientError


from areq import fetch_html
from conftest import mock_request
class TestFetchHtml:
    @pytest.mark.asyncio
    async def test_fetch_html(self): 
        with patch.object(ClientSession, 'request', side_effect=lambda *args, **kwargs: mock_request(200)):
            res = await fetch_html('http://example.com', ClientSession())
            assert type(res) is str

    @pytest.mark.asyncio
    async def test_fetch_html_exception(self):
        with patch.object(ClientSession, 'request', side_effect=lambda *args, **kwargs: mock_request(404, _raise=True)):
            with pytest.raises(ClientError):
                await fetch_html('http://example.com', ClientSession())


from areq import parse
class TestParse:
    # test an ClientError is raised when the request fails
    @pytest.mark.asyncio
    async def test_parse_exception(self, caplog):
        with patch.object(ClientSession, 'request', side_effect=lambda *args, **kwargs: mock_request(404, _raise=True)):
            await parse('http://example.com', ClientSession())
            assert caplog.records[0].levelname == 'ERROR'
    
    # test the href is found
    @pytest.mark.asyncio
    async def test_parse_find_href(self):
        with patch.object(ClientSession, 'request', side_effect=lambda *args, **kwargs: mock_request(200)):
            assert await parse('http://example.com', ClientSession()) == {'http://example.com/static/assets/'}


from areq import write_one
from conftest import mock_aiofile_open
class TestWriteOne:
    @pytest.mark.asyncio
    async def test_write_one(self, caplog):
        fake_file_path = 'tests/fake_file.txt'
        m = mock_aiofile_open(fake_file_path)
        with patch.object(ClientSession, 'request', side_effect=lambda *args, **kwargs: mock_request(200)):
            with patch('aiofiles.open', m):
                async with ClientSession() as session:
                    test_url = 'http://example.com'
                    await write_one(fake_file_path, test_url, session=session)
                    m.assert_has_calls([call(fake_file_path, 'a')])
                    m().__aenter__.assert_awaited()
                    m().write.assert_called_once_with(f"{test_url} -> {test_url}/static/assets/\n")

                    
                    
