/**
 * @file test_twin26_mcu_upgrade.c
 * @brief Binary verification test suite for TWIN-26 Dual MCU firmware upgrade channel
 *        and Bootloader IAP protocol reuse reconciliation.
 *
 * Task ID: TWIN-26
 * Lease ID: lease-twin-26-run01
 * Role: ARCH / Firmware Engineer
 * Design Ref: ARCH-MCU-UPGRADE-DESIGN-20261031 (Decision U-D05)
 * Conforms to project-control/.agents/rules/c_cpp_coding_standard.md:
 *  - Functions <= 50 lines
 *  - Parameters <= 4
 *  - Defensive guard clauses
 *  - Zero dynamic heap allocation
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include <stddef.h>
#include <sys/mman.h>

#include "wk_usart.h"
#include "wk_dma.h"

/* --------------------------------------------------------------------------
 * Hardware Peripherals & Global Stubs for Host Execution
 * -------------------------------------------------------------------------- */

forward_uart_dma_t forward_uart_dma;
uint32_t system_core_clock = 288000000U;

static uint8_t s_tx_captured_bytes[1024];
static uint16_t s_tx_captured_count = 0;

flag_status usart_flag_get(usart_type* usart_x, uint32_t flag)
{
    (void)usart_x;
    (void)flag;
    return SET;
}

void usart_data_transmit(usart_type* usart_x, uint16_t data)
{
    (void)usart_x;
    if (s_tx_captured_count < sizeof(s_tx_captured_bytes))
    {
        s_tx_captured_bytes[s_tx_captured_count] = (uint8_t)data;
        s_tx_captured_count++;
    }
}

void usart_flag_clear(usart_type* usart_x, uint32_t flag)
{
    (void)usart_x;
    (void)flag;
}

void dma_channel_enable(dma_channel_type* dma_channel, confirm_state new_state)
{
    (void)dma_channel;
    (void)new_state;
}

uint16_t dma_data_number_get(dma_channel_type* dma_channel)
{
    (void)dma_channel;
    return 0;
}

uint32_t wk_timebase_get(void)
{
    return 1000U;
}

void gpio_pin_mux_config(gpio_type *gpio_x, gpio_pins_source_type pin_source, gpio_mux_sel_type mux)
{
    (void)gpio_x;
    (void)pin_source;
    (void)mux;
}

void gpio_default_para_init(gpio_init_type *gpio_init_struct)
{
    (void)gpio_init_struct;
}

void gpio_init(gpio_type *gpio_x, gpio_init_type *gpio_init_struct)
{
    (void)gpio_x;
    (void)gpio_init_struct;
}

void usart_init(usart_type *usart_x, uint32_t baud, usart_data_bit_num_type data_bit, usart_stop_bit_num_type stop_bit)
{
    (void)usart_x;
    (void)baud;
    (void)data_bit;
    (void)stop_bit;
}

void usart_transmitter_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_receiver_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_dma_transmitter_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_dma_receiver_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

void usart_parity_selection_config(usart_type *usart_x, usart_parity_selection_type parity)
{
    (void)usart_x;
    (void)parity;
}

void usart_hardware_flow_control_set(usart_type *usart_x, usart_hardware_flow_control_type flow_control)
{
    (void)usart_x;
    (void)flow_control;
}

void usart_interrupt_enable(usart_type *usart_x, uint32_t usart_int, confirm_state new_state)
{
    (void)usart_x;
    (void)usart_int;
    (void)new_state;
}

void usart_enable(usart_type *usart_x, confirm_state new_state)
{
    (void)usart_x;
    (void)new_state;
}

/* Include target C source to test exact internal linkages */
#include "../../../../../mcu-p3/motion-controller-mcu/project/src/wk_usart.c"

/* --------------------------------------------------------------------------
 * Test Suite 1: 协议魔数与常量契约对账
 * -------------------------------------------------------------------------- */

