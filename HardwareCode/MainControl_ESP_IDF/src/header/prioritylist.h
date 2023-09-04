#ifndef PRIORITYLIST_H
#define PRIORITYLIST_H


// --> Priority
#define PRIORITY_TX     1
#define PRIORITY_RX     0
#define PRIORITY_COMMAND_DISTRIBUTE     2
#define PRIORITY_SYSTEM_HANDLE          2
#define PRIORITY_CURVE_HANDLE           3
#define PRIORITY_APPROACH_HANDLE        1
#define PRIORITY_CURVE_TEST             0
#define PRIORITY_SCAN                   0


// --> Core
#define CORE_TX         0
#define CORE_RX         0
#define CORE_COMMAND    0
#define CORE_SYSTEM_H   0
#define CORE_CURVE      0
#define CORE_APPROACH   1
#define CORE_CURVE_TEST 1
#define CORE_SCAN       1

// --> Queue param
#define TX_QUENE_LENGTH             6000
#define TX_SINGLE_SIZE              20
#define COMMAND_QUENE_LENGTH        100
#define COMMAND_QUENE_SIZE          50
#define SYSTEMH_QUENE_LENGTH        50
#define SYSTEMH_QUENE_SIZE          50
#define CURVE_QUEUE_LENGTH          20
#define CURVE_QUEUE_SIZE            50
#define APPROACH_QUEUE_LENGTH       100
#define APPROACH_QUEUE_SIZE         50
#define CURVE_TEST_QUEUE_LENGTH     20
#define CURVE_TEST_QUEUE_SIZE       50
#define SCAN_QUEUE_LENGTH           50
#define SCAN_QUEUE_SIZE             20





#endif