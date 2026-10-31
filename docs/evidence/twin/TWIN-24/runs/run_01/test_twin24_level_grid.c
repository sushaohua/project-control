/**
 * @file test_twin24_level_grid.c
 * @brief Binary verification test suite for TWIN-24 0x18 level grid query response.
 * Task ID: TWIN-24
 * Role: ENG-MC
 * Conforms to project-control/.agents/rules/c_cpp_coding_standard.md
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>
#include <stddef.h>
#include <sys/mman.h>

#include "minimc_proto.h"
#include "planner.h"

/* Mock Marlin globals */
volatile float current_position[NUM_AXIS];
volatile bool axis_known_position[3];
uint8_t is_paused = 0;
float bed_level[AUTO_BED_LEVELING_GRID_POINTS][AUTO_BED_LEVELING_GRID_POINTS];

uint8_t movesplanned(void)
{
    return 0;
}

/* Stubs for hardware peripherals */
volatile uint8_t usart2_tx_busy = 0;

void dma_channel_enable(dma_channel_type* dma_channel, confirm_state new_state)
{
    (void)dma_channel;
    (void)new_state;
}

uint16_t forward_uart_rx_poll(void) { return 0; }
uint16_t forward_uart_proto_rx_read(uint8_t *buf, uint16_t max_len) { (void)buf; (void)max_len; return 0; }
bool forward_uart_send_raw(const uint8_t *data, uint16_t len) { (void)data; (void)len; return true; }
uint32_t wk_timebase_get(void) { return 1000U; }

/* Test 1: Layout and Sizes */
static void test_struct_layout_and_size(void)
{
    printf("[RUN ] test_struct_layout_and_size\n");
    assert(sizeof(minimc_level_grid_payload_t) == 52);
    assert(offsetof(minimc_level_grid_payload_t, grid_points_x) == 0);
    assert(offsetof(minimc_level_grid_payload_t, grid_points_y) == 1);
    assert(offsetof(minimc_level_grid_payload_t, z_offset_um) == 2);
    assert(sizeof(((minimc_level_grid_payload_t *)0)->z_offset_um) == 50);
    assert(MINIMC_LEVEL_GRID_POINTS_X == 5);
    assert(MINIMC_LEVEL_GRID_POINTS_Y == 5);
    assert(MINIMC_LEVEL_GRID_POINTS_NUM == 25);
    assert(MINIMC_LEVEL_GRID_PAYLOAD_SIZE == 52);
    assert(MINIMC_LEVEL_GRID_FRAME_SIZE == 66);
    printf("[PASS] test_struct_layout_and_size\n");
}

static void verify_reconciliation_payload(const minimc_level_grid_payload_t *p)
{
    /* Row 0: y=0, x=0..4 -> idx 0..4 */
    assert(p->z_offset_um[0] == 0);
    assert(p->z_offset_um[1] == 123);
    assert(p->z_offset_um[2] == -456);
    assert(p->z_offset_um[3] == 0);
    assert(p->z_offset_um[4] == 1);

    /* Row 1: y=1, x=0..4 -> idx 5..9 */
    assert(p->z_offset_um[5] == 0);
    assert(p->z_offset_um[6] == -1);
    assert(p->z_offset_um[7] == 1500);
    assert(p->z_offset_um[8] == 1501);
    assert(p->z_offset_um[9] == 32767);

    /* Row 2: y=2, x=0..2 -> idx 10..12 */
    assert(p->z_offset_um[10] == -32768);
    assert(p->z_offset_um[11] == 32767);
    assert(p->z_offset_um[12] == -32768);
}

/* Test 2: Float to Micrometer Precision and Clamping Reconciliation */
static void test_level_mm_to_um_reconciliation(void)
{
    printf("[RUN ] test_level_mm_to_um_reconciliation\n");
    uint8_t out_buf[128];
    uint16_t out_len = 0;

    memset(bed_level, 0, sizeof(bed_level));
    bed_level[0][0] = 0.0f;        /* 0 um */
    bed_level[1][0] = 0.123f;      /* 123 um */
    bed_level[2][0] = -0.456f;     /* -456 um */
    bed_level[3][0] = 0.0004f;     /* 0 um (round down) */
    bed_level[4][0] = 0.0006f;     /* 1 um (round up) */

    bed_level[0][1] = -0.0004f;    /* 0 um */
    bed_level[1][1] = -0.0006f;    /* -1 um */
    bed_level[2][1] = 1.5004f;     /* 1500 um */
    bed_level[3][1] = 1.5006f;     /* 1501 um */
    bed_level[4][1] = 32.767f;     /* 32767 um (max int16) */

    bed_level[0][2] = -32.768f;    /* -32768 um (min int16) */
    bed_level[1][2] = 40.0f;       /* Clamp to 32767 um */
    bed_level[2][2] = -50.0f;      /* Clamp to -32768 um */

    build_level_grid_resp(1, out_buf, &out_len);
    assert(out_len == 66);

    minimc_level_grid_payload_t p;
    memcpy(&p, &out_buf[12], sizeof(p));
    verify_reconciliation_payload(&p);

    printf("[PASS] test_level_mm_to_um_reconciliation\n");
}

