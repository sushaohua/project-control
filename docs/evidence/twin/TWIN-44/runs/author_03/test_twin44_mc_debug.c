/**
 * @file test_twin44_mc_debug.c
 * @brief Independent verification test suite for TWIN-44 (USART2 921600 & USART1 [MC-DBG] Ring Buffer).
 * Task ID: TWIN-44
 * Role: ENG-MC
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include <sys/mman.h>

#include "minimc_proto.h"
#include "planner.h"
#include "thermistor.h"

/* Mock Marlin globals */
volatile float current_position[NUM_AXIS];
volatile bool axis_known_position[3];
volatile int16_t current_temperature_bed = 25;
volatile int16_t current_temperature_ex1 = 25;
uint8_t is_paused = 0U;
float bed_level[AUTO_BED_LEVELING_GRID_POINTS][AUTO_BED_LEVELING_GRID_POINTS];
static uint8_t s_mock_moves_planned = 0U;

uint8_t movesplanned(void)
{
    return s_mock_moves_planned;
}

/* Mock hardware state */
volatile uint8_t usart2_tx_busy = 0U;
static bool s_dma_auto_clear_busy = true;
static bool s_forward_send_ok = true;
static uint32_t s_mock_tick_ms = 1000U;
static uint32_t s_usart2_baud = 115200U;
static uint32_t s_usart2_disable_cnt = 0U;
static uint32_t s_usart2_enable_cnt = 0U;
static flag_status s_usart1_tdbe = SET;
static char s_usart1_tx_capture[8192];
static size_t s_usart1_tx_len = 0U;
static uint8_t s_mock_th_rx_buf[64];
static uint16_t s_mock_th_rx_len = 0U;
static uint8_t s_last_ap_tx_frame[MINIMC_MAX_FRAME_SIZE];
static uint16_t s_last_ap_tx_len = 0U;
static uint32_t s_ap_tx_count = 0U;
static uint8_t s_test_seq = 0U;

void dma_channel_enable(dma_channel_type *dma_channel, confirm_state new_state)
{
    if ((dma_channel == DMA1_CHANNEL2) && (new_state == TRUE))
    {
        const uint16_t len = (uint16_t)DMA1_CHANNEL2->dtcnt;
        const uint8_t *src = (const uint8_t *)(uintptr_t)DMA1_CHANNEL2->maddr;
        if ((src != NULL) && (len > 0U) && (len <= MINIMC_MAX_FRAME_SIZE))
        {
            memcpy(s_last_ap_tx_frame, src, len);
            s_last_ap_tx_len = len;
            s_ap_tx_count++;
        }
        if (s_dma_auto_clear_busy)
        {
            usart2_tx_busy = 0U;
        }
    }
}

void usart_enable(usart_type *usart_x, confirm_state new_state)
{
    if (usart_x == USART2)
    {
        if (new_state == FALSE)
        {
            s_usart2_disable_cnt++;
        }
        else
        {
            s_usart2_enable_cnt++;
        }
    }
}

void usart_init(usart_type *usart_x, uint32_t baud_rate,
                usart_data_bit_num_type data_bit, usart_stop_bit_num_type stop_bit)
{
    if (usart_x == USART2)
    {
        assert(data_bit == USART_DATA_8BITS);
        assert(stop_bit == USART_STOP_1_BIT);
        s_usart2_baud = baud_rate;
    }
}

flag_status usart_flag_get(usart_type *usart_x, uint32_t flag)
{
    (void)usart_x;
    (void)flag;
    return s_usart1_tdbe;
}

void usart_data_transmit(usart_type *usart_x, uint16_t data)
{
    if ((usart_x == USART1) && (s_usart1_tx_len + 1U < sizeof(s_usart1_tx_capture)))
    {
        s_usart1_tx_capture[s_usart1_tx_len] = (char)(data & 0xFFU);
        s_usart1_tx_len++;
        s_usart1_tx_capture[s_usart1_tx_len] = '\0';
    }
}

uint8_t forward_uart_rx_poll(void)
{
    return (s_mock_th_rx_len > 0U) ? 1U : 0U;
}

