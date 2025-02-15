import base64

import pytest

from tests.fixtures import mars_jira  # noqa


@pytest.mark.asyncio
async def test_all_in_one(mars_jira):
    #    result = await mars_jira.create_issue(
    #        summary="TestAsset", description="Don't touch please", fields={"components": "Desktop", "mteam": "FLS"}
    #    )
    #    assert result.startswith("IT-")
    result = "IT-810958"
    # assert await mars_jira.comment_issue(issue=result, comment="test_comment")
    # assert await mars_jira.update_issue(issue=result, fields={"labels": "hwr_done"})
    try:
        file = open("tests/lina.jpg", "rb")
        encoded = base64.b64encode(file.read()).decode("utf-8")
        assert await mars_jira.upload_attachment(issue=result, file_name="lina.jpg", file=encoded)
    finally:
        file.close()
