..  SPDX-License-Ident   ifier: BSD-3-Clause
    Copyright(c) 2017-2019 Nippon Telegraph and Telephone Corporation


.. _setup_install_rpm_dpdk_spp:

Install DPDK and SPP
====================

Before setting up SPP, you need to install DPDK.
In this document, briefly described how to install and setup DPDK.
Refer to `DPDK documentation
<https://dpdk.org/doc/guides/>`_ for more details.
For Linux, see `Getting Started Guide for Linux
<http://www.dpdk.org/doc/guides/linux_gsg/index.html>`_ .

.. _setup_install_packages:

Required Packages
-----------------

Installing packages for DPDK and SPP is almost the on Ubunu and CentOS,
but names are different for some packages.

When installing SPP and DPDK using RPM package,
please follow the instruction described in
:ref:`Install using RPM<rpm_install_dpdk_spp>`.


Ubuntu
~~~~~~

To compile DPDK, it is required to install following packages.

.. code-block:: console

    $ sudo apt install libnuma-dev \
      libarchive-dev \
      build-essential

You also need to install linux-headers of your kernel version.

.. code-block:: console

    $ sudo apt install linux-headers-$(uname -r)

Some of SPP secondary processes depend on other libraries and you fail to
compile SPP without installing them.

SPP provides libpcap-based PMD for dumping packet to a file or retrieve
it from the file.
``spp_nfv`` and ``spp_pcap`` use ``libpcap-dev`` for packet capture.
``spp_pcap`` uses ``liblz4-dev`` and ``liblz4-tool`` to compress PCAP file.

.. code-block:: console

   $ sudo apt install libpcap-dev \
     liblz4-dev \
     liblz4-tool

``text2pcap`` is also required for creating pcap file which
is included in ``wireshark``.

.. code-block:: console

    $ sudo apt install wireshark


CentOS
~~~~~~

Before installing packages for DPDK, you should add
`IUS Community repositories
<https://ius.io/GettingStarted/>`_
with yum command.

.. code-block:: console
  
    $ sudo yum install https://centos7.iuscommunity.org/ius-release.rpm

To compile DPDK, required to install following packages.

.. code-block:: console

    $ sudo yum install numactl-devel \
      libarchive-devel \
      kernel-headers \
      kernel-devel

As same as Ubuntu, you should install additional packages because
SPP provides libpcap-based PMD for dumping packet to a file or retrieve
it from the file.
``spp_nfv`` and ``spp_pcap`` use ``libpcap-dev`` for packet capture.
``spp_pcap`` uses ``liblz4-dev`` and ``liblz4-tool`` to compress PCAP file.
``text2pcap`` is also required for creating pcap file which is included in ``wireshark``.

.. code-block:: console

   $ sudo apt install libpcap-dev \
     libpcap \
     libpcap-devel \
     lz4 \
     lz4-devel \
     wireshark \
     wireshark-devel \
     libX11-devel


.. _setup_install_dpdk:

DPDK
----

Clone repository and compile DPDK in any directory.

.. code-block:: console

    $ cd /path/to/any
    $ git clone http://dpdk.org/git/dpdk

Installing on Ubuntu and CentOS are almost the same, but required packages
are just bit different.

PCAP is disabled by default in DPDK configuration.
``CONFIG_RTE_LIBRTE_PMD_PCAP`` and ``CONFIG_RTE_PORT_PCAP`` defined in
config file ``common_base`` should be changed to ``y`` to enable PCAP.

.. code-block:: console

    # dpdk/config/common_base
    CONFIG_RTE_LIBRTE_PMD_PCAP=y
    ...
    CONFIG_RTE_PORT_PCAP=y

Compile DPDK with target environment.

.. code-block:: console

    $ cd dpdk
    $ export RTE_SDK=$(pwd)
    $ export RTE_TARGET=x86_64-native-linuxapp-gcc  # depends on your env
    $ make install T=$RTE_TARGET


PCAP is disabled by default in DPDK configuration, so should be changed
if you use this feature.
``CONFIG_RTE_LIBRTE_PMD_PCAP`` and ``CONFIG_RTE_PORT_PCAP`` defined in
config file ``common_base`` should be changed to ``y`` to enable PCAP.

