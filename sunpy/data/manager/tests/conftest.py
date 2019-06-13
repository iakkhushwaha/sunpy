import shutil
import tempfile
from unittest import mock

import pytest
from mocks import MockDownloader

from sunpy.data.manager.cache import Cache
from sunpy.data.manager.manager import DataManager
from sunpy.data.manager.storage import InMemStorage, SqliteStorage


@pytest.fixture
def downloader():
    downloader = MockDownloader()
    return downloader


@pytest.fixture
def storage():
    storage = InMemStorage()
    return storage


@pytest.fixture
def sqlstorage():
    storage = SqliteStorage('sunpy/data/manager/tests/test.db')
    return storage


@pytest.fixture
def manager(downloader, storage, mocker):
    tempdir = tempfile.mkdtemp()
    manager = DataManager(Cache(downloader, storage, tempdir))
    m = mock.Mock()
    m.headers = {'Content-Disposition': 'test_file'}
    mocker.patch('sunpy.data.manager.cache.urlopen', return_value=m)
    yield manager
    shutil.rmtree(tempdir)


@pytest.fixture
def data_function(manager):
    @manager.require('test_file', ['url1/test_file', 'url2'], '86f7e437faa5a7fce15d1ddcb9eaeaea377667b8')
    def foo(manager_tester=lambda x: 1):
        manager_tester(manager)

    return foo
