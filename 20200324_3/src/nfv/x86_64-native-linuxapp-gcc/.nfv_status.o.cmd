cmd_nfv_status.o = gcc -Wp,-MD,./.nfv_status.o.d.tmp  -m64 -pthread -I/home/tx_h-yamashita/dpdk-19.11/lib/librte_eal/linux/eal/include  -march=native -DRTE_MACHINE_CPUFLAG_SSE -DRTE_MACHINE_CPUFLAG_SSE2 -DRTE_MACHINE_CPUFLAG_SSE3 -DRTE_MACHINE_CPUFLAG_SSSE3 -DRTE_MACHINE_CPUFLAG_SSE4_1 -DRTE_MACHINE_CPUFLAG_SSE4_2 -DRTE_MACHINE_CPUFLAG_AES -DRTE_MACHINE_CPUFLAG_PCLMULQDQ -DRTE_MACHINE_CPUFLAG_AVX -DRTE_MACHINE_CPUFLAG_RDRAND -DRTE_MACHINE_CPUFLAG_FSGSBASE -DRTE_MACHINE_CPUFLAG_F16C -DRTE_MACHINE_CPUFLAG_AVX2  -I/home/tx_h-yamashita/spp/src/nfv/x86_64-native-linuxapp-gcc/include -DRTE_USE_FUNCTION_VERSIONING -I/home/tx_h-yamashita/dpdk-19.11/x86_64-native-linuxapp-gcc/include -include /home/tx_h-yamashita/dpdk-19.11/x86_64-native-linuxapp-gcc/include/rte_config.h -D_GNU_SOURCE -DALLOW_EXPERIMENTAL_API -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wold-style-definition -Wpointer-arith -Wcast-align -Wnested-externs -Wcast-qual -Wformat-nonliteral -Wformat-security -Wundef -Wwrite-strings -Wdeprecated -Wimplicit-fallthrough=2 -Wno-format-truncation -Wno-address-of-packed-member -O3 -MMD -I/home/tx_h-yamashita/spp/src/nfv/../    -o nfv_status.o -c /home/tx_h-yamashita/spp/src/nfv/nfv_status.c 