.. code-block:: console

    # dpdk/config/common_base
    CONFIG_RTE_LIBRTE_PMD_PCAP=y
    ...
    CONFIG_RTE_PORT_PCAP=y

Compile DPDK with options for target environment.

.. code-block:: console

    $ cd dpdk
    $ export RTE_SDK=$(pwd)
    $ export RTE_TARGET=x86_64-native-linuxapp-gcc  # depends on your env
    $ make install T=$RTE_TARGET


Pyhton
------

Python3 and pip3 are also required because SPP controller is implemented
in Pyhton3. Required packages can be installed from ``requirements.txt``.

.. code-block:: console

    # Ubuntu
    $ sudo apt install python3 \
      python3-pip

For CentOS, you need to specify minor version of python3.
Here is an example of installing python3.6.

.. code-block:: console

    # CentOS
    $ sudo yum install python36 \
      python36-pip

SPP provides ``requirements.txt`` for installing required packages of Python3.
You might fail to run ``pip3`` without sudo on some environments.

.. code-block:: console

    $ pip3 install -r requirements.txt

For some environments, ``pip3`` might install packages under your home
directory ``$HOME/.local/bin`` and you should add it to ``$PATH`` environment
variable.


.. _setup_install_spp:

SPP
---

Clone SPP repository and compile it in any directory.

.. code-block:: console

    $ cd /path/to/any
    $ git clone http://dpdk.org/git/apps/spp
    $ cd spp
    $ make  # Confirm that $RTE_SDK and $RTE_TARGET are set

If you use ``spp_mirror`` in deep copy mode,
which is used for cloning whole of packet data for modification,
you should change configuration of copy mode in Makefile of ``spp_mirror``
before.
It is for copying full payload into a new mbuf.
Default mode is shallow copy.

.. code-block:: console

    # src/mirror/Makefile
    #CFLAGS += -Dspp_mirror_SHALLOWCOPY

.. note::

    Before run make command, you might need to consider if using deep copy
    for cloning packets in ``spp_mirror``. Comparing with shallow copy, it
    clones entire packet payload into a new mbuf and it is modifiable,
    but lower performance. Which of copy mode should be chosen depends on
    your usage.


Binding Network Ports to DPDK
-----------------------------

Network ports must be bound to DPDK with a UIO (Userspace IO) driver.
UIO driver is for mapping device memory to userspace and registering
interrupts.

UIO Drivers
~~~~~~~~~~~

You usually use the standard ``uio_pci_generic`` for many use cases
or ``vfio-pci`` for more robust and secure cases.
Both of drivers are included by default in modern Linux kernel.

.. code-block:: console

    # Activate uio_pci_generic
    $ sudo modprobe uio_pci_generic

    # or vfio-pci
    $ sudo modprobe vfio-pci

You can also use kmod included in DPDK instead of ``uio_pci_generic``
or ``vfio-pci``.

.. code-block:: console

    $ sudo modprobe uio
    $ sudo insmod kmod/igb_uio.ko

Binding Network Ports
~~~~~~~~~~~~~~~~~~~~~

Once UIO driver is activated, bind network ports with the driver.
DPDK provides ``usertools/dpdk-devbind.py`` for managing devices.

Find ports for binding to DPDK by running the tool with ``-s`` option.

.. code-block:: console

    $ $RTE_SDK/usertools/dpdk-devbind.py --status

    Network devices using DPDK-compatible driver
    ============================================
    <none>

    Network devices using kernel driver
    ===================================
    0000:29:00.0 '82571EB ... 10bc' if=enp41s0f0 drv=e1000e unused=
    0000:29:00.1 '82571EB ... 10bc' if=enp41s0f1 drv=e1000e unused=
    0000:2a:00.0 '82571EB ... 10bc' if=enp42s0f0 drv=e1000e unused=
    0000:2a:00.1 '82571EB ... 10bc' if=enp42s0f1 drv=e1000e unused=

    Other Network devices
    =====================
    <none>
    ....