uint16_t forward_uart_proto_rx_read(uint8_t *buf, uint16_t max_len)
{
    if ((buf == NULL) || (s_mock_th_rx_len == 0U))
    {
        return 0U;
    }
    const uint16_t n = (s_mock_th_rx_len > max_len) ? max_len : s_mock_th_rx_len;
    memcpy(buf, s_mock_th_rx_buf, n);
    s_mock_th_rx_len = 0U;
    return n;
}

bool forward_uart_send_raw(const uint8_t *data, uint16_t len)
{
    if ((data == NULL) || (len == 0U))
    {
        return false;
    }
    return s_forward_send_ok;
}

uint32_t wk_timebase_get(void)
{
    return s_mock_tick_ms;
}

static void drain_all_usart1(void)
{
    s_usart1_tdbe = SET;
    for (int i = 0; i < 40; ++i)
    {
        mc_debug_poll_drain();
    }
}

static void clear_usart1_capture(void)
{
    s_usart1_tx_len = 0U;
    s_usart1_tx_capture[0] = '\0';
}

static void send_test_frame(uint8_t dst, uint8_t cmd, const uint8_t *pay, uint16_t plen)
{
    s_test_seq++;
    uint8_t frame[MINIMC_MAX_FRAME_SIZE];
    frame[0] = MINIMC_SOF_1;
    frame[1] = MINIMC_SOF_2;
    frame[2] = MINIMC_NODE_AP;
    frame[3] = dst;
    frame[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    frame[5] = cmd;
    frame[6] = 4U;
    frame[7] = 0U;
    frame[8] = s_test_seq;
    frame[9] = 0U;
    frame[10] = (uint8_t)(plen & 0xFFU);
    frame[11] = (uint8_t)((plen >> 8U) & 0xFFU);
    if ((pay != NULL) && (plen > 0U))
    {
        memcpy(&frame[12], pay, plen);
    }
    const uint16_t crc = minimc_crc16(frame, (uint16_t)(12U + plen));
    frame[12U + plen] = (uint8_t)(crc & 0xFFU);
    frame[13U + plen] = (uint8_t)((crc >> 8U) & 0xFFU);
    minimc_proto_push_ap_rx(frame, (uint16_t)(14U + plen));
    minimc_proto_poll();
    drain_all_usart1();
}

static void inject_th_response_frame(uint8_t cmd, uint8_t seq)
{
    s_mock_th_rx_buf[0] = MINIMC_SOF_1;
    s_mock_th_rx_buf[1] = MINIMC_SOF_2;
    s_mock_th_rx_buf[2] = MINIMC_NODE_TH;
    s_mock_th_rx_buf[3] = MINIMC_NODE_AP;
    s_mock_th_rx_buf[4] = (uint8_t)(MINIMC_FLAG_IS_RESPONSE | MINIMC_FLAG_PROTO_V2);
    s_mock_th_rx_buf[5] = cmd;
    s_mock_th_rx_buf[6] = 4U;
    s_mock_th_rx_buf[7] = 0U;
    s_mock_th_rx_buf[8] = seq;
    s_mock_th_rx_buf[9] = 0U;
    s_mock_th_rx_buf[10] = 0U;
    s_mock_th_rx_buf[11] = 0U;
    const uint16_t crc = minimc_crc16(s_mock_th_rx_buf, 12U);
    s_mock_th_rx_buf[12] = (uint8_t)(crc & 0xFFU);
    s_mock_th_rx_buf[13] = (uint8_t)((crc >> 8U) & 0xFFU);
    s_mock_th_rx_len = 14U;
    minimc_proto_poll();
    drain_all_usart1();
}

static void test_usart2_921600_reconfig(void)
{
    printf("[RUN ] test_usart2_921600_reconfig\n");
    s_usart2_baud = 115200U;
    s_usart2_disable_cnt = 0U;
    s_usart2_enable_cnt = 0U;
    minimc_proto_init();
    assert(AP_USART_BAUDRATE == 921600U);
    assert(s_usart2_baud == 921600U);
    assert(s_usart2_disable_cnt == 1U);
    assert(s_usart2_enable_cnt == 1U);
    printf("[PASS] test_usart2_921600_reconfig\n");
}

static void test_ring_buffer_trunc_drop_and_recovery(void)
{
    printf("[RUN ] test_ring_buffer_trunc_drop_and_recovery\n");
    minimc_proto_init();
    clear_usart1_capture();

    char long_line[220];
    memset(long_line, 'A', sizeof(long_line));
    assert(mc_debug_write(long_line, 210U) == true);
    assert(mc_debug_get_trunc_count() == 1U);

    s_usart1_tdbe = RESET;
    mc_debug_poll_drain();
    assert(s_usart1_tx_len == 0U);

    s_usart1_tdbe = SET;
    mc_debug_poll_drain();
    assert(s_usart1_tx_len == 64U);
    drain_all_usart1();
    assert(s_usart1_tx_len == 192U);
    assert(memcmp(&s_usart1_tx_capture[187], "...\r\n", 5U) == 0);

    s_usart1_tdbe = RESET;
    char chunk[160];
    memset(chunk, 'B', sizeof(chunk));
    for (int i = 0; i < 12; ++i)
    {
        assert(mc_debug_write(chunk, 160U) == true);
    }
    assert(mc_debug_write(chunk, 160U) == false);
    assert(mc_debug_get_drop_count() == 1U);

    /* Recovery A: Drain full ring buffer, write new log, verify accepted without drop */
    drain_all_usart1();
    clear_usart1_capture();
    const char *rec_msg = "[MC-DBG] RING_RECOVERY_OK\r\n";
    assert(mc_debug_write(rec_msg, (uint16_t)strlen(rec_msg)) == true);
    assert(mc_debug_get_drop_count() == 1U);
    drain_all_usart1();
    assert(strstr(s_usart1_tx_capture, "RING_RECOVERY_OK") != NULL);
    printf("[PASS] test_ring_buffer_trunc_drop_and_recovery\n");
}

static void test_honest_minimc_v2_queries_and_nack(void)
{
    printf("[RUN ] test_honest_minimc_v2_queries_and_nack\n");
    current_temperature_ex1 = 215;
    current_temperature_bed = 60;
    current_position[X_AXIS] = 120.5f;
    current_position[Y_AXIS] = 85.25f;
    current_position[Z_AXIS] = 10.0f;
    axis_known_position[X_AXIS] = true;
    axis_known_position[Y_AXIS] = true;
    axis_known_position[Z_AXIS] = true;
    bed_level[2][1] = -0.042f;
    is_paused = 0U;
    s_mock_moves_planned = 2U;

    minimc_proto_init();
    clear_usart1_capture();
    s_mock_tick_ms = 1000U;
    s_test_seq = 0U;

    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_GET_VERSION, NULL, 0U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_VERSION_REPORT);
    const uint8_t ping_pay[4] = { 0xE8U, 0x03U, 0x00U, 0x00U };
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_PING, ping_pay, 4U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_PONG);
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_TEMP_REPORT);
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_POS_QUERY, NULL, 0U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_POS_QUERY);
    const uint8_t grid_pay[1] = { 7U };
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_LEVEL_GRID_QUERY, grid_pay, 1U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_LEVEL_GRID_QUERY);
    assert(s_last_ap_tx_len == MINIMC_LEVEL_GRID_FRAME_SIZE);

    /* Unimplemented opcode (0x10 SET_TEMP) MUST honestly return NACK (0x06) with err_code=0x04 */
    const uint8_t unimpl_pay[4] = { 0x98U, 0x08U, 0x8AU, 0x02U };
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_SET_TEMP, unimpl_pay, 4U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_NACK);
    assert(s_last_ap_tx_frame[12] == 0x04U);
    assert(strstr(s_usart1_tx_capture, "dir=ERR node=MC seq=6 cmd=0x10 status=BAD_CMD err_code=0x04") != NULL);
    assert(strstr(s_usart1_tx_capture, "dir=TX node=MC seq=6 cmd=0x06 status=NACK err_code=0x04") != NULL);
    printf("[PASS] test_honest_minimc_v2_queries_and_nack\n");
}

