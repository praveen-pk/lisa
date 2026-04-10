# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from semver import VersionInfo
from typing import Any

from lisa import (
    Logger,
    Node,
    TestCaseMetadata,
    TestSuite,
    TestSuiteMetadata,
    simple_requirement,
)
from lisa.base_tools.uname import Uname
from assertpy import assert_that


@TestSuiteMetadata(
    area="kernel",
    category="functional",
    description="""
    Kernel validation tests.
    """,
    owner="prapal",
)
class KernelVersionSuite(TestSuite):
    @TestCaseMetadata(
        description="Verify the guest kernel version is at least 6.18.",
        priority=1,
        timeout=600,
        requirement=simple_requirement(),
    )
    def verify_kernel_version_at_least_6_18(self, node: Node, log: Logger) -> None:
        # --- Arrange ---
        uname = node.tools[Uname]

        # --- Act ---
        log.info("Retrieving kernel version via uname tool...")
        info = uname.get_linux_information(force_run=True)
        assert info.has_result, "Failed to retrieve uname information from node"
        kernel_version = info.kernel_version

        # --- Assert ---
        required = VersionInfo(6, 18, 0)
        assert_that(kernel_version).described_as(
            f"Kernel version {kernel_version} is less than required {required}"
        ).is_greater_than_or_equal_to(required)

        log.info("Kernel version check passed: %s" % str(kernel_version))

    def after_case(self, log: Logger, **kwargs: Any) -> None:
        # No cleanup required for this read-only validation
        return None