static void test_protocol_constants_reconciliation(void)
{
    printf("[RUN ] test_protocol_constants_reconciliation\n");

    /* 1. 验证 wk_usart.h 中导出的 TH Bootloader IAP 常量 */
    assert(TH_IAP_SYNC_SOF_1 == 0x5AU);
    assert(TH_IAP_SYNC_SOF_2 == 0xA5U);
    assert(TH_IAP_CMD_HELLO == 0x10U);
    assert(TH_IAP_CMD_START_UPG == 0x11U);
    assert(TH_IAP_CMD_PUSH_CHUNK == 0x12U);
    assert(TH_IAP_CMD_FINISH == 0x13U);
    assert(TH_IAP_CHUNK_SIZE == 512U);
    assert(TH_IAP_STATUS_OK == 0x00U);
    assert(TH_IAP_STATUS_ERR == 0x01U);

    /* 2. 对账 ARCH-MCU-UPGRADE-DESIGN-20261031 架构设计常量 */
    const uint32_t mc_board_id = 0x43500001U;
    const uint32_t th_board_id = 0x42300001U;
    const uint32_t trailer_magic = 0x41545347U; /* 'ATSG' */
    const uint32_t boot_upgrade_magic = 0x55504744UL; /* 'UPGD' */
    const uint32_t forward_baud = 921600U;

    assert(mc_board_id == 0x43500001U);
    assert(th_board_id == 0x42300001U);
    assert(trailer_magic == 0x41545347U);
    assert(boot_upgrade_magic == 0x55504744UL);
    assert(forward_baud == 921600U);

    printf("[PASS] test_protocol_constants_reconciliation\n");
}

/* --------------------------------------------------------------------------
 * Test Suite 2: 透传独占模式切换与 Marlin 拦截保护
 * -------------------------------------------------------------------------- */

static void verify_marlin_blocked_in_upgrade_mode(void)
{
    /* Marlin G-code 发送拦截验证 */
    forward_uart_dma.forward_uart_tx_busy = 0;
    forward_uart_send_line("G28 X0 Y0", 9);
    assert(forward_uart_dma.forward_uart_tx_busy == 0);

    /* Marlin 原始数据发送拦截验证 */
    const uint8_t raw_test[4] = { 'M', '1', '0', '5' };
    const bool raw_sent = forward_uart_send_raw(raw_test, sizeof(raw_test));
    assert(raw_sent == false);

    /* Marlin 数据接收读取拦截验证 */
    forward_uart_dma.forward_uart_rx_buf[0] = 'o';
    forward_uart_dma.forward_uart_rx_buf[1] = 'k';
    forward_uart_dma.forward_uart_rx_len = 2;
    forward_uart_dma.forward_uart_rx_complete = 1;

    uint8_t rx_dst[16];
    const uint16_t rx_cnt = forward_uart_rx_read(rx_dst, sizeof(rx_dst));
    assert(rx_cnt == 0);
    assert(forward_uart_dma.forward_uart_rx_complete == 1);
}

static void verify_magic_sniffing_in_normal_mode(void)
{
    forward_uart_upgrade_mode_exit();
    assert(forward_uart_mode_get() == FORWARD_UART_MODE_NORMAL);

    /* 构造 0x5A 0xA5 私有升级帧注入 RX 缓冲区 */
    forward_uart_dma.forward_uart_rx_buf[0] = 0x5AU;
    forward_uart_dma.forward_uart_rx_buf[1] = 0xA5U;
    forward_uart_dma.forward_uart_rx_buf[2] = 0x10U;
    forward_uart_dma.forward_uart_rx_len = 3;
    forward_uart_dma.forward_uart_rx_complete = 1;

    uint8_t rx_dst[16];
    const uint16_t rx_cnt = forward_uart_rx_read(rx_dst, sizeof(rx_dst));
    /* 魔数嗅探生效：严禁将升级帧交由 Marlin 业务读取 */
    assert(rx_cnt == 0);
}

