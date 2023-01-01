"""Test cz_conventionalish.py.

Create a ConventionishCz instance with default settings. Attributes should be equal
to ConventionalCommitsCz instance.

:author: Shay Hill
:created: 2023-01-01
"""

import commitizen
import cz_conventionalish as mod
import pytest
from commitizen import defaults
from commitizen.config import BaseConfig
from commitizen.cz.conventional_commits import ConventionalCommitsCz
from commitizen.defaults import MINOR, PATCH, Questions

DEFAULT_QUESTIONS = [
    ("fix", "A bug fix", "x", PATCH),
    ("feat", "A new feature", "f", MINOR),
    ("docs", "Documentation only changes", "d", None),
    (
        "style",
        (
            "Changes that do not affect the meaning of the code (white-space, "
            + "formatting, missing semi-colons, etc)"
        ),
        "s",
        None,
    ),
    (
        "refactor",
        "A code change that neither fixes a bug nor adds a feature",
        "r",
        PATCH,
    ),
    ("perf", "A code change that improves performance", "p", PATCH),
    ("test", "Adding missing or correcting existing tests", "t", None),
    (
        "build",
        (
            "Changes that affect the build system or external dependencies (example "
            + "scopes: pip, docker, npm)"
        ),
        "b",
        None,
    ),
    (
        "ci",
        (
            "Changes to our CI configuration files and scripts (example scopes: "
            + "GitLabCI)"
        ),
        "c",
        None,
    ),
]


def config():
    _config = BaseConfig()
    _config.settings.update({"name": defaults.DEFAULT_SETTINGS["name"]})
    return _config


@pytest.fixture(scope="function")
def commitizen_cc(mocker):
    return ConventionalCommitsCz(config())


@pytest.fixture(scope="function")
def custom_cc(mocker):
    mocker.patch.object(mod, "questions", DEFAULT_QUESTIONS)
    return mod.ConventionalishCz(config())


def _strip_correlates_with(questions: Questions):
    """Remove ". Correlates with ..." from the end of each paragraph choice.

    I made one small change to the original commitizen.cz.conventional_commits
    questions: The original describes fix and feat with, respectively, "A bug fix.
    Correlates with PATCH in Semver" and "A new feature. Correlates with MINOR in
    SemVar" I've added ".  Correlates with ... in SemVer" to every prefix that
    correlates with a SemVer bump. These extra ". Correlates need to be stripped away
    to test that ConventionishCz and ConventionalCommitsCz are "identical" with
    default settings.
    """
    for choice in tuple(questions)[0]["choices"]:
        choice["name"] = choice["name"].split(". Correlates with")[0]


def test_questions_choices(commitizen_cc, custom_cc):
    """Test choices in questions method.

    Only check the first two because I've *slightly* modified the format so that
    every prefix that correlates to a symver has "Correlates with ..." in the name.
    """
    default_questions = commitizen_cc.questions()
    updated_questions = custom_cc.questions()
    _strip_correlates_with(default_questions)
    _strip_correlates_with(updated_questions)
    assert default_questions == updated_questions


def test_schema_pattern(commitizen_cc, custom_cc):
    """Test schema pattern."""
    assert commitizen_cc.schema_pattern() == custom_cc.schema_pattern()


def test_bump_pattern(commitizen_cc, custom_cc):
    """Test bump pattern."""
    assert commitizen_cc.bump_pattern == custom_cc.bump_pattern


def test_changelog_pattern(commitizen_cc, custom_cc):
    """Test bump pattern."""
    assert commitizen_cc.changelog_pattern == custom_cc.changelog_pattern


def test_bump_map(commitizen_cc, custom_cc):
    """Test bump pattern."""
    assert commitizen_cc.bump_map == custom_cc.bump_map


def test_commit_parser(commitizen_cc, custom_cc):
    """Test bump pattern."""
    assert commitizen_cc.commit_parser == custom_cc.commit_parser


def test_change_type_map(commitizen_cc, custom_cc):
    """Test bump pattern."""
    assert commitizen_cc.change_type_map == custom_cc.change_type_map