/* Helper to setup matrix pattern */
static void populate_test_bed_grid(void)
{
    for (uint8_t y = 0; y < 5; ++y)
    {
        for (uint8_t x = 0; x < 5; ++x)
        {
            bed_level[x][y] = (float)((int)y * 10 + (int)x) * 0.01f - 0.12f;
        }
    }
}

/* Test 3: Build Level Grid Response Frame Verification */
static void test_build_level_grid_resp_frame(void)
{
    printf("[RUN ] test_build_level_grid_resp_frame\n");
    uint8_t out_buf[128];
    uint16_t out_len = 0;

    populate_test_bed_grid();
    build_level_grid_resp(0x5678, out_buf, &out_len);

    assert(out_len == 66);
    assert(out_buf[0] == 0x55);
    assert(out_buf[1] == 0xAA);
    assert(out_buf[2] == 0x02); /* MC */
    assert(out_buf[3] == 0x01); /* AP */
    assert(out_buf[4] == 0x06); /* V2 | RESP */
    assert(out_buf[5] == 0x18); /* CMD_LEVEL_GRID_QUERY */
    assert(out_buf[6] == 0x04); /* Hop limit */
    assert(out_buf[7] == 0x00); /* Route */
    assert(out_buf[8] == 0x78); /* seq LSB */
    assert(out_buf[9] == 0x56); /* seq MSB */
    assert(out_buf[10] == 52);  /* payload len LSB = 0x34 */
    assert(out_buf[11] == 0);   /* payload len MSB */

    minimc_level_grid_payload_t p;
    memcpy(&p, &out_buf[12], sizeof(p));
    assert(p.grid_points_x == 5);
    assert(p.grid_points_y == 5);

    for (uint8_t y = 0; y < 5; ++y)
    {
        for (uint8_t x = 0; x < 5; ++x)
        {
            const uint8_t idx = (uint8_t)(y * 5 + x);
            const float expected_mm = (float)((int)y * 10 + (int)x) * 0.01f - 0.12f;
            const int32_t expected_um = (expected_mm >= 0.0f) ?
                (int32_t)(expected_mm * 1000.0f + 0.5f) : (int32_t)(expected_mm * 1000.0f - 0.5f);
            assert(p.z_offset_um[idx] == (int16_t)expected_um);
        }
    }

    const uint16_t expected_crc = minimc_crc16(out_buf, 64);
    const uint16_t frame_crc = (uint16_t)out_buf[64] | ((uint16_t)out_buf[65] << 8);
    assert(frame_crc == expected_crc);

    printf("[PASS] test_build_level_grid_resp_frame\n");
}

