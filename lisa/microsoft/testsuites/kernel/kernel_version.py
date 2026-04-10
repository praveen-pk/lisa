# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from assertpy.assertpy import assert_that

from lisa import (
    Logger,
    Node,
    TestCaseMetadata,
    TestSuite,
    TestSuiteMetadata,
    simple_requirement,
)
from lisa.operating_system import BSD, Windows
from lisa.tools import Uname


@TestSuiteMetadata(
    area="kernel",
    category="functional",
    description="""
    This test suite validates the Linux guest kernel version
    meets a minimum required version.
    """,
)
class KernelVersionValidation(TestSuite):
    @TestCaseMetadata(
        description="""
        Verify the Linux guest kernel version is >= 6.18.
        Steps:
        1. Retrieve kernel version using the Uname tool.
        2. Assert the kernel version is greater than or equal to 6.18.0.
        """,
        priority=2,
        requirement=simple_requirement(
            unsupported_os=[Windows, BSD],
        ),
    )
    def verify_kernel_version_minimum(self, node: Node, log: Logger) -> None:
        # --- Arrange ---
        uname = node.tools[Uname]

        # --- Act ---
        uname_result = uname.get_linux_information()
        log.info(
            f"Detected kernel version: {uname_result.kernel_version_raw}"
        )

        # --- Assert ---
        assert_that(uname_result.kernel_version >= "6.18.0").described_as(
            f"Kernel version {uname_result.kernel_version_raw} is below the"
            f" minimum required version 6.18. Ensure the guest is running"
            f" a kernel >= 6.18."
        ).is_true()

        log.info("Kernel version meets the minimum requirement of 6.18.")