You can find network ports are bound to kernel driver and not to DPDK.
To bind a port to DPDK, run ``dpdk-devbind.py`` with specifying a driver
and a device ID.
Device ID is a PCI address of the device or more friendly style like
``eth0`` found by ``ifconfig`` or ``ip`` command..

.. code-block:: console

    # Bind a port with 2a:00.0 (PCI address)
    ./usertools/dpdk-devbind.py --bind=uio_pci_generic 2a:00.0

    # or eth0
    ./usertools/dpdk-devbind.py --bind=uio_pci_generic eth0


After binding two ports, you can find it is under the DPDK driver and
cannot find it by using ``ifconfig`` or ``ip``.

.. code-block:: console

    $ $RTE_SDK/usertools/dpdk-devbind.py -s

    Network devices using DPDK-compatible driver
    ============================================
    0000:2a:00.0 '82571EB ... 10bc' drv=uio_pci_generic unused=vfio-pci
    0000:2a:00.1 '82571EB ... 10bc' drv=uio_pci_generic unused=vfio-pci

    Network devices using kernel driver
    ===================================
    0000:29:00.0 '...' if=enp41s0f0 drv=e1000e unused=vfio-pci,uio_pci_generic
    0000:29:00.1 '...' if=enp41s0f1 drv=e1000e unused=vfio-pci,uio_pci_generic

    Other Network devices
    =====================
    <none>
    ....


Confirm DPDK is setup properly
------------------------------

For testing, you can confirm if you are ready to use DPDK by running
DPDK's sample application. ``l2fwd`` is good example to confirm it
before SPP because it is very similar to SPP's worker process for forwarding.

.. code-block:: console

   $ cd $RTE_SDK/examples/l2fwd
   $ make
     CC main.o
     LD l2fwd
     INSTALL-APP l2fwd
     INSTALL-MAP l2fwd.map

In this case, run this application simply with just two options
while DPDK has many kinds of options.

  * ``-l``: core list
  * ``-p``: port mask

.. code-block:: console

   $ sudo ./build/app/l2fwd \
     -l 1-2 \
     -- -p 0x3

It must be separated with ``--`` to specify which option is
for EAL or application.
Refer to `L2 Forwarding Sample Application
<https://dpdk.org/doc/guides/sample_app_ug/l2_forward_real_virtual.html>`_
for more details.


Build Documentation
-------------------

This documentation is able to be built as HTML and PDF formats from make
command. Before compiling the documentation, you need to install some of
packages required to compile.

For HTML documentation, install sphinx and additional theme.

.. code-block:: console

    $ pip3 install sphinx \
      sphinx-rtd-theme

For PDF, inkscape and latex packages are required.

.. code-block:: console

    # Ubuntu
    $ sudo apt install inkscape \
      texlive-latex-extra \
      texlive-latex-recommended

.. code-block:: console

    # CentOS
    $ sudo yum install inkscape \
      texlive-latex

You might also need to install ``latexmk`` in addition to if you use
Ubuntu 18.04 LTS.

.. code-block:: console

    $ sudo apt install latexmk

HTML documentation is compiled by running make with ``doc-html``. This
command launch sphinx for compiling HTML documents.
Compiled HTML files are created in ``docs/guides/_build/html/`` and
You can find the top page ``index.html`` in the directory.

.. code-block:: console

    $ make doc-html

PDF documentation is compiled with ``doc-pdf`` which runs latex for.
Compiled PDF file is created as ``docs/guides/_build/html/SoftPatchPanel.pdf``.

.. code-block:: console

    $ make doc-pdf

You can also compile both of HTML and PDF documentations with ``doc`` or
``doc-all``.

.. code-block:: console

    $ make doc
    # or
    $ make doc-all

.. note::

    For CentOS, compilation PDF document is not supported.

.. _setup_install ();


Build RPM Packeages
-------------------

This section describes how to build/install/uninstall rpms of both DPDK and
SPP.

.. _setup_install_rpm_build_requirements:

Build Environment
~~~~~~~~~~~~~~~~~
The following step is for installing tools for building RPM package.

.. code-block:: console

        $ sudo yum groupinstall "Development Tools"
        $ sudo yum install rpm-build rpmdevtools

.. _setup_install_rpm_dpdk:

DPDK
~~~~

