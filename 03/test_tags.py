import re
import pytest

from tags import get_tags, get_top_tags
from tags import get_similarities, TOP_NUMBER

TAG_COUNT = re.compile(r'">([^<]+)</a>\s\((\d+)\)<')
TAGS = "tags.html"


def parse_tags_html():
    with open(TAGS) as f:
        for line in f:
            if "/tag/" not in line:
                continue
            m = TAG_COUNT.search(line.rstrip())
            if m:
                yield m.groups()[0], int(m.groups()[1])


@pytest.fixture(scope="module")
def setup_tags():
    return get_tags()


def test_get_tags(setup_tags):
    assert len(setup_tags) == 189
    assert len(set(setup_tags)) == 100
    assert setup_tags.count("collections") == 4
    assert setup_tags.count("python") == 10


@pytest.mark.xfail
def test_get_top_tags(setup_tags):
    top_tags = dict(get_top_tags(setup_tags)).items()
    assert len(top_tags) == TOP_NUMBER
    pybites_tags = dict(parse_tags_html())
    for tag in top_tags:
        assert tag in pybites_tags.items()


@pytest.mark.xfail
def test_get_similarities(setup_tags):
    similar_tags = dict(get_similarities(setup_tags)).items()
    assert len(similar_tags) == 3
    assert ("game", "games") in similar_tags
    assert ("challenge", "challenges") in similar_tags
    assert ("generator", "generators") in similar_tags
