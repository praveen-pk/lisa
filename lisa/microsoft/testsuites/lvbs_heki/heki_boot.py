# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from assertpy import assert_that

from lisa import Logger, Node, TestCaseMetadata, TestSuite, TestSuiteMetadata
from lisa.features.security_profile import SecureBootEnabled
from lisa.testsuite import simple_requirement
from lisa.tools import Dmesg


@TestSuiteMetadata(
    area="lvbs_heki",
    category="functional",
    description="""
    This suite validates that LVBS HEKI guest boot markers are present in dmesg.
    """,
)
class LvbsHekiBoot(TestSuite):
    @TestCaseMetadata(
        description="""
        Verify the VM boots with HEKI enabled by checking dmesg for expected
        secure boot and HEKI guest initialization markers.

        Steps:
        1. Collect dmesg output.
        2. Verify all expected LVBS HEKI boot markers are present.
        """,
        priority=1,
        requirement=simple_requirement(
            supported_features=[SecureBootEnabled()],
        ),
    )
    def verify_heki_boot_messages(self, node: Node, log: Logger) -> None:
        dmesg_output = node.tools[Dmesg].get_output(force_run=True)

        expected_messages = [
            "Secure boot enabled",
            "heki-guest: Control registers locked",
            "heki-guest: Loaded kernel data",
        ]

        for message in expected_messages:
            assert_that(dmesg_output).described_as(
                f"Required boot message missing in dmesg: {message}"
            ).contains(message)

        log.info("All expected LVBS HEKI boot markers were found in dmesg.")
