# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

from spack.main import SpackCommand

audit = SpackCommand('audit')


@pytest.mark.parametrize('pkgs,expected_returncode', [
    # A single package with issues, should exit 1
    (['wrong-variant-in-conflicts'], 1),
    # A "sane" package should exit 0
    (['mpileaks'], 0),
    # A package with issues and a package without should exit 1
    (['wrong-variant-in-conflicts', 'mpileaks'], 1),
    (['mpileaks', 'wrong-variant-in-conflicts'], 1),
])
def test_audit_packages(
        pkgs, expected_returncode, mutable_config, mock_packages
):
    """Sanity check ``spack audit packages`` to make sure it works."""
    audit('packages', *pkgs, fail_on_error=False)
    assert audit.returncode == expected_returncode


def test_audit_configs(mutable_config, mock_packages):
    """Sanity check ``spack audit packages`` to make sure it works."""
    audit('configs', fail_on_error=False)
    # The mock configuration has duplicate definitions of some compilers
    assert audit.returncode == 1