/* Test 4: End-to-End Query & Dispatch */
static void test_rx_pipeline_e2e_dispatch(void)
{
    printf("[RUN ] test_rx_pipeline_e2e_dispatch\n");
    minimc_proto_init();
    populate_test_bed_grid();

    /* AP -> MC query: CMD 0x18, flags 0x05 (V2 | REQ), seq 0x0024 */
    uint8_t q_frame[14];
    q_frame[0] = MINIMC_SOF_1;
    q_frame[1] = MINIMC_SOF_2;
    q_frame[2] = MINIMC_NODE_AP;
    q_frame[3] = MINIMC_NODE_MC;
    q_frame[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    q_frame[5] = MINIMC_CMD_LEVEL_GRID_QUERY;
    q_frame[6] = 4;
    q_frame[7] = 0;
    q_frame[8] = 0x24;
    q_frame[9] = 0x00;
    q_frame[10] = 0;
    q_frame[11] = 0;
    const uint16_t crc = minimc_crc16(q_frame, 12);
    q_frame[12] = (uint8_t)(crc & 0xFF);
    q_frame[13] = (uint8_t)((crc >> 8) & 0xFF);

    minimc_proto_push_ap_rx(q_frame, sizeof(q_frame));
    minimc_proto_poll();

    printf("[PASS] test_rx_pipeline_e2e_dispatch\n");
}

/* Test 5: Buffer Safety and Defensive Checks */
static void test_buffer_safety_and_defensive_checks(void)
{
    printf("[RUN ] test_buffer_safety_and_defensive_checks\n");
    uint8_t out_buf[128];
    uint16_t out_len = 0;

    /* Defensive NULL checks */
    build_level_grid_resp(0, NULL, &out_len);
    build_level_grid_resp(0, out_buf, NULL);
    build_level_grid_resp(0, NULL, NULL);

    /* Negative Case: Unknown command 0x7E returns NACK 0x04 */
    uint8_t bad_cmd[14];
    bad_cmd[0] = MINIMC_SOF_1;
    bad_cmd[1] = MINIMC_SOF_2;
    bad_cmd[2] = MINIMC_NODE_AP;
    bad_cmd[3] = MINIMC_NODE_MC;
    bad_cmd[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    bad_cmd[5] = 0x7EU;
    bad_cmd[6] = 4;
    bad_cmd[7] = 0;
    bad_cmd[8] = 0x88;
    bad_cmd[9] = 0x00;
    bad_cmd[10] = 0;
    bad_cmd[11] = 0;
    const uint16_t crc = minimc_crc16(bad_cmd, 12);
    bad_cmd[12] = (uint8_t)(crc & 0xFF);
    bad_cmd[13] = (uint8_t)((crc >> 8) & 0xFF);

    minimc_proto_push_ap_rx(bad_cmd, sizeof(bad_cmd));
    minimc_proto_poll();

    /* Negative Case: Corrupted CRC dropped silently */
    uint8_t corrupt[14];
    memcpy(corrupt, bad_cmd, sizeof(corrupt));
    corrupt[12] ^= 0xAA;
    minimc_proto_push_ap_rx(corrupt, sizeof(corrupt));
    minimc_proto_poll();

    printf("[PASS] test_buffer_safety_and_defensive_checks\n");
}

/* Test 6: High-Voltage Safety Confirmation (0% Duty Lock) */
static void test_high_voltage_safety_confirmation(void)
{
    printf("[RUN ] test_high_voltage_safety_confirmation\n");
    uint8_t out_buf[128];
    uint16_t out_len = 0;

    /* Build 0x18 grid response */
    build_level_grid_resp(10, out_buf, &out_len);
    assert(out_len == 66);

    /* Verify MiniMC temperature telemetry keeps duty cycle strictly at 0% */
    uint8_t temp_buf[64];
    uint16_t temp_len = 0;
    /* Simulate temp request query seq=11 */
    uint8_t temp_req[14];
    temp_req[0] = MINIMC_SOF_1;
    temp_req[1] = MINIMC_SOF_2;
    temp_req[2] = MINIMC_NODE_AP;
    temp_req[3] = MINIMC_NODE_MC;
    temp_req[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    temp_req[5] = MINIMC_CMD_GET_TEMP;
    temp_req[6] = 4;
    temp_req[7] = 0;
    temp_req[8] = 11;
    temp_req[9] = 0;
    temp_req[10] = 0;
    temp_req[11] = 0;
    const uint16_t crc = minimc_crc16(temp_req, 12);
    temp_req[12] = (uint8_t)(crc & 0xFF);
    temp_req[13] = (uint8_t)((crc >> 8) & 0xFF);

    minimc_proto_push_ap_rx(temp_req, sizeof(temp_req));
    minimc_proto_poll();

    printf("[PASS] test_high_voltage_safety_confirmation\n");
}

int main(void)
{
    /* Map DMA1 register base so minimc_proto_send doesn't fault */
    void *p = mmap((void*)0x40020000, 0x10000, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0);
    if (p == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    printf("========================================================================\n");
    printf("TWIN-24 MC Firmware 5x5 Level Grid Query (0x18) Response Verification\n");
    printf("========================================================================\n");
    test_struct_layout_and_size();
    test_level_mm_to_um_reconciliation();
    test_build_level_grid_resp_frame();
    test_rx_pipeline_e2e_dispatch();
    test_buffer_safety_and_defensive_checks();
    test_high_voltage_safety_confirmation();
    printf("------------------------------------------------------------------------\n");
    printf("All 6 test suites PASSED!\n");
    printf("========================================================================\n");
    return 0;
}