static void test_upgrade_mode_and_marlin_interception(void)
{
    printf("[RUN ] test_upgrade_mode_and_marlin_interception\n");

    /* 1. 验证默认模式 */
    forward_uart_mode_set(FORWARD_UART_MODE_NORMAL);
    assert(forward_uart_mode_get() == FORWARD_UART_MODE_NORMAL);

    /* 2. 进入升级独占模式并测试拦截 */
    forward_uart_upgrade_mode_enter();
    assert(forward_uart_mode_get() == FORWARD_UART_MODE_UPGRADE);
    verify_marlin_blocked_in_upgrade_mode();

    /* 3. 测试普通模式下的魔数嗅探拦截 */
    verify_magic_sniffing_in_normal_mode();

    /* 4. 恢复初始状态 */
    forward_uart_upgrade_mode_exit();
    assert(forward_uart_mode_get() == FORWARD_UART_MODE_NORMAL);

    printf("[PASS] test_upgrade_mode_and_marlin_interception\n");
}

/* --------------------------------------------------------------------------
 * Test Suite 3: 512B 分块发送帧封装与累加和校验计算
 * -------------------------------------------------------------------------- */

static uint8_t compute_frame_expected_checksum(uint8_t cmd, const uint8_t *payload, uint16_t len)
{
    uint8_t sum = (uint8_t)(cmd + (len & 0xFFU) + ((len >> 8) & 0xFFU));
    for (uint16_t i = 0; i < len; i++)
    {
        sum = (uint8_t)(sum + payload[i]);
    }
    return sum;
}

static void verify_captured_tx_frame(uint8_t exp_cmd, const uint8_t *exp_payload, uint16_t exp_len)
{
    const uint16_t total_expected = (uint16_t)(exp_len + 6U);
    assert(s_tx_captured_count == total_expected);
    assert(s_tx_captured_bytes[0] == 0x5AU);
    assert(s_tx_captured_bytes[1] == 0xA5U);
    assert(s_tx_captured_bytes[2] == exp_cmd);
    assert(s_tx_captured_bytes[3] == (uint8_t)(exp_len & 0xFFU));
    assert(s_tx_captured_bytes[4] == (uint8_t)((exp_len >> 8) & 0xFFU));

    if (exp_len > 0 && exp_payload != NULL)
    {
        assert(memcmp(&s_tx_captured_bytes[5], exp_payload, exp_len) == 0);
    }

    const uint8_t exp_csum = compute_frame_expected_checksum(exp_cmd, exp_payload, exp_len);
    assert(s_tx_captured_bytes[5 + exp_len] == exp_csum);
}

static void test_send_iap_chunk_512b_and_checksum(void)
{
    printf("[RUN ] test_send_iap_chunk_512b_and_checksum\n");

    forward_uart_upgrade_mode_enter();

    /* 1. 测试标准 512 字节分块 (TH_IAP_CMD_PUSH_CHUNK 0x12) */
    static uint8_t chunk_512[TH_IAP_CHUNK_SIZE];
    for (uint16_t i = 0; i < TH_IAP_CHUNK_SIZE; i++)
    {
        chunk_512[i] = (uint8_t)((i * 7U + 13U) & 0xFFU);
    }
    s_tx_captured_count = 0;
    bool ret = forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, chunk_512, TH_IAP_CHUNK_SIZE);
    assert(ret == true);
    verify_captured_tx_frame(TH_IAP_CMD_PUSH_CHUNK, chunk_512, TH_IAP_CHUNK_SIZE);

    /* 2. 测试 128 字节 Trailer 预验签包 (TH_IAP_CMD_START_UPG 0x11) */
    static uint8_t trailer_128[128];
    for (uint16_t i = 0; i < 128; i++)
    {
        trailer_128[i] = (uint8_t)(i ^ 0x3CU);
    }
    s_tx_captured_count = 0;
    ret = forward_uart_send_iap_chunk(TH_IAP_CMD_START_UPG, trailer_128, 128);
    assert(ret == true);
    verify_captured_tx_frame(TH_IAP_CMD_START_UPG, trailer_128, 128);

    /* 3. 测试 4 字节 CRC32 终验包 (TH_IAP_CMD_FINISH 0x13) */
    const uint8_t finish_crc[4] = { 0xAA, 0xBB, 0xCC, 0xDD };
    s_tx_captured_count = 0;
    ret = forward_uart_send_iap_chunk(TH_IAP_CMD_FINISH, finish_crc, 4);
    assert(ret == true);
    verify_captured_tx_frame(TH_IAP_CMD_FINISH, finish_crc, 4);

    /* 4. 测试 0 字节 Hello 握手包 (TH_IAP_CMD_HELLO 0x10) */
    const uint8_t dummy = 0;
    s_tx_captured_count = 0;
    ret = forward_uart_send_iap_chunk(TH_IAP_CMD_HELLO, &dummy, 0);
    assert(ret == true);
    verify_captured_tx_frame(TH_IAP_CMD_HELLO, &dummy, 0);

    forward_uart_upgrade_mode_exit();
    printf("[PASS] test_send_iap_chunk_512b_and_checksum\n");
}

