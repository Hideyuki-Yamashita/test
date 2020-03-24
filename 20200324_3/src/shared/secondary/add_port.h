/* SPDX-License-Identifier: BSD-3-Clause
 * Copyright(c) 2015-2016 Intel Corporation
 * Copyright(c) 2019 Nippon Telegraph and Telephone Corporation
 */

#ifndef _SHARED_SECONDARY_ADD_PORT_H_
#define _SHARED_SECONDARY_ADD_PORT_H_

// The number of receive descriptors to allocate for the receive ring.
#define NR_DESCS 128

#define VHOST_IFACE_NAME "/tmp/sock%u"
#define VHOST_BACKEND_NAME "spp_vhost%u"

#define PCAP_PMD_DEV_NAME "eth_pcap%u"
#define MEMIF_PMD_DEV_NAME "net_memif%u"
#define NULL_PMD_DEV_NAME "eth_null%u"

#define PCAP_IFACE_RX "/tmp/spp-rx%d.pcap"
#define PCAP_IFACE_TX "/tmp/spp-tx%d.pcap"

/**
 * SPP provides memif for other processes as "master" role and via socket
 * file "/tmp/spp-memif.sock". Details of memif is described in here.
 * https://doc.dpdk.org/guides/nics/memif.html
 */
#define MEMIF_ROLE "master"
#define MEMIF_SOCK "/tmp/spp-memif.sock"

#define RTE_LOGTYPE_SHARED RTE_LOGTYPE_USER1

/**
 * Get unique name used to reserve vhost interface.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique name with VHOST_BACKEND_NAME and ID.
 *   e.g. `eth_vhost0`
 */
char *
get_vhost_backend_name(unsigned int id);

/**
 * Get vhost name as the path of sock device.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique name with VHOST_IFACE_NAME and ID.
 *   e.g. `tmp/sock0`
 */
char *
get_vhost_iface_name(unsigned int id);

/**
 * Create a ring PMD with given ring_id.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique port ID
 */
int
add_ring_pmd(int ring_id);

/**
 * Create a vhost PMD with given ring_id.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique port ID
 */
int
add_vhost_pmd(int index);

/**
 * Create a PCAP PMD with given ring_id.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique port ID
 */
int
add_pcap_pmd(int index);

/**
 * Create a memif PMD with given ID.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique port ID
 */
int
add_memif_pmd(int index);

/**
 * Create a null PMD with given ID.
 *
 * @param port_id
 *   ID of the next possible valid port.
 * @return
 *   Unique port ID
 */
int
add_null_pmd(int index);

#endif
