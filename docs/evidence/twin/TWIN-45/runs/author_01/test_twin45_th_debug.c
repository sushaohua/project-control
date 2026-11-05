/**
 * @file test_twin45_th_debug.c
 * @brief Independent verification test suite for TWIN-45 (TH USART3 Non-Blocking [TH-DBG] Logger).
 * Task ID: TWIN-45
 * Role: ENG-TH
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include <sys/mman.h>

#include "usart.h"
#include "minimc_proto.h"
#include "minimc_telemetry.h"
#include "thermistor_adc.h"

/* Mock globals referenced by usart.c */
volatile uint32_t cmdbuf_full_skip_count = 0U;
char load_filament_Flag = 0;
uint8_t active_extruder = 0U;

static uint32_t s_mock_tick_ms = 1000U;
static uint32_t s_usart1_baud = 0U;
static uint32_t s_usart3_baud = 0U;
static uint16_t s_usart1_rx_write_pos = 0U;
static bool s_usart3_auto_drain = true;
static flag_status s_usart3_fdt_flag = SET;

static char s_usart3_capture[16384];
static size_t s_usart3_capture_len = 0U;
static uint8_t s_usart1_last_tx[128];
static uint16_t s_usart1_last_tx_len = 0U;

uint32_t get_tick_count(void)
{
    return s_mock_tick_ms;
}

uint8_t Board_getFilamentStatus(void)
{
    return 0U; /* FILAMENT_NORMAL */
}

bool thermistor_adc_get_telemetry(minimc_temp_report_payload_t *report)
{
    if (report == NULL)
    {
        return false;
    }
    report->current_temp_deci_c = 245;
    report->target_temp_deci_c = 0;
    report->raw_adc_value = 3911U;
    report->sensor_status = MINIMC_TEMP_STATUS_OK;
    report->heater_duty_percent = 0U;
    report->sample_timestamp_ms = s_mock_tick_ms;
    report->reserved = 0U;
    return true;
}

/* Mock AT32F423 stdperiph driver functions */
void crm_periph_clock_enable(crm_periph_clock_type value, confirm_state new_state)
{
    (void)value;
    (void)new_state;
}

void gpio_default_para_init(gpio_init_type *init_struct)
{
    if (init_struct != NULL)
    {
        memset(init_struct, 0, sizeof(*init_struct));
    }
}

void gpio_init(gpio_type *gpio_x, gpio_init_type *init_struct)
{
    (void)gpio_x;
    (void)init_struct;
}

void gpio_pin_mux_config(gpio_type *gpio_x, gpio_pins_source_type gpio_pin_source, gpio_mux_sel_type gpio_mux)
{
    (void)gpio_x;
    (void)gpio_pin_source;
    (void)gpio_mux;
}

void usart_init(usart_type *usart_x, uint32_t baud_rate,
                usart_data_bit_num_type data_bit, usart_stop_bit_num_type stop_bit)
{
    assert(data_bit == USART_DATA_8BITS);
    assert(stop_bit == USART_STOP_1_BIT);
    if (usart_x == USART1)
    {
        s_usart1_baud = baud_rate;
    }
    else if (usart_x == USART3)
    {
        s_usart3_baud = baud_rate;
    }
}

void usart_parity_selection_config(usart_type *usart_x, usart_parity_selection_type parity)
{
    (void)usart_x;
    (void)parity;
}

void usart_receiver_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_transmitter_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_dma_receiver_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_dma_transmitter_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

flag_status usart_flag_get(usart_type *usart_x, uint32_t flag)
{
    (void)usart_x;
    (void)flag;
    return SET;
}

void usart_data_transmit(usart_type *usart_x, uint16_t data)
{
    (void)usart_x;
    (void)data;
}

void dma_reset(dma_channel_type *dmax_channely)
{
    (void)dmax_channely;
}

void dma_default_para_init(dma_init_type *init_struct)
{
    if (init_struct != NULL)
    {
        memset(init_struct, 0, sizeof(*init_struct));
    }
}

void dma_init(dma_channel_type *dmax_channely, dma_init_type *init_struct)
{
    (void)init_struct;
    if (dmax_channely == DMA1_CHANNEL2)
    {
        s_usart1_rx_write_pos = 0U;
    }
}