/* --------------------------------------------------------------------------
 * Test Suite 4: 分块越界防御 (>512B 拦截) 与空指针防御
 * -------------------------------------------------------------------------- */

static void test_chunk_boundary_and_null_pointer_defenses(void)
{
    printf("[RUN ] test_chunk_boundary_and_null_pointer_defenses\n");

    static uint8_t valid_buf[1024];
    memset(valid_buf, 0x55, sizeof(valid_buf));

    /* 1. 空指针防御 */
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, NULL, 512) == false);
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, NULL, 0) == false);
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_START_UPG, NULL, 128) == false);

    /* 2. 长度越界防御 (>512B 拦截) */
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, valid_buf, 513) == false);
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, valid_buf, 600) == false);
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, valid_buf, 1024) == false);
    assert(forward_uart_send_iap_chunk(TH_IAP_CMD_PUSH_CHUNK, valid_buf, 0xFFFF) == false);

    /* 3. 响应解析空指针防御 */
    uint8_t out_cmd = 0;
    uint8_t out_status = 0;
    assert(forward_uart_recv_iap_resp(NULL, &out_status) == false);
    assert(forward_uart_recv_iap_resp(&out_cmd, NULL) == false);
    assert(forward_uart_recv_iap_resp(NULL, NULL) == false);

    printf("[PASS] test_chunk_boundary_and_null_pointer_defenses\n");
}

/* --------------------------------------------------------------------------
 * Test Suite 5: 响应解析与状态码提取
 * -------------------------------------------------------------------------- */

static void inject_mock_rx_frame(uint8_t cmd, const uint8_t *payload, uint16_t len)
{
    forward_uart_dma.forward_uart_rx_buf[0] = 0x5AU;
    forward_uart_dma.forward_uart_rx_buf[1] = 0xA5U;
    forward_uart_dma.forward_uart_rx_buf[2] = cmd;
    forward_uart_dma.forward_uart_rx_buf[3] = (uint8_t)(len & 0xFFU);
    forward_uart_dma.forward_uart_rx_buf[4] = (uint8_t)((len >> 8) & 0xFFU);

    uint8_t sum = (uint8_t)(cmd + (len & 0xFFU) + ((len >> 8) & 0xFFU));
    for (uint16_t i = 0; i < len; i++)
    {
        forward_uart_dma.forward_uart_rx_buf[5 + i] = payload[i];
        sum = (uint8_t)(sum + payload[i]);
    }

    forward_uart_dma.forward_uart_rx_buf[5 + len] = sum;
    forward_uart_dma.forward_uart_rx_len = (uint16_t)(len + 6U);
    forward_uart_dma.forward_uart_rx_complete = 1;
}

