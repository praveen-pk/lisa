# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from assertpy import assert_that

from lisa import Node, TestCaseMetadata, TestSuite, TestSuiteMetadata
from lisa.features.security_profile import SecureBootEnabled
from lisa.sut_orchestrator import AZURE
from lisa.testsuite import simple_requirement
from lisa.tools import Dmesg


@TestSuiteMetadata(
    area="lvbs_heki",
    category="functional",
    description="""
    This test suite validates HEKI-related boot signals on Azure LVBS guests.
    """,
)
class LVBSHekiBoot(TestSuite):
    @TestCaseMetadata(
        description="""
        Verify the Azure VM boots with HEKI enabled by checking dmesg for:
        1. Secure boot enabled
        2. heki-guest: Control registers locked
        3. heki-guest: Loaded kernel data

        Note: Ordering is not validated; only presence is required.
        """,
        priority=1,
        requirement=simple_requirement(
            supported_features=[SecureBootEnabled()],
            supported_platform_type=[AZURE],
        ),
    )
    def verify_heki_boot_messages(self, node: Node) -> None:
        dmesg_output = node.tools[Dmesg].get_output(force_run=True)

        assert_that(dmesg_output).described_as(
            "Expected secure boot and HEKI boot messages were not all found in dmesg."
        ).contains(
            "Secure boot enabled",
            "heki-guest: Control registers locked",
            "heki-guest: Loaded kernel data",
        )