static void test_non_intrusive_notify_and_fault_sync(void)
{
    printf("[RUN ] test_non_intrusive_notify_and_fault_sync\n");
    clear_usart1_capture();
    mc_debug_notify_temp_target(2200, 650);
    mc_debug_notify_motion("MOVE", 0x03U, 3600U);
    mc_debug_notify_filament("UNLOAD", 2U, 0x0BU, "DONE");
    mc_debug_notify_job(2U, 625U, 10U);
    drain_all_usart1();

    assert(strstr(s_usart1_tx_capture, "nozzle_ddC=2150 nozzle_set_ddC=2200 bed_ddC=600 bed_set_ddC=650 heater_fault=0") != NULL);
    assert(strstr(s_usart1_tx_capture, "op=MOVE axes_mask=0x03 x_mm_x100=12050 y_mm_x100=8525 z_mm_x100=1000 feed=3600 homed_mask=0x07 motion_state=MOVING") != NULL);
    assert(strstr(s_usart1_tx_capture, "op=UNLOAD slot=2 active_slot=2 filament_present_mask=0x0B step_state=DONE") != NULL);
    assert(strstr(s_usart1_tx_capture, "job_state=PRINTING progress_permille=625 ack_seq=10") != NULL);

    /* Simulate thermistor fault + pause, verify sentinel and recovery */
    current_temperature_ex1 = 200;
    current_temperature_bed = BAD_TEMPERATURE;
    is_paused = 1U;
    s_mock_moves_planned = 0U;
    clear_usart1_capture();
    s_mock_tick_ms = 1600U;
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(strstr(s_usart1_tx_capture, "nozzle_ddC=2000 nozzle_set_ddC=2200 bed_ddC=32767 bed_set_ddC=650 heater_fault=1") != NULL);
    assert(strstr(s_usart1_tx_capture, "job_state=PAUSED progress_permille=625") != NULL);

    current_temperature_bed = 55;
    is_paused = 0U;
    clear_usart1_capture();
    s_mock_tick_ms = 2200U;
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(strstr(s_usart1_tx_capture, "nozzle_ddC=2000 nozzle_set_ddC=2200 bed_ddC=550 bed_set_ddC=650 heater_fault=0") != NULL);
    printf("[PASS] test_non_intrusive_notify_and_fault_sync\n");
}