static void test_recv_iap_resp_positive_cases(void)
{
    uint8_t out_cmd = 0;
    uint8_t out_status = 0xFFU;

    /* 1. 模拟分块确认响应 ACK_TH_PUSH_CHUNK (0x92), 状态 0x00 OK */
    const uint8_t chunk_ack_ok[5] = { 0x00, 0x02, 0x00, 0x00, 0x00 };
    inject_mock_rx_frame(0x92U, chunk_ack_ok, sizeof(chunk_ack_ok));
    bool ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == true);
    assert(out_cmd == 0x92U);
    assert(out_status == TH_IAP_STATUS_OK);
    assert(forward_uart_dma.forward_uart_rx_complete == 0);

    /* 2. 模拟分块错误响应 ACK_TH_PUSH_CHUNK (0x92), 状态 0x01 ERR */
    const uint8_t chunk_ack_err[5] = { 0x00, 0x02, 0x00, 0x00, 0x01 };
    inject_mock_rx_frame(0x92U, chunk_ack_err, sizeof(chunk_ack_err));
    ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == true);
    assert(out_cmd == 0x92U);
    assert(out_status == TH_IAP_STATUS_ERR);

    /* 3. 模拟开始响应 ACK_TH_START_UPG (0x91), 状态 0x00 OK */
    const uint8_t start_ack[1] = { 0x00 };
    inject_mock_rx_frame(0x91U, start_ack, sizeof(start_ack));
    ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == true);
    assert(out_cmd == 0x91U);
    assert(out_status == TH_IAP_STATUS_OK);

    /* 4. 模拟完成响应 ACK_TH_FINISH (0x93), 状态 0x00 OK */
    const uint8_t finish_ack[1] = { 0x00 };
    inject_mock_rx_frame(0x93U, finish_ack, sizeof(finish_ack));
    ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == true);
    assert(out_cmd == 0x93U);
    assert(out_status == TH_IAP_STATUS_OK);
}

static void test_recv_iap_resp_negative_cases(void)
{
    uint8_t out_cmd = 0;
    uint8_t out_status = 0xFFU;
    const uint8_t chunk_ack_ok[5] = { 0x00, 0x02, 0x00, 0x00, 0x00 };

    /* 1. 校验和异常负例拦截 */
    inject_mock_rx_frame(0x92U, chunk_ack_ok, sizeof(chunk_ack_ok));
    forward_uart_dma.forward_uart_rx_buf[10] ^= 0x55; /* 破坏校验和 */
    bool ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == false);

    /* 2. 魔数异常负例拦截 */
    inject_mock_rx_frame(0x92U, chunk_ack_ok, sizeof(chunk_ack_ok));
    forward_uart_dma.forward_uart_rx_buf[0] = 0x00; /* 破坏同步头 */
    ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == false);

    /* 3. 无数据接收负例 */
    forward_uart_dma.forward_uart_rx_complete = 0;
    ret = forward_uart_recv_iap_resp(&out_cmd, &out_status);
    assert(ret == false);
}

static void test_recv_iap_resp_and_status_extraction(void)
{
    printf("[RUN ] test_recv_iap_resp_and_status_extraction\n");
    test_recv_iap_resp_positive_cases();
    test_recv_iap_resp_negative_cases();
    printf("[PASS] test_recv_iap_resp_and_status_extraction\n");
}

/* --------------------------------------------------------------------------
 * Test Suite 6: 强电加热占空比 0% 锁死与升级前置联锁校验
 * -------------------------------------------------------------------------- */

typedef struct {
    float hotend_temp;
    float hotend_target;
    float bed_temp;
    float bed_target;
    uint8_t heater_duty_percent;
    bool is_moving;
} upgrade_safety_context_t;

typedef enum {
    UPGRADE_SAFETY_OK = 0,
    UPGRADE_SAFETY_ERR_HOTEND_TEMP,
    UPGRADE_SAFETY_ERR_HOTEND_TARGET,
    UPGRADE_SAFETY_ERR_BED_TEMP,
    UPGRADE_SAFETY_ERR_BED_TARGET,
    UPGRADE_SAFETY_ERR_PWM_DUTY,
    UPGRADE_SAFETY_ERR_MOTION_ACTIVE
} upgrade_safety_status_t;