void dma_flexible_config(dma_type *dma_x, dmamux_channel_type *dmamux_channelx, dmamux_requst_id_sel_type req_id)
{
    (void)dma_x;
    (void)dmamux_channelx;
    (void)req_id;
}

void dma_interrupt_enable(dma_channel_type *dmax_channely, uint32_t dma_int, confirm_state new_state)
{
    (void)dmax_channely;
    (void)dma_int;
    (void)new_state;
}

void nvic_irq_enable(IRQn_Type irqn, uint32_t preempt_priority, uint32_t sub_priority)
{
    (void)irqn;
    (void)preempt_priority;
    (void)sub_priority;
}

void dma_flag_clear(uint32_t dmax_flag)
{
    (void)dmax_flag;
}

flag_status dma_flag_get(uint32_t dmax_flag)
{
    if (dmax_flag == DMA1_FDT5_FLAG)
    {
        return s_usart3_fdt_flag;
    }
    if (dmax_flag == DMA1_FDT4_FLAG)
    {
        return SET;
    }
    return RESET;
}

static uint16_t s_dma_ch4_len = 0U;
static uint16_t s_dma_ch5_len = 0U;

void dma_data_number_set(dma_channel_type *dmax_channely, uint16_t data_number)
{
    if (dmax_channely == DMA1_CHANNEL4)
    {
        s_dma_ch4_len = data_number;
    }
    else if (dmax_channely == DMA1_CHANNEL5)
    {
        s_dma_ch5_len = data_number;
    }
    else if (dmax_channely == DMA1_CHANNEL2)
    {
        s_usart1_rx_write_pos = 0U;
    }
}

uint16_t dma_data_number_get(dma_channel_type *dmax_channely)
{
    if (dmax_channely == DMA1_CHANNEL2)
    {
        return (uint16_t)(USART1_RXBUFF_SIZE - s_usart1_rx_write_pos);
    }
    return USART3_RXBUFF_SIZE;
}

void dma_channel_enable(dma_channel_type *dmax_channely, confirm_state new_state)
{
    if ((dmax_channely == DMA1_CHANNEL4) && (new_state == TRUE) && (s_dma_ch4_len > 0U))
    {
        const uint8_t *src = (const uint8_t *)(uintptr_t)DMA1_CHANNEL4->maddr;
        const uint16_t copy_n = (s_dma_ch4_len <= sizeof(s_usart1_last_tx))
                                    ? s_dma_ch4_len
                                    : (uint16_t)sizeof(s_usart1_last_tx);
        memcpy(s_usart1_last_tx, src, copy_n);
        s_usart1_last_tx_len = copy_n;
    }
    else if ((dmax_channely == DMA1_CHANNEL5) && (new_state == TRUE) && (s_dma_ch5_len > 0U))
    {
        const char *src = (const char *)(uintptr_t)DMA1_CHANNEL5->maddr;
        if ((s_usart3_capture_len + s_dma_ch5_len + 1U) < sizeof(s_usart3_capture))
        {
            memcpy(&s_usart3_capture[s_usart3_capture_len], src, s_dma_ch5_len);
            s_usart3_capture_len += s_dma_ch5_len;
            s_usart3_capture[s_usart3_capture_len] = '\0';
        }
    }
}

static void drain_usart3_dma(void)
{
    s_usart3_fdt_flag = SET;
    for (int i = 0; i < 8; ++i)
    {
        USART3_dma_tx_isr_handler();
    }
}

static void clear_capture(void)
{
    s_usart3_capture_len = 0U;
    s_usart3_capture[0] = '\0';
    s_usart1_last_tx_len = 0U;
}

static void push_usart1_rx_bytes(const uint8_t *bytes, uint16_t len)
{
    for (uint16_t i = 0U; i < len; ++i)
    {
        usart1_rx_buffer[s_usart1_rx_write_pos] = bytes[i];
        s_usart1_rx_write_pos = (uint16_t)((s_usart1_rx_write_pos + 1U) % USART1_RXBUFF_SIZE);
    }
}