.. _setup_install_rpm_dpdk_build:

Build RPM
^^^^^^^^^

Create base directory for building DPDK RPM.
This manual assumes the user uses home directory as base directory.
It is allowed for user to choose arbitary directory as base directory.

.. code-block:: console

        $ mkdir ~/rpmbuild
        $ cd ~/rpmbuild

Download spec file of DPDK.

.. code-block:: console

        $ mkdir -p rpmbuild/SPECS
        $ wget -P rpmbuild/SPECS \n
	http://git.dpdk.org/dpdk-stable/plain/pkg/dpdk.spec
        $ cd ~/rpmbuild

Download source file of DPDK.

.. code-block:: console

        $ mkdir -p rpmbuild/SOURCES
        $ wget -P rpmbuild/SOURCES https://fast.dpdk.org/rel/dpdk-18.08.1.tar.xz
        $ cd ~/rpmbuild

Further down, modify the content of SPECS/dpdk.spec.

.. code-block:: console

        $ vi SPECS/dpdk.spec

Change the version number of the source code.

.. code-block:: none

        Version: 17.11

is replaced by the following.

.. note::
        The version number corresponds to that of downloaded DPDK

.. code-block:: none

        Version: 18.08.1

Change the URL of the source code.

.. code-block:: none

        Source: http://dpdk.org/browse/dpdk/snapshot/dpdk-%{version}.tar.gz

is replaced by the following.

.. code-block:: none

        Source: https://fast.dpdk.org/rel/dpdk-%{version}.tar.xz

Add -n option to specify source directory.

.. code-block:: none

        %setup -q

is replaced by the following.

.. code-block:: none

        %setup -q -n %{name}-stable-%{version}

Modify the build target.

.. code-block:: none

        ExclusiveArch: i686 x86_64 aarch64
        %ifarch aarch64
        %global machine armv8a
        %global target arm64-%{machine}-linuxapp-gcc
        %global config arm64-%{machine}-linuxapp-gcc
        %else
        %global machine default
        %global target %{_arch}-%{machine}-linuxapp-gcc
        %global config %{_arch}-native-linuxapp-gcc
        %endif

is replaced by the following.

.. code-block:: none

        ExclusiveArch: x86_64
        %global machine native
        %global target %{_arch}-%{machine}-linuxapp-gcc
        %global config %{_arch}-native-linuxapp-gcc

Change dependency files when building RPM.

.. code-block:: none

        BuildRequires: kernel-devel, kernel-headers, libpcap-devel
        BuildRequires: doxygen, python-sphinx, inkscape
        BuildRequires: texlive-collection-latexextra

is replaced by the following.

.. code-block:: none

        BuildRequires: kernel-devel, kernel-headers, libpcap-devel
        BuildRequires: doxygen, python-sphinx, inkscape
        # BuildRequires: texlive-collection-latexextra
        BuildRequires: numactl-devel wireshark texlive texlive-latex
        BuildRequires: texlive-xetex texlive-collection-xetex latexmk

Add last 3 lines to specify PMD driver directory.

.. code-block:: none

        %build
        make O=%{target} T=%{config} config
        sed -ri 's,(RTE_MACHINE=).*,\1%{machine},' %{target}/.config
        sed -ri 's,(RTE_APP_TEST=).*,\1n,'         %{target}/.config
        sed -ri 's,(RTE_BUILD_SHARED_LIB=).*,\1y,' %{target}/.config
        sed -ri 's,(RTE_NEXT_ABI=).*,\1n,'         %{target}/.config
        sed -ri 's,(LIBRTE_VHOST=).*,\1y,'         %{target}/.config
        sed -ri 's,(LIBRTE_PMD_PCAP=).*,\1y,'      %{target}/.config

is replaced by the following.