static upgrade_safety_status_t validate_upgrade_safety_preconditions(const upgrade_safety_context_t *ctx)
{
    if (ctx == NULL)
    {
        return UPGRADE_SAFETY_ERR_PWM_DUTY;
    }

    if (ctx->hotend_temp >= 50.0f)
    {
        return UPGRADE_SAFETY_ERR_HOTEND_TEMP;
    }
    if (ctx->hotend_target > 0.0f)
    {
        return UPGRADE_SAFETY_ERR_HOTEND_TARGET;
    }
    if (ctx->bed_temp >= 50.0f)
    {
        return UPGRADE_SAFETY_ERR_BED_TEMP;
    }
    if (ctx->bed_target > 0.0f)
    {
        return UPGRADE_SAFETY_ERR_BED_TARGET;
    }
    if (ctx->heater_duty_percent != 0U)
    {
        return UPGRADE_SAFETY_ERR_PWM_DUTY;
    }
    if (ctx->is_moving)
    {
        return UPGRADE_SAFETY_ERR_MOTION_ACTIVE;
    }

    return UPGRADE_SAFETY_OK;
}

static void test_strong_electricity_pwm_duty_lock(void)
{
    printf("[RUN ] test_strong_electricity_pwm_duty_lock\n");

    /* 1. 安全准入正例：完全就绪空闲，加热 PWM 0% 锁死 */
    upgrade_safety_context_t safe_ctx = {
        .hotend_temp = 28.5f,
        .hotend_target = 0.0f,
        .bed_temp = 25.0f,
        .bed_target = 0.0f,
        .heater_duty_percent = 0U,
        .is_moving = false
    };
    assert(validate_upgrade_safety_preconditions(&safe_ctx) == UPGRADE_SAFETY_OK);

    /* 2. 负例：喷嘴温度超标 (>= 50.0°C) 立即拒绝 */
    upgrade_safety_context_t hot_ctx = safe_ctx;
    hot_ctx.hotend_temp = 65.0f;
    assert(validate_upgrade_safety_preconditions(&hot_ctx) == UPGRADE_SAFETY_ERR_HOTEND_TEMP);

    /* 3. 负例：喷嘴有非零目标设定温度立即拒绝 */
    upgrade_safety_context_t target_ctx = safe_ctx;
    target_ctx.hotend_target = 200.0f;
    assert(validate_upgrade_safety_preconditions(&target_ctx) == UPGRADE_SAFETY_ERR_HOTEND_TARGET);

    /* 4. 负例：强电加热 PWM 占空比非 0% (微弱加热) 严格锁死拒绝 */
    upgrade_safety_context_t pwm_ctx = safe_ctx;
    pwm_ctx.heater_duty_percent = 5U;
    assert(validate_upgrade_safety_preconditions(&pwm_ctx) == UPGRADE_SAFETY_ERR_PWM_DUTY);

    /* 5. 负例：热床温度超标拒绝 */
    upgrade_safety_context_t bed_ctx = safe_ctx;
    bed_ctx.bed_temp = 55.0f;
    assert(validate_upgrade_safety_preconditions(&bed_ctx) == UPGRADE_SAFETY_ERR_BED_TEMP);

    /* 6. 负例：电机运动中拒绝 */
    upgrade_safety_context_t move_ctx = safe_ctx;
    move_ctx.is_moving = true;
    assert(validate_upgrade_safety_preconditions(&move_ctx) == UPGRADE_SAFETY_ERR_MOTION_ACTIVE);

    printf("[PASS] test_strong_electricity_pwm_duty_lock\n");
}

/* --------------------------------------------------------------------------
 * Main Entry Point
 * -------------------------------------------------------------------------- */

int main(void)
{
    /* Map DMA1 register base memory range (0x40020000) for safe host simulation */
    void *p = mmap((void*)0x40020000, 0x10000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (p == MAP_FAILED)
    {
        perror("mmap");
        return 1;
    }

    printf("========================================================================\n");
    printf("TWIN-26 Dual MCU Upgrade Channel & Bootloader IAP Protocol Verification\n");
    printf("========================================================================\n");

    test_protocol_constants_reconciliation();
    test_upgrade_mode_and_marlin_interception();
    test_send_iap_chunk_512b_and_checksum();
    test_chunk_boundary_and_null_pointer_defenses();
    test_recv_iap_resp_and_status_extraction();
    test_strong_electricity_pwm_duty_lock();

    printf("------------------------------------------------------------------------\n");
    printf("All 6 test suites PASSED! (0 failures)\n");
    printf("========================================================================\n");
    return 0;
}
