# SPDX-License-Identifier: BSD-3-Clause
# Copyright(c) 2019 Nippon Telegraph and Telephone Corporation

##################################################
# Basic information
##################################################
Summary: Soft Patch Panel
Name: spp
Version: 18.08.3
Release: 1
License: BSD-3-Clause
URL: http://git.dpdk.org/apps/spp/
Source: http://git.dpdk.org/apps/spp/snapshot/%{name}-%{version}.tar.gz
Group: Applications/File
Prefix: %{_prefix}

##################################################
# Requires
##################################################
BuildRequires: python36 python36-pip python-devel python-six libpcap-devel lz4-devel wireshark-devel
BuildRequires: inkscape texlive-latex latexmk
BuildRequires: dpdk-devel

Requires: lz4 libpcap wireshark python36 python36-pip
Requires: lz4-devel libpcap-devel wireshark-devel libX11-devel
Requires: dpdk

##################################################
# Description
##################################################
%description
The Soft Patch Panel (SPP) is a DPDK application for providing
switching functionality for Service Function Chaining in NFV
(Network Function Virtualization).

##################################################
# Define
##################################################
# Need for make
%define SDK_PATH                /usr/share/dpdk
%define TARGET                  x86_64-native-linuxapp-gcc

# Place of installation
%define INS_PATH                /opt/spp
%define INS_PATH_DOC            /usr/share/doc/spp
%define INS_PATH_LINK           /usr/bin

# Source path
%define SRC_PATH                src

# Tools path
%define TOOLS_PATH              tools
%define HELPS_PATH              %{TOOLS_PATH}/helpers

# Document path
%define DOC_TREE_PATH           docs/guides/_build/doctrees
%define DOC_HTML_PATH           docs/guides/_build/html
%define DOC_LATEX_PATH          docs/guides/_build/latex

# License path
%define LICENSE_PATH            license

# Install path
%define BUILD_INS_PATH          %{buildroot}%{INS_PATH}
%define BUILD_INS_PATH_BIN      %{buildroot}%{INS_PATH}/bin
%define BUILD_INS_PATH_LICENSE  %{buildroot}%{INS_PATH}/%{LICENSE_PATH}
%define BUILD_INS_PATH_HELPS    %{buildroot}%{INS_PATH}/%{HELPS_PATH}
%define BUILD_INS_PATH_DOC      %{buildroot}%{INS_PATH_DOC}
%define BUILD_INS_PATH_LINK     %{buildroot}%{INS_PATH_LINK}

# Target path
%define CLI_PATH                controller
%define CTL_PATH                spp-ctl
%define PRI_PATH                primary/%{TARGET}
%define VF_PATH                 vf/%{TARGET}
%define NFV_PATH                nfv/%{TARGET}
%define MIR_PATH                mirror/%{TARGET}
%define PCAP_PATH               pcap/%{TARGET}

# Python path
%define PYTHON_PATH /usr/lib64/python3.6:/usr/lib64/python3.6/lib-dynload:/usr/local/lib64/python3.6/site-packages:/usr/local/lib/python3.6/site-packages:/usr/lib64/python3.6/site-packages:/usr/lib/python3.6/site-packages

##################################################
# prep section
##################################################
%prep
%setup -q

##################################################
# build section
##################################################
%build
export RTE_SDK=%{SDK_PATH}
export RTE_TARGET=%{TARGET}
export PYTHONPATH=%{PYTHON_PATH}
make
make doc-all

##################################################
# install section
##################################################
%install
# Clearn up
rm -rf %{buildroot}

# Make install directory
mkdir -p %{BUILD_INS_PATH}
mkdir -p %{BUILD_INS_PATH_LICENSE}
mkdir -p %{BUILD_INS_PATH_HELPS}
mkdir -p %{BUILD_INS_PATH_BIN}
mkdir -p %{BUILD_INS_PATH_BIN}/%{PRI_PATH}
mkdir -p %{BUILD_INS_PATH_BIN}/%{VF_PATH}
mkdir -p %{BUILD_INS_PATH_BIN}/%{NFV_PATH}
mkdir -p %{BUILD_INS_PATH_BIN}/%{MIR_PATH}
mkdir -p %{BUILD_INS_PATH_BIN}/%{PCAP_PATH}
mkdir -p %{BUILD_INS_PATH_DOC}
mkdir -p %{BUILD_INS_PATH_LINK}

# File copy
cp README.md                                %{BUILD_INS_PATH}
cp requirements.txt                         %{BUILD_INS_PATH}
cp CONTRIBUTING.txt                         %{BUILD_INS_PATH}

