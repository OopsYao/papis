import os
import pytest

import papis.downloaders
from papis.downloaders.aps import Downloader

import logging
logging.basicConfig(level=logging.DEBUG)

APS_URLS = (
    "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.122.145901",
    "https://journals.aps.org/prx/abstract/10.1103/PhysRevX.12.041027",
    "https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.94.045004",
    )


@pytest.mark.parametrize("url", APS_URLS)
def test_aps_fetch(monkeypatch, url: str) -> None:
    cls = papis.downloaders.get_downloader_by_name("aps")
    assert cls is Downloader

    down = cls.match(url)
    assert down is not None

    uid = os.path.basename(url)
    infile = "APS_{}.html".format(uid)
    outfile = "APS_{}_Out.json".format(uid)

    from tests.downloaders import get_remote_resource, get_local_resource

    with monkeypatch.context() as m:
        m.setattr(down, "_get_body", get_remote_resource(infile, url))
        m.setattr(down, "download_document", lambda: None)

        # NOTE: bibtex add some extra fields, so we just disable it for the test
        m.setattr(down, "download_bibtex", lambda: None)

        down.fetch()
        extracted_data = down.ctx.data
        expected_data = get_local_resource(outfile, extracted_data)

        assert extracted_data == expected_data
