# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RocprofilerDev(CMakePackage):
    """ROCPROFILER library for AMD HSA runtime API extension support"""

    homepage = "https://github.com/ROCm-Developer-Tools/rocprofiler"
    git      = "https://github.com/ROCm-Developer-Tools/rocprofiler.git"
    url      = "https://github.com/ROCm-Developer-Tools/rocprofiler/archive/rocm-4.2.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.2.0', sha256='c5888eda1404010f88219055778cfeb00d9c21901e172709708720008b1af80f')
    version('4.1.0', sha256='2eead5707016da606d636b97f3af1c98cb471da78659067d5a77d4a2aa43ef4c')
    version('4.0.0', sha256='e9960940d1ec925814a0e55ee31f5fc2fb23fa839d1c6a909f72dd83f657fb25')
    version('3.10.0', sha256='fbf5ce9fbc13ba2b3f9489838e00b54885aba92336f055e8b03fef3e3347071e')
    version('3.9.0', sha256='f07ddd9bf2f86550c8d243f887e9bde9d4f2ceec81ecc6393012aaf2a45999e8')
    version('3.8.0', sha256='38ad3ac20f60f3290ce750c34f0aad442354b1d0a56b81167a018e44ecdf7fff')
    version('3.7.0', sha256='d3f03bf850cbd86ca9dfe6e6cc6f559d8083b0f3ea4711d8260b232cb6fdd1cc')
    version('3.5.0', sha256='c42548dd467b7138be94ad68c715254eb56a9d3b670ccf993c43cd4d43659937')

    depends_on('cmake@3:', type='build')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0']:
        depends_on('hsakmt-roct@' + ver, when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, when='@' + ver)
        depends_on('rocminfo@' + ver, when='@' + ver)
        depends_on('roctracer-dev-api@' + ver, when='@' + ver)

    # See https://github.com/ROCm-Developer-Tools/rocprofiler/pull/50
    patch('fix-includes.patch')

    def patch(self):
        filter_file('${HSA_RUNTIME_LIB_PATH}/../include',
                    '${HSA_RUNTIME_LIB_PATH}/../include ${HSA_KMT_LIB_PATH}/..\
                     /include', 'test/CMakeLists.txt', string=True)

    def cmake_args(self):
        return [
            self.define(
                'PROF_API_HEADER_PATH',
                self.spec['roctracer-dev-api'].prefix.roctracer.inc.ext
            ),
            self.define('ROCM_ROOT_DIR', self.spec['hsakmt-roct'].prefix.include)
        ]