static void test_tx_fail_suppresses_ack_and_recovers(void)
{
    printf("[RUN ] test_tx_fail_suppresses_ack_and_recovers\n");
    minimc_proto_init();
    clear_usart1_capture();
    s_mock_tick_ms = 3000U;
    s_test_seq = 20U;

    /* 1. Simulate USART2 DMA TX busy timeout -> minimc_proto_send returns false */
    const uint32_t tx_before = s_ap_tx_count;
    s_dma_auto_clear_busy = false;
    usart2_tx_busy = 1U;
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(s_ap_tx_count == tx_before);
    assert(strstr(s_usart1_tx_capture, "dir=TX node=MC seq=21 cmd=0x14 status=ACK") == NULL);
    assert(strstr(s_usart1_tx_capture, "dir=STATE node=MC seq=21 cmd=0x14 status=OK") == NULL);
    assert(strstr(s_usart1_tx_capture, "dir=ERR node=MC seq=21 cmd=0x14 status=TX_ERR err_code=0x06") != NULL);

    /* Recovery B: Clear busy state, send next query, verify wire frame & TX status=ACK */
    s_dma_auto_clear_busy = true;
    usart2_tx_busy = 0U;
    clear_usart1_capture();
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(s_ap_tx_count == tx_before + 1U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_TEMP_REPORT);
    assert(strstr(s_usart1_tx_capture, "dir=STATE node=MC seq=22 cmd=0x14 status=OK") != NULL);
    assert(strstr(s_usart1_tx_capture, "dir=TX node=MC seq=22 cmd=0x14 status=ACK") != NULL);
    printf("[PASS] test_tx_fail_suppresses_ack_and_recovers\n");
}

