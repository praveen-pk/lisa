# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from assertpy import assert_that

from lisa import (
    Logger,
    Node,
    TestCaseMetadata,
    TestSuite,
    TestSuiteMetadata,
    simple_requirement,
)
from lisa.features.security_profile import LVBSDevEnabled
from lisa.tools import Dmesg


@TestSuiteMetadata(
    area="lvbs",
    category="functional",
    description="""
    This suite validates that an LVBS VM booted successfully with HEKI enabled.
    HEKI (Hypervisor Enforced Kernel Integrity) locks control registers and
    loads kernel data, both of which are reported in dmesg on a successful boot.
    """,
)
class HekiBoot(TestSuite):
    _HEKI_CONTROL_REGISTERS_LOCKED = "heki-guest: control registers locked"
    _HEKI_LOADED_KERNEL_DATA = "heki-guest: loaded kernel data"

    @TestCaseMetadata(
        description="""
        Verify that the LVBS VM booted with HEKI enabled by checking dmesg for:
        1. 'HEKI-guest: Control registers locked' - confirms control registers
           were locked by the hypervisor.
        2. 'HEKI-guest: Loaded kernel data' - confirms kernel data was loaded
           under HEKI protection.
        """,
        priority=1,
        requirement=simple_requirement(
            supported_features=[LVBSDevEnabled()],
        ),
    )
    def verify_heki_boot(self, node: Node, log: Logger) -> None:
        # Arrange
        dmesg = node.tools[Dmesg]

        # Act
        log.info("Retrieving dmesg output to check for HEKI boot messages...")
        dmesg_output = dmesg.get_output(force_run=True).lower()

        # Assert
        assert_that(dmesg_output).described_as(
            "Expected 'HEKI-guest: Control registers locked' in dmesg, "
            "indicating HEKI locked control registers on boot. "
            "Verify the VM image has HEKI support enabled."
        ).contains(self._HEKI_CONTROL_REGISTERS_LOCKED)

        assert_that(dmesg_output).described_as(
            "Expected 'HEKI-guest: Loaded kernel data' in dmesg, "
            "indicating HEKI loaded kernel data on boot. "
            "Verify the VM image has HEKI support enabled."
        ).contains(self._HEKI_LOADED_KERNEL_DATA)

        log.info(
            "HEKI boot verification passed: control registers locked "
            "and kernel data loaded successfully."
        )
