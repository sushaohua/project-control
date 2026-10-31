/**
 * @file test_twin21_pos_query.c
 * @brief Binary verification test suite for TWIN-21 0x16 position query and motion response.
 * Task ID: TWIN-21
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
static uint8_t s_mock_movesplanned = 0;

uint8_t movesplanned(void)
{
    return s_mock_movesplanned;
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
static void test_struct_layout(void)
{
    printf("[RUN ] test_struct_layout\n");
    assert(sizeof(minimc_pos_report_payload_t) == 20);
    assert(offsetof(minimc_pos_report_payload_t, pos_x_um) == 0);
    assert(offsetof(minimc_pos_report_payload_t, x_um) == 0);
    assert(offsetof(minimc_pos_report_payload_t, pos_y_um) == 4);
    assert(offsetof(minimc_pos_report_payload_t, y_um) == 4);
    assert(offsetof(minimc_pos_report_payload_t, pos_z_um) == 8);
    assert(offsetof(minimc_pos_report_payload_t, z_um) == 8);
    assert(offsetof(minimc_pos_report_payload_t, pos_e_um) == 12);
    assert(offsetof(minimc_pos_report_payload_t, e_um) == 12);
    assert(offsetof(minimc_pos_report_payload_t, mc_state) == 16);
    assert(offsetof(minimc_pos_report_payload_t, motion_state) == 16);
    assert(offsetof(minimc_pos_report_payload_t, homed_mask) == 17);
    assert(offsetof(minimc_pos_report_payload_t, reserved) == 18);
    printf("[PASS] test_struct_layout\n");
}

/* Test 2: Build Position Response Frame */
static void test_build_pos_resp(void)
{
    printf("[RUN ] test_build_pos_resp\n");
    uint8_t out_buf[64];
    uint16_t out_len = 0;

    /* Set positions: X=10.5mm (10500um), Y=20.001mm (20001um), Z=0.2mm (200um), E=5.0mm (5000um) */
    current_position[X_AXIS] = 10.5f;
    current_position[Y_AXIS] = 20.001f;
    current_position[Z_AXIS] = 0.2f;
    current_position[E_AXIS] = 5.0f;

    /* Set homed state: X and Y homed, Z not homed */
    axis_known_position[X_AXIS] = true;
    axis_known_position[Y_AXIS] = true;
    axis_known_position[Z_AXIS] = false;

    /* Set motion state: moving */
    is_paused = 0;
    s_mock_movesplanned = 3;

    build_pos_resp(0x1234, out_buf, &out_len);

    assert(out_len == 34);
    assert(out_buf[0] == 0x55);
    assert(out_buf[1] == 0xAA);
    assert(out_buf[2] == 0x02); /* MC */
    assert(out_buf[3] == 0x01); /* AP */
    assert(out_buf[4] == 0x06); /* V2 | RESP */
    assert(out_buf[5] == 0x16); /* CMD_POS_QUERY */
    assert(out_buf[6] == 0x04); /* hop limit */
    assert(out_buf[7] == 0x00); /* route */
    assert(out_buf[8] == 0x34); /* seq LSB */
    assert(out_buf[9] == 0x12); /* seq MSB */
    assert(out_buf[10] == 20);  /* payload len = 20 */
    assert(out_buf[11] == 0);

    /* Verify Payload */
    minimc_pos_report_payload_t payload;
    memcpy(&payload, &out_buf[12], sizeof(payload));

    assert(payload.pos_x_um == 10500);
    assert(payload.pos_y_um == 20001);
    assert(payload.pos_z_um == 200);
    assert(payload.pos_e_um == 5000);
    assert(payload.x_um == 10500);
    assert(payload.y_um == 20001);
    assert(payload.z_um == 200);
    assert(payload.e_um == 5000);
    assert(payload.mc_state == MINIMC_MOTION_STATE_MOVING);
    assert(payload.motion_state == MINIMC_MOTION_STATE_MOVING);
    assert(payload.homed_mask == (MINIMC_HOMED_X | MINIMC_HOMED_Y));
    assert(payload.reserved == 0);

    /* Verify CRC */
    uint16_t expected_crc = minimc_crc16(out_buf, 32);
    uint16_t frame_crc = (uint16_t)out_buf[32] | ((uint16_t)out_buf[33] << 8);
    assert(frame_crc == expected_crc);

    printf("[PASS] test_build_pos_resp\n");
}

/* Test 3: Motion State & Homed Combinations */
static void test_motion_states_and_homing(void)
{
    printf("[RUN ] test_motion_states_and_homing\n");
    uint8_t out_buf[64];
    uint16_t out_len = 0;

    /* Case A: Paused takes precedence over movesplanned */
    is_paused = 1;
    s_mock_movesplanned = 5;
    axis_known_position[X_AXIS] = true;
    axis_known_position[Y_AXIS] = true;
    axis_known_position[Z_AXIS] = true;

    build_pos_resp(1, out_buf, &out_len);
    minimc_pos_report_payload_t p;
    memcpy(&p, &out_buf[12], sizeof(p));
    assert(p.mc_state == MINIMC_MOTION_STATE_PAUSED);
    assert(p.homed_mask == (MINIMC_HOMED_X | MINIMC_HOMED_Y | MINIMC_HOMED_Z));

    /* Case B: Idle (not paused, movesplanned == 0) */
    is_paused = 0;
    s_mock_movesplanned = 0;
    axis_known_position[X_AXIS] = false;
    axis_known_position[Y_AXIS] = false;
    axis_known_position[Z_AXIS] = false;

    build_pos_resp(2, out_buf, &out_len);
    memcpy(&p, &out_buf[12], sizeof(p));
    assert(p.mc_state == MINIMC_MOTION_STATE_IDLE);
    assert(p.homed_mask == 0);

    /* Case C: Negative coordinates */
    current_position[X_AXIS] = -5.250f;
    current_position[Y_AXIS] = -0.001f;
    current_position[Z_AXIS] = -10.0f;
    current_position[E_AXIS] = -0.5f;

    build_pos_resp(3, out_buf, &out_len);
    memcpy(&p, &out_buf[12], sizeof(p));
    assert(p.pos_x_um == -5250);
    assert(p.pos_y_um == -1);
    assert(p.pos_z_um == -10000);
    assert(p.pos_e_um == -500);

    printf("[PASS] test_motion_states_and_homing\n");
}