.. code-block:: none

 %build
 make O=%{target} T=%{config} config
 sed -ri 's,(RTE_MACHINE=).*,\1%{machine},' %{target}/.config
 sed -ri 's,(RTE_APP_TEST=).*,\1n,'         %{target}/.config
 sed -ri 's,(RTE_BUILD_SHARED_LIB=).*,\1y,' %{target}/.config
 sed -ri 's,(RTE_NEXT_ABI=).*,\1n,'         %{target}/.config
 sed -ri 's,(LIBRTE_VHOST=).*,\1y,'         %{target}/.config
 sed -ri 's,(LIBRTE_PMD_PCAP=).*,\1y,'      %{target}/.config
 sed -ri 's,(CONFIG_RTE_LIBRTE_PMD_PCAP=).*,\1y,' %{target}/.config
 sed -ri 's,(CONFIG_RTE_PORT_PCAP=).*,\1y,'       %{target}/.config
 sed -ri 's,(CONFIG_RTE_EAL_PMD_PATH=).*,\1\"%{_libdir}/dpdk\",' %{target}/.config

Add 4 lines to move PMD driver files to specific directory.

.. code-block:: none

        %install
        rm -rf %{buildroot}
        make install O=%{target} DESTDIR=%{buildroot} \
        prefix=%{_prefix} bindir=%{_bindir} sbindir=%{_sbindir} \
        includedir=%{_includedir}/dpdk libdir=%{_libdir} \
        datadir=%{_datadir}/dpdk docdir=%{_docdir}/dpdk

is replaced by the following.

.. code-block:: none

    %install
    rm -rf %{buildroot}
    make install O=%{target} DESTDIR=%{buildroot} \
    prefix=%{_prefix} bindir=%{_bindir} sbindir=%{_sbindir} \
    includedir=%{_includedir}/dpdk libdir=%{_libdir} \
    datadir=%{_datadir}/dpdk docdir=%{_docdir}/dpdk
    mkdir %{buildroot}%{_libdir}/dpdk
    mv %{buildroot}%{_libdir}/librte_pmd_* %{buildroot}%{_libdir}/dpdk
    mv %{buildroot}%{_libdir}/dpdk/librte_pmd_ring* %{buildroot}%{_libdir}/
    mv %{buildroot}%{_libdir}/dpdk/librte_pmd_vhost* %{buildroot}%{_libdir}/


Install epel repository.

.. code-block:: console

        $ sudo rpm -ivh \
        https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

Install dependency files when building.

.. code-block:: console

        $ sudo yum install python-pip kernel-devel kernel-headers \
        libpcap-devel doxygen python-sphinx inkscape numactl-devel \
        kernel-devel-$(uname -r) wireshark
        $ sudo yum install texlive texlive-latex texlive-xetex \
        texlive-collection-xetex texlive-*.noarch latexmk

Install python packages to build documents.

.. code-block:: console

        $ sudo pip install sphinx==1.3.1 sphinx_rtd_theme

Build RPMS.

.. code-block:: console

        $ rpmbuild -ba SPECS/dpdk.spec

When build is completed, the following 3 files will be generated.

.. code-block:: console

        $ ls ~/rpmbuild/RPMS/x86_64/

        dpdk-18.08.1-1.x86_64.rpm
        dpdk-debuginfo-18.08.1-1.x86_64.rpm
        dpdk-devel-18.08.1-1.x86_64.rpm

.. _setup_install_rpm_dpdk:

Install
^^^^^^^

Use RPM which is built by the previous step.

.. code-block:: console

        $ mv /path/to/any/dpdk-18.08.1-1.x86_64.rpm ~/

Install DPDK including its dependency files via `yum localinstall` command.

.. code-block:: console

        $ cd ~/
        $ sudo yum localinstall dpdk-18.08.1-1.x86_64.rpm

.. note::
        Above sample assumes `dpdk-18.08.1-1.x86_64.rpm` is built by
        previous steps.
        You can change the name of RPM by modifying DPDK spec file.

.. _rpm_uninstall_dpdk:

Uninstall
^^^^^^^^^
You can uninstall DPDK using `yum erase` command.

.. code-block:: console

        $ sudo yum erase dpdk

.. _spp_uninstall__dpdk:

Build, install and uninstall SPP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. note::
        Because the version of python and sphinx used for build of DPDK and SPP
        is different, environment for building DPDK and SPP should be
        different.

.. _rpm_build_spp:

Build RPM
^^^^^^^^^
Create base directory for building SPP RPM.

