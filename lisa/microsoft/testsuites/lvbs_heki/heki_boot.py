# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Any

from lisa import (
    Logger,
    Node,
    TestCaseMetadata,
    TestSuite,
    TestSuiteMetadata,
)
from lisa.features.security_profile import SecureBootEnabled
from lisa.sut_orchestrator import AZURE
from lisa.testsuite import simple_requirement
from lisa.tools import Dmesg


@TestSuiteMetadata(
    area="lvbs_heki",
    category="functional",
    description="""
    This test suite verifies Heki (Hardware-Enforced Kernel Integrity)
    functionality on Azure VMs with secure boot enabled.
    """,
)
class HekiBoot(TestSuite):
    @TestCaseMetadata(
        description="""
        Verify that an Azure VM boots correctly with Heki enabled by
        checking for all three required kernel boot messages in dmesg:
        1. "Secure boot enabled" - Confirms secure boot is active
        2. "heki-guest: Control registers locked" - Confirms Heki control registers locked
        3. "heki-guest: Loaded kernel data" - Confirms Heki kernel data loaded

        The three messages can appear in any order in dmesg. All three must
        be present for the test to pass.

        Steps:
        1. Acquire the Dmesg tool from the node
        2. Retrieve full kernel boot messages using dmesg
        3. Assert all three required messages exist in the output
        """,
        priority=0,
        requirement=simple_requirement(
            supported_features=[SecureBootEnabled()],
            supported_platform_type=[AZURE],
        ),
    )
    def verify_heki_boot_messages(self, node: Node, log: Logger) -> None:
        """
        Verify Heki boot messages in kernel dmesg output.

        Args:
            node: The test node running with Heki enabled
            log: Logger instance for test output
        """
        log.info("Starting Heki boot message verification test")

        # Acquire Dmesg tool
        dmesg = node.tools[Dmesg]
        log.debug("Acquired Dmesg tool from node")

        # Get full kernel boot messages
        log.info("Retrieving kernel boot messages from dmesg")
        dmesg_output = dmesg.get_output(force_run=True)
        log.debug(f"Retrieved {len(dmesg_output)} bytes of dmesg output")

        # Define required boot messages
        required_messages = [
            "Secure boot enabled",
            "heki-guest: Control registers locked",
            "heki-guest: Loaded kernel data",
        ]

        # Verify all required messages are present in dmesg
        missing_messages = []
        for message in required_messages:
            if message in dmesg_output:
                log.info(f"✓ Found expected message: '{message}'")
            else:
                log.error(f"✗ Missing expected message: '{message}'")
                missing_messages.append(message)

        # Assert all required messages are present
        assert (
            len(missing_messages) == 0
        ), f"Heki boot verification failed. Missing messages: {missing_messages}"

        log.info("✓ All Heki boot messages verified successfully")