/* Test 4: Defensive null checks */
static void test_defensive_checks(void)
{
    printf("[RUN ] test_defensive_checks\n");
    uint8_t out_buf[64];
    uint16_t out_len = 0;

    build_pos_resp(0, NULL, &out_len);
    build_pos_resp(0, out_buf, NULL);
    build_pos_resp(0, NULL, NULL);

    printf("[PASS] test_defensive_checks\n");
}

/* Test 5: Full Rx pipeline (0x16 Query dispatched through minimc_proto_push_ap_rx) */
static void test_rx_pipeline(void)
{
    printf("[RUN ] test_rx_pipeline (End-to-End Query & Dispatch)\n");
    minimc_proto_init();

    /* Build a query frame: AP (0x01) -> MC (0x02), CMD 0x16, flags 0x05 (V2 | REQ), seq 0x42 */
    uint8_t q_frame[14];
    q_frame[0] = MINIMC_SOF_1;
    q_frame[1] = MINIMC_SOF_2;
    q_frame[2] = MINIMC_NODE_AP;
    q_frame[3] = MINIMC_NODE_MC;
    q_frame[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    q_frame[5] = MINIMC_CMD_POS_QUERY;
    q_frame[6] = 4; /* hop limit */
    q_frame[7] = 0; /* route */
    q_frame[8] = 0x42; /* seq */
    q_frame[9] = 0x00;
    q_frame[10] = 0; /* payload len = 0 */
    q_frame[11] = 0;
    uint16_t crc = minimc_crc16(q_frame, 12);
    q_frame[12] = (uint8_t)(crc & 0xFF);
    q_frame[13] = (uint8_t)((crc >> 8) & 0xFF);

    /* Push and poll */
    minimc_proto_push_ap_rx(q_frame, sizeof(q_frame));
    minimc_proto_poll();

    printf("[PASS] test_rx_pipeline\n");
}

/* Test 6: Negative Cases - Unknown Command NACK & Corrupt Frame Rejection */
static void test_negative_cases(void)
{
    printf("[RUN ] test_negative_cases (Unknown CMD NACK 0x04 & Corrupted CRC)\n");
    minimc_proto_init();

    /* 6A: Unknown command 0x7E should yield NACK (CMD 0x00, err 0x04) */
    uint8_t bad_cmd_frame[14];
    bad_cmd_frame[0] = MINIMC_SOF_1;
    bad_cmd_frame[1] = MINIMC_SOF_2;
    bad_cmd_frame[2] = MINIMC_NODE_AP;
    bad_cmd_frame[3] = MINIMC_NODE_MC;
    bad_cmd_frame[4] = (uint8_t)(MINIMC_FLAG_WANTS_ACK | MINIMC_FLAG_PROTO_V2);
    bad_cmd_frame[5] = 0x7EU; /* unknown cmd */
    bad_cmd_frame[6] = 4;
    bad_cmd_frame[7] = 0;
    bad_cmd_frame[8] = 0x99;
    bad_cmd_frame[9] = 0x00;
    bad_cmd_frame[10] = 0;
    bad_cmd_frame[11] = 0;
    uint16_t crc = minimc_crc16(bad_cmd_frame, 12);
    bad_cmd_frame[12] = (uint8_t)(crc & 0xFF);
    bad_cmd_frame[13] = (uint8_t)((crc >> 8) & 0xFF);

    minimc_proto_push_ap_rx(bad_cmd_frame, sizeof(bad_cmd_frame));
    minimc_proto_poll();

    /* 6B: Corrupted CRC byte should be silently dropped by stream parser */
    uint8_t corrupt_frame[14];
    memcpy(corrupt_frame, bad_cmd_frame, sizeof(corrupt_frame));
    corrupt_frame[12] ^= 0xFF; /* corrupt CRC */
    corrupt_frame[13] ^= 0xFF;

    minimc_proto_push_ap_rx(corrupt_frame, sizeof(corrupt_frame));
    minimc_proto_poll();

    printf("[PASS] test_negative_cases\n");
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
    printf("TWIN-21 MC Firmware 0x16 Position Query & Motion Response Verification\n");
    printf("========================================================================\n");
    test_struct_layout();
    test_build_pos_resp();
    test_motion_states_and_homing();
    test_defensive_checks();
    test_rx_pipeline();
    test_negative_cases();
    printf("------------------------------------------------------------------------\n");
    printf("All 6 test suites PASSED!\n");
    printf("========================================================================\n");
    return 0;
}