static void inject_minimc_req(uint8_t seq, uint8_t cmd, const uint8_t *payload, uint16_t plen)
{
    uint8_t frame[MINIMC_MAX_FRAME_SIZE];
    frame[0] = MINIMC_SOF_1;
    frame[1] = MINIMC_SOF_2;
    frame[2] = MINIMC_NODE_MC;
    frame[3] = MINIMC_NODE_TH;
    frame[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    frame[5] = cmd;
    frame[6] = 3U;
    frame[7] = MINIMC_ROUTE_IS_ROUTED;
    frame[8] = seq;
    frame[9] = 0U;
    frame[10] = (uint8_t)(plen & 0xFFU);
    frame[11] = (uint8_t)((plen >> 8U) & 0xFFU);
    if ((payload != NULL) && (plen > 0U))
    {
        memcpy(&frame[12], payload, plen);
    }
    const uint16_t crc = minimc_crc16(frame, (uint16_t)(12U + plen));
    frame[12U + plen] = (uint8_t)(crc & 0xFFU);
    frame[13U + plen] = (uint8_t)((crc >> 8U) & 0xFFU);

    push_usart1_rx_bytes(frame, (uint16_t)(14U + plen));
    minimc_proto_poll();
    if (s_usart3_auto_drain)
    {
        drain_usart3_dma();
    }
}

static void test_usart1_921600_and_usart3_115200_init(void)
{
    printf("[RUN ] test_usart1_921600_and_usart3_115200_init\n");
    s_usart1_baud = 0U;
    s_usart3_baud = 0U;
    s_usart1_rx_write_pos = 0U;
    MY_USART1_Init();
    MY_USART3_Init();
    minimc_proto_init();

    assert(BAUDRATE1 == 921600);
    assert(BAUDRATE2 == 115200);
    assert(s_usart1_baud == 921600U);
    assert(s_usart3_baud == 115200U);
    assert(TH_DEBUG_MODE_ENABLE == 1);
    assert(th_debug_is_enabled() == true);
    assert(USART3_get_tx_drop_count() == 0U);
    assert(USART3_get_tx_trunc_count() == 0U);
    printf("[PASS] test_usart1_921600_and_usart3_115200_init\n");
}

static void test_cascade_rx_and_tx_logging(void)
{
    printf("[RUN ] test_cascade_rx_and_tx_logging\n");
    MY_USART1_Init();
    MY_USART3_Init();
    minimc_proto_init();
    clear_capture();
    s_mock_tick_ms = 1000U;

    /* 1. GET_VERSION (0x01) -> VERSION_REPORT (0x02) */
    inject_minimc_req(1U, MINIMC_CMD_GET_VERSION, NULL, 0U);
    assert(strstr(s_usart3_capture, "[TH-DBG] ts=1000 dir=RX node=TH seq=1 cmd=0x01 status=OK len=14") != NULL);
    assert(strstr(s_usart3_capture, "[TH-DBG] ts=1000 dir=TX node=TH seq=1 cmd=0x02 status=ACK fw=2.0") != NULL);

    /* 2. PING (0x03) -> PONG (0x04) */
    const uint8_t ping_pay[4] = { 0x78U, 0x56U, 0x34U, 0x12U };
    inject_minimc_req(2U, MINIMC_CMD_PING, ping_pay, 4U);
    assert(strstr(s_usart3_capture, "dir=RX node=TH seq=2 cmd=0x03 status=OK len=18") != NULL);
    assert(strstr(s_usart3_capture, "dir=TX node=TH seq=2 cmd=0x04 status=ACK pong=1") != NULL);

    /* 3. GET_TEMP (0x14) -> STATE + TEMP_REPORT (0x14) */
    inject_minimc_req(3U, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(strstr(s_usart3_capture, "dir=RX node=TH seq=3 cmd=0x14 status=OK len=14") != NULL);
    assert(strstr(s_usart3_capture, "dir=STATE node=TH seq=3 cmd=0x14 status=OK nozzle_ddC=245 adc_raw=3911 pullup_sel=0 fault=0") != NULL);
    assert(strstr(s_usart3_capture, "dir=TX node=TH seq=3 cmd=0x14 status=ACK nozzle_ddC=245 adc_raw=3911 pullup_sel=0 fault=0") != NULL);

    /* 4. SET_TEMP (0x10) and FILAMENT_CONTROL (0x15) / SLOT_SELECT (0x19) */
    const uint8_t set_temp_pay[2] = { 0x66U, 0x08U }; /* 2150 = 215.0C */
    inject_minimc_req(4U, MINIMC_CMD_SET_TEMP, set_temp_pay, 2U);
    assert(strstr(s_usart3_capture, "dir=RX node=TH seq=4 cmd=0x10 status=OK len=16 nozzle_set=2150") != NULL);

    const uint8_t fil_pay[2] = { 2U, 0U }; /* slot=2, LOAD */
    inject_minimc_req(5U, MINIMC_CMD_FILAMENT_CONTROL, fil_pay, 2U);
    assert(strstr(s_usart3_capture, "dir=RX node=TH seq=5 cmd=0x15 status=OK len=16 op=LOAD slot=2") != NULL);
    assert(strstr(s_usart3_capture, "dir=STATE node=TH seq=5 cmd=0x15 status=OK op=LOAD slot=2 active_slot=2 filament_present_mask=0x0F step_state=DONE") != NULL);

    const uint8_t slot_pay[1] = { 3U }; /* slot=3, SELECT */
    inject_minimc_req(6U, MINIMC_CMD_SLOT_SELECT, slot_pay, 1U);
    assert(strstr(s_usart3_capture, "dir=STATE node=TH seq=6 cmd=0x19 status=OK op=SELECT slot=3 active_slot=3 filament_present_mask=0x0F step_state=DONE") != NULL);
    printf("[PASS] test_cascade_rx_and_tx_logging\n");
}

static void test_periodic_state_rate_limit_2hz(void)
{
    printf("[RUN ] test_periodic_state_rate_limit_2hz\n");
    MY_USART1_Init();
    MY_USART3_Init();
    minimc_proto_init();
    clear_capture();

    s_mock_tick_ms = 2000U;
    th_debug_log_periodic_state(2000U);
    drain_usart3_dma();
    assert(strstr(s_usart3_capture, "ts=2000 dir=STATE node=TH seq=0 cmd=0x14 status=OK nozzle_ddC=245 adc_raw=3911 pullup_sel=0 fault=0") != NULL);
    assert(strstr(s_usart3_capture, "ts=2000 dir=STATE node=TH seq=0 cmd=0x15 status=OK") != NULL);

    /* Within 500ms (<2Hz limit): must not emit any new logs */
    clear_capture();
    s_mock_tick_ms = 2250U;
    th_debug_log_periodic_state(2250U);
    s_mock_tick_ms = 2499U;
    th_debug_log_periodic_state(2499U);
    drain_usart3_dma();
    assert(s_usart3_capture_len == 0U);

    /* At +500ms: must emit periodic state summary */
    s_mock_tick_ms = 2500U;
    th_debug_log_periodic_state(2500U);
    drain_usart3_dma();
    assert(strstr(s_usart3_capture, "ts=2500 dir=STATE node=TH seq=0 cmd=0x14 status=OK") != NULL);
    printf("[PASS] test_periodic_state_rate_limit_2hz\n");
}

static void test_negative_crc_err_bad_frame_and_dma_recovery(void)
{
    printf("[RUN ] test_negative_crc_err_bad_frame_and_dma_recovery\n");
    MY_USART1_Init();
    MY_USART3_Init();
    minimc_proto_init();
    clear_capture();
    s_mock_tick_ms = 3000U;

    /* 1. CRC error frame -> dir=ERR status=CRC_ERR */
    const uint8_t bad_crc_frame[14] = {
        0x55U, 0xAAU, 0x02U, 0x03U, 0x05U, 0x14U, 0x03U, 0x04U,
        10U,   0x00U, 0x00U, 0x00U, 0xDEU, 0xADU
    };
    push_usart1_rx_bytes(bad_crc_frame, sizeof(bad_crc_frame));
    minimc_proto_poll();
    drain_usart3_dma();
    assert(strstr(s_usart3_capture, "dir=ERR node=TH seq=10 cmd=0x14 status=CRC_ERR err_code=0x01") != NULL);

    /* 2. Malformed frame with payload_len=100 (>64) -> dir=ERR status=BAD_FRAME */
    const uint8_t bad_len_hdr[12] = {
        0x55U, 0xAAU, 0x02U, 0x03U, 0x05U, 0x14U, 0x03U, 0x04U,
        11U,   0x00U, 100U,  0x00U
    };
    push_usart1_rx_bytes(bad_len_hdr, sizeof(bad_len_hdr));
    minimc_proto_poll();
    drain_usart3_dma();
    assert(strstr(s_usart3_capture, "dir=ERR node=TH seq=11 cmd=0x14 status=BAD_FRAME err_code=0x02") != NULL);

    /* 3. Verify USART1 cascade recovery immediately after error */
    clear_capture();
    inject_minimc_req(12U, MINIMC_CMD_GET_TEMP, NULL, 0U);
    assert(s_usart1_last_tx_len == 30U);
    assert(strstr(s_usart3_capture, "dir=RX node=TH seq=12 cmd=0x14 status=OK len=14") != NULL);
    assert(strstr(s_usart3_capture, "dir=TX node=TH seq=12 cmd=0x14 status=ACK") != NULL);
    printf("[PASS] test_negative_crc_err_bad_frame_and_dma_recovery\n");
}

static void test_negative_usart3_ring_full_drop_and_trunc_nonblocking(void)
{
    printf("[RUN ] test_negative_usart3_ring_full_drop_and_trunc_nonblocking\n");
    MY_USART1_Init();
    MY_USART3_Init();
    minimc_proto_init();
    clear_capture();
    s_mock_tick_ms = 4000U;

    /* 1. Test >192B line truncation */
    char long_line[220];
    memset(long_line, 'X', sizeof(long_line));
    assert(th_debug_write(long_line, 210U) == true);
    drain_usart3_dma();
    assert(USART3_get_tx_trunc_count() == 1U);
    assert(s_usart3_capture_len == 192U);
    assert(memcmp(&s_usart3_capture[187], "...\r\n", 5U) == 0);

    /* 2. Hold USART3 DMA busy (do not drain ISR) and fill 2048B ring buffer */
    s_usart3_auto_drain = false;
    char block[160];
    memset(block, 'Y', sizeof(block));
    for (int i = 0; i < 12; ++i)
    {
        assert(th_debug_write(block, 160U) == true);
    }
    /* Next write exceeds remaining free space -> must drop and return false immediately */
    assert(th_debug_write(block, 160U) == false);
    assert(USART3_get_tx_drop_count() >= 1U);

    /* 3. While USART3 ring buffer is full, USART1 cascade response must NOT block */
    s_usart1_last_tx_len = 0U;
    const uint8_t ping_pay[4] = { 0x01U, 0x02U, 0x03U, 0x04U };
    inject_minimc_req(20U, MINIMC_CMD_PING, ping_pay, 4U);
    assert(s_usart1_last_tx_len == 26U); /* PONG sent on USART1 without blocking */
    assert(s_usart1_last_tx[5] == MINIMC_CMD_PONG);

    /* 4. Drain USART3 DMA and verify subsequent log carries drop>0 and trunc=1 */
    s_usart3_auto_drain = true;
    drain_usart3_dma();
    clear_capture();
    inject_minimc_req(21U, MINIMC_CMD_GET_VERSION, NULL, 0U);
    assert(strstr(s_usart3_capture, "dir=TX node=TH seq=21 cmd=0x02 status=ACK fw=2.0") != NULL);
    assert(strstr(s_usart3_capture, "trunc=1") != NULL);
    assert(USART3_get_tx_drop_count() >= 2U);
    printf("[PASS] test_negative_usart3_ring_full_drop_and_trunc_nonblocking\n");
}

int main(void)
{
    void *p1 = mmap((void *)0x40000000, 0x30000, PROT_READ | PROT_WRITE,
                    MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (p1 == MAP_FAILED)
    {
        perror("mmap");
        return 1;
    }
    printf("========================================================================\n");
    printf("TWIN-45 TH USART1 921600 Cascade & USART3 Non-Blocking [TH-DBG] Suite\n");
    printf("========================================================================\n");
    test_usart1_921600_and_usart3_115200_init();
    test_cascade_rx_and_tx_logging();
    test_periodic_state_rate_limit_2hz();
    test_negative_crc_err_bad_frame_and_dma_recovery();
    test_negative_usart3_ring_full_drop_and_trunc_nonblocking();
    printf("------------------------------------------------------------------------\n");
    printf("All 5 TWIN-45 test suites PASSED!\n");
    printf("========================================================================\n");
    return 0;
}