# License copy
cp %{LICENSE_PATH}/*                        %{BUILD_INS_PATH_LICENSE}/

# Execute file copy
cp -r %{SRC_PATH}/%{CLI_PATH}               %{BUILD_INS_PATH_BIN}
cp -r %{SRC_PATH}/%{CTL_PATH}               %{BUILD_INS_PATH_BIN}
cp %{SRC_PATH}/spp.py                       %{BUILD_INS_PATH_BIN}
cp %{SRC_PATH}/%{PRI_PATH}/app/spp_primary  %{BUILD_INS_PATH_BIN}/%{PRI_PATH}
cp %{SRC_PATH}/%{VF_PATH}/app/spp_vf        %{BUILD_INS_PATH_BIN}/%{VF_PATH}
cp %{SRC_PATH}/%{NFV_PATH}/app/spp_nfv      %{BUILD_INS_PATH_BIN}/%{NFV_PATH}
cp %{SRC_PATH}/%{MIR_PATH}/app/spp_mirror   %{BUILD_INS_PATH_BIN}/%{MIR_PATH}
cp %{SRC_PATH}/%{PCAP_PATH}/app/spp_pcap    %{BUILD_INS_PATH_BIN}/%{PCAP_PATH}
cp %{HELPS_PATH}/sec_launcher.py            %{BUILD_INS_PATH_HELPS}

# Document file copy
cp -r %{DOC_TREE_PATH}                      %{BUILD_INS_PATH_DOC}
cp -r %{DOC_HTML_PATH}                      %{BUILD_INS_PATH_DOC}
cp -r %{DOC_LATEX_PATH}                     %{BUILD_INS_PATH_DOC}

# Create symbolic link
ln -sf %{INS_PATH}/bin/spp.py                   %{BUILD_INS_PATH_LINK}/spp
ln -sf %{INS_PATH}/bin/%{CTL_PATH}/spp-ctl      %{BUILD_INS_PATH_LINK}/spp-ctl
ln -sf %{INS_PATH}/bin/%{PRI_PATH}/spp_primary  %{BUILD_INS_PATH_LINK}/spp_primary
ln -sf %{INS_PATH}/bin/%{VF_PATH}/spp_vf        %{BUILD_INS_PATH_LINK}/spp_vf
ln -sf %{INS_PATH}/bin/%{NFV_PATH}/spp_nfv      %{BUILD_INS_PATH_LINK}/spp_nfv
ln -sf %{INS_PATH}/bin/%{MIR_PATH}/spp_mirror   %{BUILD_INS_PATH_LINK}/spp_mirror
ln -sf %{INS_PATH}/bin/%{PCAP_PATH}/spp_pcap    %{BUILD_INS_PATH_LINK}/spp_pcap


##################################################
# post section
##################################################
%post
# python package install
pip3 install -r %{INS_PATH}/requirements.txt

##################################################
# clean section
##################################################
%clean
rm -rf %{buildroot}

##################################################
# files section
##################################################
%files
# Execute files
%dir %{INS_PATH}
%dir %{INS_PATH}/bin
%dir %attr(777,root,root) %{INS_PATH}/bin/%{CLI_PATH}
%dir %{INS_PATH}/bin/%{CTL_PATH}
%dir %{INS_PATH}/bin/primary
%dir %{INS_PATH}/bin/primary/%{TARGET}
%dir %{INS_PATH}/bin/vf
%dir %{INS_PATH}/bin/vf/%{TARGET}
%dir %{INS_PATH}/bin/nfv
%dir %{INS_PATH}/bin/nfv/%{TARGET}
%dir %{INS_PATH}/bin/mirror
%dir %{INS_PATH}/bin/mirror/%{TARGET}
%dir %{INS_PATH}/bin/pcap
%dir %{INS_PATH}/bin/pcap/%{TARGET}
%attr(755,root,root) %{INS_PATH}/bin/spp.py
%attr(755,root,root) %{INS_PATH}/bin/%{CTL_PATH}/spp-ctl
%attr(744,root,root) %{INS_PATH}/bin/%{PRI_PATH}/spp_primary
%attr(744,root,root) %{INS_PATH}/bin/%{VF_PATH}/spp_vf
%attr(744,root,root) %{INS_PATH}/bin/%{NFV_PATH}/spp_nfv
%attr(744,root,root) %{INS_PATH}/bin/%{MIR_PATH}/spp_mirror
%attr(744,root,root) %{INS_PATH}/bin/%{PCAP_PATH}/spp_pcap
%{INS_PATH}/bin/%{CLI_PATH}/*
%{INS_PATH}/bin/%{CTL_PATH}/*.py
%{INS_PATH}/%{TOOLS_PATH}
%{INS_PATH}/%{HELPS_PATH}
%{INS_PATH}/%{LICENSE_PATH}

#Symbolic link files
%{INS_PATH_LINK}/spp
%{INS_PATH_LINK}/spp-ctl
%{INS_PATH_LINK}/spp_primary
%{INS_PATH_LINK}/spp_vf
%{INS_PATH_LINK}/spp_nfv
%{INS_PATH_LINK}/spp_mirror
%{INS_PATH_LINK}/spp_pcap

# Doc files
%doc %{INS_PATH}/README.md
%doc %{INS_PATH}/requirements.txt
%doc %{INS_PATH}/CONTRIBUTING.txt
%doc %{INS_PATH_DOC}

##################################################
# preun section
##################################################
%preun
if [ -e %{INS_PATH} ]; then
    # delete log file
    find %{INS_PATH} -name "*.log" | xargs --no-run-if-empty rm 

    if [ -d %{INS_PATH}/bin/%{CLI_PATH}/log/ ]; then
        rmdir %{INS_PATH}/bin/%{CLI_PATH}/log/
    fi

    # delete python cache
    find %{INS_PATH} -name "*.pyc" | xargs --no-run-if-empty rm 
    find %{INS_PATH} -name "__pycache__" | xargs --no-run-if-empty rmdir
fi

##################################################
# changelog section
##################################################
%changelog
* Fri Sep 27 2019 Yutaka Ogasawara <yutaka.ogasawara@po.ntt-tx.co.jp>
- initial version 18.08.3