static void test_relay_timeout_crc_err_and_recovery(void)
{
    printf("[RUN ] test_relay_timeout_crc_err_and_recovery\n");
    minimc_proto_init();
    clear_usart1_capture();
    s_mock_tick_ms = 4000U;
    s_test_seq = 30U;

    /* 1. Relay to TH and simulate TH timeout after 250ms (seq=31) */
    send_test_frame(MINIMC_NODE_TH, MINIMC_CMD_GET_VERSION, NULL, 0U);
    assert(strstr(s_usart1_tx_capture, "dir=RELAY_TX node=TH seq=31 cmd=0x01 status=EXEC timeout_ms=200") != NULL);
    s_mock_tick_ms = 4250U;
    minimc_proto_poll();
    drain_all_usart1();
    assert(strstr(s_usart1_tx_capture, "dir=RELAY_RX node=TH seq=31 cmd=0x01 status=TIMEOUT elapsed_ms=250") != NULL);
    assert(strstr(s_usart1_tx_capture, "dir=ERR node=TH seq=31 cmd=0x01 status=TIMEOUT") != NULL);

    /* Recovery C: Subsequent TH relay request (seq=32) + valid TH response after 15ms succeeds */
    clear_usart1_capture();
    send_test_frame(MINIMC_NODE_TH, MINIMC_CMD_GET_VERSION, NULL, 0U);
    assert(strstr(s_usart1_tx_capture, "dir=RELAY_TX node=TH seq=32 cmd=0x01 status=EXEC timeout_ms=200") != NULL);
    s_mock_tick_ms = 4265U;
    inject_th_response_frame(MINIMC_CMD_VERSION_REPORT, 32U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_VERSION_REPORT);
    assert(strstr(s_usart1_tx_capture, "dir=RELAY_RX node=TH seq=32 cmd=0x02 status=ACK elapsed_ms=15") != NULL);
    assert(strstr(s_usart1_tx_capture, "dir=TX node=TH seq=32 cmd=0x02 status=ACK elapsed_ms=15") != NULL);

    /* 2. Corrupted CRC frame -> CRC_ERR, followed by valid PING recovery (seq=33) */
    uint8_t bad_crc[14] = { 0x55U, 0xAAU, 0x01U, 0x02U, 0x05U, 0x01U, 0x04U, 0x00U, 0x28U, 0x00U, 0x00U, 0x00U, 0xFFU, 0xFFU };
    minimc_proto_push_ap_rx(bad_crc, sizeof(bad_crc));
    minimc_proto_poll();
    drain_all_usart1();
    assert(strstr(s_usart1_tx_capture, "dir=ERR node=MC seq=40 cmd=0x01 status=CRC_ERR err_code=0x01") != NULL);
    send_test_frame(MINIMC_NODE_MC, MINIMC_CMD_PING, NULL, 0U);
    assert(s_last_ap_tx_frame[5] == MINIMC_CMD_PONG);
    assert(strstr(s_usart1_tx_capture, "dir=TX node=MC seq=33 cmd=0x04 status=ACK") != NULL);
    printf("[PASS] test_relay_timeout_crc_err_and_recovery\n");
}

int main(void)
{
    void *p = mmap((void *)0x40020000, 0x10000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (p == MAP_FAILED)
    {
        perror("mmap");
        return 1;
    }
    printf("========================================================================\n");
    printf("TWIN-44 MC USART2 921600 & USART1 Non-Blocking [MC-DBG] Verification\n");
    printf("========================================================================\n");
    test_usart2_921600_reconfig();
    test_ring_buffer_trunc_drop_and_recovery();
    test_honest_minimc_v2_queries_and_nack();
    test_non_intrusive_notify_and_fault_sync();
    test_tx_fail_suppresses_ack_and_recovers();
    test_relay_timeout_crc_err_and_recovery();
    printf("------------------------------------------------------------------------\n");
    printf("All 6 TWIN-44 test suites (including post-error recovery) PASSED!\n");
    printf("========================================================================\n");
    return 0;
}