.. code-block:: console

        $ mkdir ~/rpmbuild
        $ cd ~/rpmbuild

Download spec file of SPP.

.. code-block:: console

        $ mkdir SPECS
        $ cd SPECS
        $ wget http://git.dpdk.org/apps/spp/plain/spec/spp.spec
        $ cd ~/rpmbuild

Download source file of SPP.

.. code-block:: console

        $ mkdir SOURCES
        $ cd SOURCES
        $ wget http://git.dpdk.org/apps/spp/snapshot/spp-18.08.3.tar.gz
        $ cd ~/rpmbuild

.. note::
        If you use newer version of spp, please modify the following part
        of spp.spec.Please align the version number which is downloaded
        via above mentioned step.

.. code-block:: none

        Version: 19.11

Install DPDK RPMs required for building SPP.

.. code-block:: console

        $ mv /path/to/any/dpdk-devel-18.08.1-1.x86_64.rpm ~/
        $ mv /path/to/any/dpdk-18.08.1-1.x86_64.rpm ~/
        $ cd ~/
        $ sudo yum localinstall dpdk-devel-18.08.1-1.x86_64.rpm \
        dpdk-18.08.1-1.x86_64.rpm

Install epel repository.

.. code-block:: console

        $ sudo rpm -ivh \
        https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

Install dependency files for building SPP.

.. code-block:: console

        $ sudo yum install python36 python36-pip python-devel \
        python-six libpcap-devel lz4-devel wireshark-devel
        $ sudo yum install inkscape texlive-latex latexmk  texlive-*.noarch

Install python packages.

.. code-block:: console

        $ sudo pip3 install sphinx sphinx-rtd-theme

Install sty files for building documents.

.. code-block:: console

        $ cd /tmp

        # tabulary.sty
        $ wget http://mirrors.ctan.org/macros/latex/contrib/tabulary.zip
        $ unzip tabulary.zip
        $ cd tabulary
        $ latex tabulary.ins
        $ cd ../
        $ sudo mv tabulary /usr/share/texlive/texmf-dist/tex/latex/

        # capt-of.sty
        $ wget http://mirrors.ctan.org/macros/latex/contrib/capt-of.zip
        $ unzip capt-of.zip
        $ cd capt-of
        $ latex capt-of.ins
        $ cd ../
        $ sudo mv capt-of /usr/share/texlive/texmf-dist/tex/latex/

        # needspace.sty
        $ wget http://mirrors.ctan.org/macros/latex/contrib/needspace.zip
        $ unzip needspace.zip
        $ cd needspace
        $ latex needspace.ins
        $ cd ../
        $ sudo mv needspace /usr/share/texlive/texmf-dist/tex/latex/

        # Registration
        $ sudo texhash

Start building SPP RPM.

.. code-block:: console

        $ cd ~/rpmbuild
        $ rpmbuild -ba SPECS/spp.spec

When build is completed, the following 2 files will be generated.

.. code-block:: console

        $ ls ~/rpmbuild/RPMS/x86_64/

        spp-18.08.3-1.x86_64.rpm
        spp-debuginfo-18.08.3-1.x86_64.rpm

.. _rpm_install_spp:

Install
^^^^^^^
Install epel reposiitory to resolve dependency of SPP RPM.

.. code-block:: console

        $ sudo rpm -ivh \
        https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

Use RPM which is built by the previous step.

.. code-block:: console

        $ mv /path/to/any/spp-18.08.3-1.x86_64.rpm ~/

Install SPP including its dependency files via `yum localinstall` command.

.. code-block:: console

        $ sudo yum localinstall spp-18.08.3-1.x86_64.rpm

.. note::
        Above sample assumes `spp-18.08.3-1.x86_64.rpm` is built by
        previous steps. You can change the name of RPM by modifying
        SPP spec file.

.. note::
        This section assumes DPDK is already installed using DPDK RPM.

.. note::
        If SPP is installed via RPM, process can be started without
        specifying path.

.. _rpm_uninstall_spp:

Uninstall
^^^^^^^^^
You can uninstall SPP using `yum erase` command.

.. code-block:: console

        $ sudo yum erase spp

.. note::
        Above command does NOT uninstall DPDK.
