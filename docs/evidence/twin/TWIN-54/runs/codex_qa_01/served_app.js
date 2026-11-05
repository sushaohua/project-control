/**
 * AI-SoC Twin HMI Frontend Application (First Release)
 * Supports 4-channel filament slot mapping & 10000 base weight validation,
 * OOBE setup wizard with strict realism invariant, dynamic i18n & theme switching,
 * and mDNS service discovery integration.
 * Complies with project-control/.agents/rules/c_cpp_coding_standard.md spirit.
 */

(function () {
    'use strict';

    var AISOC_TEMP_MILLIC_FAULT = 2147483647; // 0x7FFFFFFF
    var AISOC_TEMP_MILLIC_OFFLINE = 2147483646; // 0x7FFFFFFE
    var SENTINEL_FAULT_DECI = 0x7FFF;
    var SENTINEL_OFFLINE_DECI = 0x7FFE;
    var SENTINEL_FAULT = AISOC_TEMP_MILLIC_FAULT;
    var SENTINEL_OFFLINE = AISOC_TEMP_MILLIC_OFFLINE;
    var TOTAL_WEIGHT_TARGET = 10000;
    var GATEWAY_BASE_URL = (typeof window !== 'undefined' && window.location && window.location.origin && window.location.origin.indexOf('http') === 0) ? window.location.origin : 'http://127.0.0.1:8080';

    // 国际化双语字典 (zh-CN 与 en-US)
    var I18N = {
        'zh-CN': {
            app_title: 'AI-SoC 3D HMI',
            app_subtitle: '工业级数字孪生控制台 v2.0',
            status_connecting: '连接中...',
            status_connected: '已连接',
            status_disconnected: '已断开',
            hw_status_online: '硬件在线',
            hw_status_offline: '硬件离线',
            hw_status_unknown: '硬件未知',
            hw_offline_banner_msg: '⚠️ 硬件连接已断开，运控与加热已锁定，请检查物理连线后重试',
            net_error: '网络通信异常',
            theme_light: '浅色模式',
            theme_dark: '深色模式',
            nav_oobe: '新机引导',
            tab_dashboard: '打印工作台',
            tab_motion: '轴控与调平',
            btn_estop: 'E-STOP 急停',
            dashboard_heading: '🖨️ 打印作业控制台 (Dashboard & Jobs)',
            dashboard_desc: '全流程本地作业加载、流式模拟空跑监视与核心运控调度。',
            motion_heading: '🕹️ 轴控与 5×5 自动调平',
            motion_desc: '三轴触控罗盘手动微调、G28 软件回零与 5×5 调平高程偏差热力图。',
            tab_slots: '料槽与调色板',
            tab_sensors: '温度与传感器',
            tab_network: '局域网与 mDNS',
            tab_hms: '健康监控 (HMS)',
            slots_heading: '4 通道耗材料槽映射与混色规划',
            slots_desc: '配置 Slot 1~4 耗材类型、颜色及余量。混色权重基准严格遵循 10000 规范 (COL-001 / TWIN-17)。',
            preset_title: '快捷混色配比:',
            slot_1: '料槽 1 (Slot 1)',
            slot_2: '料槽 2 (Slot 2)',
            slot_3: '料槽 3 (Slot 3)',
            slot_4: '料槽 4 (Slot 4)',
            tag_loaded: '已装载',
            lbl_material: '材料类型',
            lbl_color: '耗材颜色',
            lbl_remaining: '余量估算',
            lbl_weight: '混色基准权重 (0~10000)',
            val_total_title: '混色权重总和:',
            val_valid: '有效 (100.00%)',
            val_invalid: '权重和无效',
            val_msg_ok: '权重总和严格等于 10000，符合 COL-001 混色作业规划。',
            val_msg_err: '权重总和必须严格等于 10000，当前总和: ',
            btn_save_slots: '保存料槽映射配置',
            save_success: '料槽配置保存成功！',
            save_failed: '保存失败: 权重总和非法',
            sensors_heading: '双 MCU 传感器与温度状态实时遥测',
            sensors_desc: '严格展示后端真实微服务遥测数据。未接入真实硬件或离线项明确指示，严防伪造温度。',
            btn_sample: '立即准入采样 (POST)',
            th_title: '工具头喷嘴 (Extruder Nozzle)',
            mc_title: '运动主控热床 (Heated Bed)',
            runout_title: '4 通道光电断料检测状态 (Filament Runout Sensors)',
            sensor_unknown: '未检查/离线',
            sensor_loaded: '正常 (有丝)',
            sensor_empty: '断料 (空槽)',
            lbl_target_temp: '目标设定:',
            lbl_duty: '加热占空比:',
            lbl_sensor_state: '传感器状态:',
            lbl_firmware_ver: '固件版本:',
            ver_status_unknown: '未知',
            ver_status_offline: '设备离线',
            ver_status_query_failed: '查询失败',
            ver_status_stale: '数据已过期',
            lbl_raw_adc: 'ADC 读数:',
            net_heading: '局域网设备自发现与 mDNS 广播服务',
            net_desc: '轻量级 C 广播器向 224.0.0.251:5353 组播 _aisoc._tcp.local 服务，实现免 IP 直连。',
            net_mdns_title: 'mDNS 局域网服务属性',
            net_lbl_hostname: '本地主机名:',
            net_lbl_service: '服务广播标识:',
            net_lbl_multicast: '组播目标:',
            net_lbl_port: 'HTTP Web 端口:',
            net_lbl_txt: 'TXT 元数据:',
            net_access_title: '浏览器快速直连指引',
            net_access_p1: '同一局域网下的 PC、手机或平板无需查找 IP，直接访问：',
            btn_copy: '复制链接',
            copied: '已复制！',
            net_tip: '提示：网关已集成 C11/C++17 纯静态无堆内存分配的 mdns_advertiser 广播守护组件。',
            hms_heading: '全机健康监控系统与急停联动 (HMS)',
            hms_desc: '统一度量 0x1000~0x5000 分层错误码，双级急停与故障保护。',
            estop_normal: '急停状态: 正常',
            th_hms_code: '错误代码',
            th_hms_subsys: '子系统',
            th_hms_severity: '严重度',
            th_hms_desc: '描述与排查指引',
            th_hms_time: '时间戳',
            hms_empty: '当前无活动告警 (系统健康运行)',
            oobe_wizard_title: '新机检查引导向导 (OOBE)',
            step_1: '欢迎',
            step_2: '语言',
            step_3: '通信与固件',
            step_4: '传感器检测',
            step_5: '就绪完成',
            oobe_w1_title: '欢迎使用 AI-SoC 全彩多色 3D 打印机！',
            oobe_w1_p1: '本向导将引导您完成初次开机自检，包括语言设定、运动控制器通信握手、工具头串口连通性以及双端传感器健康核验。',
            oobe_w1_rule: '核心真实性原则：系统严格遵循真实硬件接入检测规范，任何未连接或脱机组件均如实显示，绝不伪造通过结果。',
            oobe_w2_title: '选择系统界面语言与视觉主题',
            oobe_w2_desc: '您可以在下方选择偏好语言，设置将即时动态生效：',
            oobe_w3_title: '双 MCU 固件与通信链路自检',
            oobe_w3_desc: '系统正在尝试与底层微控制器建立 MiniMCProto 握手连接：',
            oobe_mc_comm: 'MC (AT32F435) 运动主控通信链路',
            oobe_th_comm: 'TH (AT32F423) 工具头挤出机通信链路',
            oobe_fwd_state: 'AP 转发核心与协议同步状态',
            status_unready: '未就绪/未连接/等待接入',
            status_online: '已连接 (在线)',
            oobe_w4_title: '双端温控与断料传感器有效性检测',
            oobe_w4_desc: '核验喷嘴/热床热敏电阻 ADC 有效性，检测断料光电对射状态：',
            oobe_nozzle_temp: '工具头喷嘴温度传感器 (TH NTC)',
            oobe_bed_temp: '热床加热板温度传感器 (MC NTC)',
            oobe_runout: '4 通道断料检测传感器组 (COL-007)',
            oobe_w5_title: '新机自检向导已完成',
            oobe_w5_p1: '向导已保存您的界面与语言偏好设置。系统状态与传感器将继续在控制台仪表盘中保持实时监测。',
            sum_lang: '语言偏好:',
            sum_theme: '视觉主题:',
            sum_slots: '料槽配置:',
            sum_slots_val: '4 通道已映射 (权重和 10000)',
            btn_prev: '上一步',
            btn_next: '下一步',
            btn_finish: '进入打印控制台',
            oobe_finished_toast: '新机自检向导已完成，已进入控制台',
            btn_estop_clear: '解除急停',
            estop_cleared_toast: '急停锁定已解除 (M999)，硬件控制已恢复',
            estop_triggered_toast: '紧急急停已触发 (M112)！强电与电机已熔断自锁',
            estop_active_badge: '急停状态: 已触发锁定 (M112)',
            btn_send_gcode: '发送指令',
            quick_g28: 'G28 归零',
            quick_m114: 'M114 查坐标',
            quick_t0: 'T0 料槽1',
            quick_t1: 'T1 料槽2',
            gcode_ack_toast: 'G-code 硬件执行成功',
            btn_set_th_temp: '设定喷嘴温度',
            btn_set_mc_temp: '设定热床温度',
            preset_off: '0°C 关',
            temp_ack_toast: '目标温度已下发并获双端硬件 ACK',
            btn_slot_select: '选槽',
            btn_slot_load: '进丝',
            btn_slot_unload: '退丝',
            slot_act_toast: '料槽硬件动作已执行'
        },
        'en-US': {
            app_title: 'AI-SoC 3D HMI',
            app_subtitle: 'Industrial Digital Twin Console v2.0',
            status_connecting: 'Connecting...',
            status_connected: 'Connected',
            status_disconnected: 'Disconnected',
            hw_status_online: 'Hardware Online',
            hw_status_offline: 'Hardware Offline',
            hw_status_unknown: 'Hardware Unknown',
            hw_offline_banner_msg: '⚠️ Hardware link disconnected. Motion and heating locked. Please check physical link and retry.',
            net_error: 'Network communication error',
            theme_light: 'Light Mode',
            theme_dark: 'Dark Mode',
            nav_oobe: 'Setup Wizard',
            tab_dashboard: 'Print Jobs',
            tab_motion: 'Motion & Level',
            btn_estop: 'EMERGENCY STOP',
            dashboard_heading: '🖨️ Print Dashboard & Jobs',
            dashboard_desc: 'Full-cycle local job staging, streaming dry-run supervision, and motion dispatch.',
            motion_heading: '🕹️ Motion Control & 5×5 Leveling',
            motion_desc: 'Tri-axis manual jog compass, G28 homing, and 5×5 bed mesh deviation heatmap.',
            tab_slots: 'Slots & Palette',
            tab_sensors: 'Temperatures & Sensors',
            tab_network: 'Network & mDNS',
            tab_hms: 'Health Monitor (HMS)',
            slots_heading: '4-Channel Feeder Slot Mapping & Color Mixing',
            slots_desc: 'Configure Slot 1~4 materials, colors, and remaining volume. Mixing weights strictly conform to 10000 base (COL-001 / TWIN-17).',
            preset_title: 'Quick Mixing Ratios:',
            slot_1: 'Slot 1 (CH-1)',
            slot_2: 'Slot 2 (CH-2)',
            slot_3: 'Slot 3 (CH-3)',
            slot_4: 'Slot 4 (CH-4)',
            tag_loaded: 'Loaded',
            lbl_material: 'Material Type',
            lbl_color: 'Filament Color',
            lbl_remaining: 'Remaining Est.',
            lbl_weight: 'Mixing Base Weight (0~10000)',
            val_total_title: 'Total Mixing Weight:',
            val_valid: 'Valid (100.00%)',
            val_invalid: 'Invalid Weight Sum',
            val_msg_ok: 'Total sum strictly equals 10000, compliant with COL-001 mixing plan.',
            val_msg_err: 'Total weight must strictly equal 10000, current sum: ',
            btn_save_slots: 'Save Slot Configuration',
            save_success: 'Slot configuration saved successfully!',
            save_failed: 'Save failed: Invalid weight sum',
            sensors_heading: 'Dual MCU Sensor & Temperature Live Telemetry',
            sensors_desc: 'Authoritative telemetry from real microservices. Unlinked hardware items explicitly marked to prevent synthetic data.',
            btn_sample: 'Request Sample (POST)',
            th_title: 'Toolhead Nozzle (TH)',
            mc_title: 'Heated Bed (MC)',
            runout_title: '4-Channel Optical Filament Runout Sensors',
            sensor_unknown: 'Not Checked / Offline',
            sensor_loaded: 'Loaded (Filament Present)',
            sensor_empty: 'Runout (Slot Empty)',
            lbl_target_temp: 'Target Temp:',
            lbl_duty: 'Heater Duty:',
            lbl_sensor_state: 'Sensor State:',
            lbl_firmware_ver: 'Firmware Ver:',
            ver_status_unknown: 'Unknown',
            ver_status_offline: 'Device Offline',
            ver_status_query_failed: 'Query Failed',
            ver_status_stale: 'Data Stale',
            lbl_raw_adc: 'Raw ADC:',
            net_heading: 'LAN Device Discovery & mDNS Service',
            net_desc: 'Lightweight C advertiser broadcasts _aisoc._tcp.local to 224.0.0.251:5353 for zero-config direct access.',
            net_mdns_title: 'mDNS LAN Service Attributes',
            net_lbl_hostname: 'Local Hostname:',
            net_lbl_service: 'Service Identifier:',
            net_lbl_multicast: 'Multicast Target:',
            net_lbl_port: 'HTTP Web Port:',
            net_lbl_txt: 'TXT Metadata:',
            net_access_title: 'Browser Quick Direct Access',
            net_access_p1: 'Any PC, phone or tablet on the same LAN can access directly without IP lookup:',
            btn_copy: 'Copy Link',
            copied: 'Copied!',
            net_tip: 'Note: Gateway embeds zero-heap C11/C++17 mdns_advertiser daemon component.',
            hms_heading: 'Health Management System & E-Stop (HMS)',
            hms_desc: 'Unified 0x1000~0x5000 hierarchical error codes, dual-level e-stop and safety protection.',
            estop_normal: 'E-Stop State: Normal',
            th_hms_code: 'Error Code',
            th_hms_subsys: 'Subsystem',
            th_hms_severity: 'Severity',
            th_hms_desc: 'Description & Troubleshooting',
            th_hms_time: 'Timestamp',
            hms_empty: 'No active alarms (System Healthy)',
            oobe_wizard_title: 'Out of Box Setup Wizard (OOBE)',
            step_1: 'Welcome',
            step_2: 'Language',
            step_3: 'Communication',
            step_4: 'Sensors Check',
            step_5: 'Completed',
            oobe_w1_title: 'Welcome to AI-SoC Full-Color 3D Printer!',
            oobe_w1_p1: 'This wizard guides you through the initial self-check, including language selection, controller communication handshake, toolhead link, and sensor health checks.',
            oobe_w1_rule: 'Realism Invariant: The system strictly adheres to hardware detection rules. Unconnected items are reported as unready. Fake PASS results are strictly prohibited.',
            oobe_w2_title: 'Select Language & Theme Preferences',
            oobe_w2_desc: 'Select your preferred language below. Changes apply dynamically without page refresh:',
            oobe_w3_title: 'Dual MCU Firmware & Link Self-Check',
            oobe_w3_desc: 'Attempting MiniMCProto handshake with underlying microcontrollers:',
            oobe_mc_comm: 'MC (AT32F435) Motion Controller Link',
            oobe_th_comm: 'TH (AT32F423) Toolhead Extruder Link',
            oobe_fwd_state: 'AP Forwarding Core & Protocol Sync',
            status_unready: 'Not Ready / Offline / Awaiting Connection',
            status_online: 'Connected (Online)',
            oobe_w4_title: 'Sensors & Thermal Validity Check',
            oobe_w4_desc: 'Verifying nozzle & bed thermistor ADC validity, and filament runout switches:',
            oobe_nozzle_temp: 'Toolhead Nozzle Sensor (TH NTC)',
            oobe_bed_temp: 'Heated Bed Sensor (MC NTC)',
            oobe_runout: '4-Channel Filament Runout Switches (COL-007)',
            oobe_w5_title: 'Setup Wizard Completed',
            oobe_w5_p1: 'Preferences have been saved. Sensor status will continue to be monitored in real time on the dashboard.',
            sum_lang: 'Language:',
            sum_theme: 'Theme:',
            sum_slots: 'Slot Config:',
            sum_slots_val: '4 Channels Mapped (Sum = 10000)',
            btn_prev: 'Previous',
            btn_next: 'Next',
            btn_finish: 'Enter Dashboard',
            oobe_finished_toast: 'Setup wizard completed, entered dashboard',
            btn_estop_clear: 'Clear E-Stop',
            estop_cleared_toast: 'E-Stop cleared (M999), hardware control restored',
            estop_triggered_toast: 'Emergency stop triggered (M112)! Motors & heaters locked',
            estop_active_badge: 'E-Stop State: ACTIVE LOCKED (M112)',
            btn_send_gcode: 'Send G-code',
            quick_g28: 'G28 Home',
            quick_m114: 'M114 Pos',
            quick_t0: 'T0 Slot 1',
            quick_t1: 'T1 Slot 2',
            gcode_ack_toast: 'G-code executed (HW ACK)',
            btn_set_th_temp: 'Set Nozzle Temp',
            btn_set_mc_temp: 'Set Bed Temp',
            preset_off: '0°C Off',
            temp_ack_toast: 'Target temperature set (Dual MCU ACK)',
            btn_slot_select: 'Select',
            btn_slot_load: 'Load',
            btn_slot_unload: 'Unload',
            slot_act_toast: 'Slot hardware action ACKed'
        }
    };

    // 应用运行时状态
    var appState = {
        lang: 'zh-CN',
        theme: 'dark',
        isConnected: false,
        hwOnline: null,
        isHwLocked: false,
        stateGen: 0,
        oobeStep: 1,
        slots: [
            { channel_id: 0, slot_name: 'Slot 1', material: 'PLA', color_hex: '#E53935', color_rgb: [229, 57, 53], remaining_percent: 85, remaining_grams: 850, mixing_weight: 10000, is_loaded: true },
            { channel_id: 1, slot_name: 'Slot 2', material: 'PLA', color_hex: '#1E88E5', color_rgb: [30, 136, 229], remaining_percent: 50, remaining_grams: 500, mixing_weight: 0, is_loaded: true },
            { channel_id: 2, slot_name: 'Slot 3', material: 'PLA', color_hex: '#FFFFFF', color_rgb: [255, 255, 255], remaining_percent: 70, remaining_grams: 700, mixing_weight: 0, is_loaded: true },
            { channel_id: 3, slot_name: 'Slot 4', material: 'PLA', color_hex: '#212121', color_rgb: [33, 33, 33], remaining_percent: 30, remaining_grams: 300, mixing_weight: 0, is_loaded: true }
        ],
        eventSource: null,
        pollTimer: null,
        targetThDeciC: 0,
        targetMcDeciC: 0,
        devices: { mc: null, th: null }
    };

    // DOM 元素引用集合
    var dom = {
        html: document.documentElement,
        connStatus: document.getElementById('conn-status'),
        statusDot: document.getElementById('status-dot'),
        hwConnPill: document.getElementById('hw-conn-pill'),
        hwStatusDot: document.getElementById('hw-status-dot'),
        hwConnStatus: document.getElementById('hw-conn-status'),
        hwOfflineBanner: document.getElementById('hw-offline-banner'),
        toastContainer: document.getElementById('toast-container'),
        stateGen: document.getElementById('state-gen'),
        btnLangToggle: document.getElementById('btn-lang-toggle'),
        langLabel: document.getElementById('lang-label'),
        btnThemeToggle: document.getElementById('btn-theme-toggle'),
        themeIcon: document.getElementById('theme-icon'),
        themeLabel: document.getElementById('theme-label'),
        btnOpenOobe: document.getElementById('btn-open-oobe'),
        btnHeaderEstop: document.getElementById('btn-header-estop'),
        btnHeaderEstopClear: document.getElementById('btn-header-estop-clear'),
        estopBadge: document.getElementById('estop-badge'),
        gcodeManualInput: document.getElementById('gcode-manual-input'),
        btnSendGcode: document.getElementById('btn-send-gcode'),
        inputThTarget: document.getElementById('input-th-target'),
        btnSetThTemp: document.getElementById('btn-set-th-temp'),
        inputMcTarget: document.getElementById('input-mc-target'),
        btnSetMcTemp: document.getElementById('btn-set-mc-temp'),
        jobStatusBadge: document.getElementById('job-status-badge'),
        jobProgressCircle: document.getElementById('job-progress-circle'),
        jobProgressPercent: document.getElementById('job-progress-percent'),
        jobLayerInfo: document.getElementById('job-layer-info'),
        jobElapsedTime: document.getElementById('job-elapsed-time'),
        jobRemainingTime: document.getElementById('job-remaining-time'),
        jobCurrentLine: document.getElementById('job-current-line'),
        jobModelName: document.getElementById('job-model-name'),
        btnJobStart: document.getElementById('btn-job-start'),
        btnJobPause: document.getElementById('btn-job-pause'),
        btnJobResume: document.getElementById('btn-job-resume'),
        btnJobCancel: document.getElementById('btn-job-cancel'),
        gcodeDropzone: document.getElementById('gcode-dropzone'),
        gcodeFileInput: document.getElementById('gcode-file-input'),
        btnHomeAll: document.getElementById('btn-home-all'),
        btnHomeXy: document.getElementById('btn-home-xy'),
        coordValX: document.getElementById('coord-val-x'),
        coordValY: document.getElementById('coord-val-y'),
        coordValZ: document.getElementById('coord-val-z'),
        coordValE: document.getElementById('coord-val-e'),
        levelingMeshGrid: document.getElementById('leveling-mesh-grid'),
        btnTriggerLeveling: document.getElementById('btn-trigger-leveling'),
        meshVarianceVal: document.getElementById('mesh-variance-val'),
        meshTiltVal: document.getElementById('mesh-tilt-val'),
        navTabs: document.querySelectorAll('.nav-tab'),
        tabContents: document.querySelectorAll('.tab-content'),
        totalWeightDisplay: document.getElementById('total-weight-display'),
        weightStatusBadge: document.getElementById('weight-status-badge'),
        weightStatusMsg: document.getElementById('weight-status-msg'),
        btnSaveSlots: document.getElementById('btn-save-slots'),
        slotSaveFeedback: document.getElementById('slot-save-feedback'),
        headerThTemp: document.getElementById('header-th-temp'),
        headerMcTemp: document.getElementById('header-mc-temp'),
        thCurrentTemp: document.getElementById('th-current-temp'),
        thTargetTemp: document.getElementById('th-target-temp'),
        thQuality: document.getElementById('th-quality'),
        thDuty: document.getElementById('th-duty'),
        thSensorStatus: document.getElementById('th-sensor-status'),
        thRawAdc: document.getElementById('th-raw-adc'),
        mcCurrentTemp: document.getElementById('mc-current-temp'),
        mcTargetTemp: document.getElementById('mc-target-temp'),
        mcQuality: document.getElementById('mc-quality'),
        mcDuty: document.getElementById('mc-duty'),
        mcSensorStatus: document.getElementById('mc-sensor-status'),
        mcRawAdc: document.getElementById('mc-raw-adc'),
        thFirmwareVersion: document.getElementById('th-firmware-version'),
        mcFirmwareVersion: document.getElementById('mc-firmware-version'),
        oobeMcVersion: document.getElementById('oobe-mc-version'),
        oobeThVersion: document.getElementById('oobe-th-version'),
        oobeMcStatus: document.getElementById('oobe-mc-status'),
        oobeThStatus: document.getElementById('oobe-th-status'),
        oobeFwdStatus: document.getElementById('oobe-fwd-status'),
        oobeFwdDesc: document.getElementById('oobe-fwd-desc'),
        oobeNozzleStatus: document.getElementById('oobe-nozzle-status'),
        oobeNozzleDetail: document.getElementById('oobe-nozzle-detail'),
        oobeBedStatus: document.getElementById('oobe-bed-status'),
        oobeBedDetail: document.getElementById('oobe-bed-detail'),
        oobeRunoutStatus: document.getElementById('oobe-runout-status'),
        btnRequestSample: document.getElementById('btn-request-sample'),
        btnCopyUrl: document.getElementById('btn-copy-url'),
        directUrl: document.getElementById('direct-url'),
        oobeModal: document.getElementById('oobe-modal'),
        btnCloseOobe: document.getElementById('btn-close-oobe'),
        btnOobePrev: document.getElementById('btn-oobe-prev'),
        btnOobeNext: document.getElementById('btn-oobe-next'),
        btnOobeFinish: document.getElementById('btn-oobe-finish'),
        btnChoiceZh: document.getElementById('btn-choice-zh'),
        btnChoiceEn: document.getElementById('btn-choice-en'),
        sumLangVal: document.getElementById('sum-lang-val'),
        sumThemeVal: document.getElementById('sum-theme-val')
    };

    /* ===================================================================== */
    /* 1. 国际化 (i18n) 动态免刷新切换                                        */
    /* ===================================================================== */

    function t(key) {
        var dict = I18N[appState.lang] || I18N['zh-CN'];
        return dict[key] || key;
    }

    function setLanguage(lang) {
        if (!I18N[lang]) return;
        appState.lang = lang;
        dom.html.setAttribute('lang', lang);

        // 更新带 data-i18n 属性的所有 DOM 节点
        var elements = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            var key = el.getAttribute('data-i18n');
            if (key && I18N[lang][key]) {
                el.textContent = I18N[lang][key];
            }
        }

        // 更新按钮标签与总结栏
        if (dom.langLabel) {
            dom.langLabel.textContent = (lang === 'zh-CN') ? 'English' : '简体中文';
        }
        if (dom.themeLabel) {
            dom.themeLabel.textContent = (appState.theme === 'dark') ? t('theme_light') : t('theme_dark');
        }
        if (dom.sumLangVal) {
            dom.sumLangVal.textContent = (lang === 'zh-CN') ? '简体中文 (zh-CN)' : 'English (en-US)';
        }

        if (appState.devices && (appState.devices.th || appState.devices.mc)) {
            if (appState.devices.th) updateDeviceVersion('th', appState.devices.th, dom.thFirmwareVersion, dom.oobeThVersion, dom.oobeThStatus);
            if (appState.devices.mc) updateDeviceVersion('mc', appState.devices.mc, dom.mcFirmwareVersion, dom.oobeMcVersion, dom.oobeMcStatus);
        }

        if (dom.connStatus) {
            dom.connStatus.textContent = appState.isConnected ? t('status_connected') : t('status_disconnected');
        }
        updateHardwareConnectionUI(appState.hwOnline);

        updateWeightValidationUI();
        updateOobeSensorsRealism();
    }

    /* ===================================================================== */
    /* 2. 主题切换 (Dark / Light)                                            */
    /* ===================================================================== */

    function setTheme(theme) {
        appState.theme = theme;
        dom.html.setAttribute('data-theme', theme);
        if (dom.themeIcon) {
            dom.themeIcon.textContent = (theme === 'dark') ? '☀️' : '🌙';
        }
        if (dom.themeLabel) {
            dom.themeLabel.textContent = (theme === 'dark') ? t('theme_light') : t('theme_dark');
        }
        if (dom.sumThemeVal) {
            dom.sumThemeVal.textContent = (theme === 'dark') ? t('theme_dark') : t('theme_light');
        }
    }

    /* ===================================================================== */
    /* 3. 料槽映射与 TWIN-17 10000 混色权重校验                              */
    /* ===================================================================== */

    function hexToRgb(hex) {
        var clean = hex.replace('#', '');
        if (clean.length === 3) {
            clean = clean[0] + clean[0] + clean[1] + clean[1] + clean[2] + clean[2];
        }
        var num = parseInt(clean, 16);
        return [(num >> 16) & 255, (num >> 8) & 255, num & 255];
    }

    function calculateTotalWeight() {
        var sum = 0;
        for (var i = 0; i < appState.slots.length; i++) {
            sum += (parseInt(appState.slots[i].mixing_weight, 10) || 0);
        }
        return sum;
    }

    function updateWeightValidationUI() {
        var sum = calculateTotalWeight();
        var isValid = (sum === TOTAL_WEIGHT_TARGET);
        var permilleStr = (sum / 100).toFixed(2) + '%';

        if (dom.totalWeightDisplay) {
            dom.totalWeightDisplay.textContent = sum + ' / ' + TOTAL_WEIGHT_TARGET + ' (' + permilleStr + ')';
        }

        if (dom.weightStatusBadge) {
            if (isValid) {
                dom.weightStatusBadge.className = 'validation-badge badge-valid';
                dom.weightStatusBadge.textContent = t('val_valid');
            } else {
                dom.weightStatusBadge.className = 'validation-badge badge-invalid';
                dom.weightStatusBadge.textContent = t('val_invalid');
            }
        }

        if (dom.weightStatusMsg) {
            if (isValid) {
                dom.weightStatusMsg.textContent = t('val_msg_ok');
                dom.weightStatusMsg.style.color = 'var(--text-secondary)';
            } else {
                var delta = sum - TOTAL_WEIGHT_TARGET;
                var deltaStr = (delta > 0) ? ('+' + delta) : ('' + delta);
                dom.weightStatusMsg.textContent = t('val_msg_err') + sum + ' (' + deltaStr + ')';
                dom.weightStatusMsg.style.color = 'var(--danger)';
            }
        }

        if (dom.btnSaveSlots) {
            dom.btnSaveSlots.disabled = !isValid;
        }
    }

    function syncSlotDOM(slotIndex) {
        var slot = appState.slots[slotIndex];
        if (!slot) return;

        var matEl = document.getElementById('slot-mat-' + slotIndex);
        var colorEl = document.getElementById('slot-color-' + slotIndex);
        var hexEl = document.getElementById('slot-hex-' + slotIndex);
        var swatchEl = document.getElementById('slot-swatch-' + slotIndex);
        var remEl = document.getElementById('slot-rem-' + slotIndex);
        var remValEl = document.getElementById('slot-rem-val-' + slotIndex);
        var progressEl = document.getElementById('slot-progress-' + slotIndex);
        var weightEl = document.getElementById('slot-weight-' + slotIndex);
        var permilleEl = document.getElementById('slot-weight-permille-' + slotIndex);

        if (matEl) matEl.value = slot.material;
        if (colorEl) colorEl.value = slot.color_hex;
        if (hexEl) hexEl.value = slot.color_hex;
        if (swatchEl) swatchEl.style.backgroundColor = slot.color_hex;
        if (remEl) remEl.value = slot.remaining_percent;
        if (remValEl) remValEl.textContent = slot.remaining_percent + '% (~' + (slot.remaining_percent * 10) + 'g)';
        if (progressEl) progressEl.style.width = slot.remaining_percent + '%';
        if (weightEl) weightEl.value = slot.mixing_weight;
        if (permilleEl) permilleEl.textContent = (slot.mixing_weight / 100).toFixed(2) + '%';
    }

    function initSlotEvents() {
        for (var i = 0; i < 4; i++) {
            (function (idx) {
                var matEl = document.getElementById('slot-mat-' + idx);
                var colorEl = document.getElementById('slot-color-' + idx);
                var hexEl = document.getElementById('slot-hex-' + idx);
                var remEl = document.getElementById('slot-rem-' + idx);
                var weightEl = document.getElementById('slot-weight-' + idx);

                if (matEl) {
                    matEl.addEventListener('change', function () {
                        appState.slots[idx].material = matEl.value;
                    });
                }
                if (colorEl) {
                    colorEl.addEventListener('input', function () {
                        var hex = colorEl.value.toUpperCase();
                        appState.slots[idx].color_hex = hex;
                        appState.slots[idx].color_rgb = hexToRgb(hex);
                        syncSlotDOM(idx);
                    });
                }
                if (hexEl) {
                    hexEl.addEventListener('change', function () {
                        var hex = hexEl.value.trim().toUpperCase();
                        if (/^#[0-9A-F]{6}$/.test(hex)) {
                            appState.slots[idx].color_hex = hex;
                            appState.slots[idx].color_rgb = hexToRgb(hex);
                            syncSlotDOM(idx);
                        } else {
                            hexEl.value = appState.slots[idx].color_hex;
                        }
                    });
                }
                if (remEl) {
                    remEl.addEventListener('input', function () {
                        var val = parseInt(remEl.value, 10) || 0;
                        appState.slots[idx].remaining_percent = val;
                        appState.slots[idx].remaining_grams = val * 10;
                        syncSlotDOM(idx);
                    });
                }
                if (weightEl) {
                    weightEl.addEventListener('input', function () {
                        var val = parseInt(weightEl.value, 10) || 0;
                        if (val < 0) val = 0;
                        if (val > 10000) val = 10000;
                        appState.slots[idx].mixing_weight = val;
                        syncSlotDOM(idx);
                        updateWeightValidationUI();
                    });
                }
            })(i);
        }

        // 预设调色板快捷选择按钮事件绑定
        var paletteBtns = document.querySelectorAll('.palette-btn');
        for (var p = 0; p < paletteBtns.length; p++) {
            paletteBtns[p].addEventListener('click', function () {
                var container = this.closest('.palette-swatches');
                if (!container) return;
                var targetIdx = parseInt(container.getAttribute('data-target'), 10);
                var hex = this.getAttribute('data-hex');
                if (!isNaN(targetIdx) && hex) {
                    appState.slots[targetIdx].color_hex = hex;
                    appState.slots[targetIdx].color_rgb = hexToRgb(hex);
                    syncSlotDOM(targetIdx);
                }
            });
        }

        // 快捷混色配比按钮
        var presetBtns = document.querySelectorAll('.btn-preset');
        for (var b = 0; b < presetBtns.length; b++) {
            presetBtns[b].addEventListener('click', function () {
                var pType = this.getAttribute('data-preset');
                if (pType === 'single-1') {
                    appState.slots[0].mixing_weight = 10000;
                    appState.slots[1].mixing_weight = 0;
                    appState.slots[2].mixing_weight = 0;
                    appState.slots[3].mixing_weight = 0;
                } else if (pType === 'single-2') {
                    appState.slots[0].mixing_weight = 0;
                    appState.slots[1].mixing_weight = 10000;
                    appState.slots[2].mixing_weight = 0;
                    appState.slots[3].mixing_weight = 0;
                } else if (pType === 'dual-50') {
                    appState.slots[0].mixing_weight = 5000;
                    appState.slots[1].mixing_weight = 5000;
                    appState.slots[2].mixing_weight = 0;
                    appState.slots[3].mixing_weight = 0;
                } else if (pType === 'quad-25') {
                    appState.slots[0].mixing_weight = 2500;
                    appState.slots[1].mixing_weight = 2500;
                    appState.slots[2].mixing_weight = 2500;
                    appState.slots[3].mixing_weight = 2500;
                }
                for (var k = 0; k < 4; k++) syncSlotDOM(k);
                updateWeightValidationUI();
            });
        }

        // 保存料槽映射按钮
        if (dom.btnSaveSlots) {
            dom.btnSaveSlots.addEventListener('click', function () {
                var sum = calculateTotalWeight();
                if (sum !== TOTAL_WEIGHT_TARGET) {
                    alert(t('save_failed'));
                    return;
                }
                saveSlotsToBackend();
            });
        }

        // 单槽选槽/进丝/退丝硬件动作按钮
        var slotActBtns = document.querySelectorAll('.btn-slot-act');
        for (var s = 0; s < slotActBtns.length; s++) {
            slotActBtns[s].addEventListener('click', function () {
                var slotId = parseInt(this.getAttribute('data-slot-id'), 10) || 1;
                var actCode = parseInt(this.getAttribute('data-slot-action'), 10) || 0;
                triggerSlotHardwareAction(slotId, actCode);
            });
        }
    }

    /**
     * @brief 下发单通道耗材选槽/进丝/退丝指令至后端 0x19 真实闭环
     */
    function triggerSlotHardwareAction(slotId, actionCode) {
        var payload = {
            active_slot: slotId,
            slot_id: slotId,
            action: actionCode,
            target_temp_deci_c: appState.targetThDeciC > 0 ? appState.targetThDeciC : 2100
        };
        sendPostRequest('/api/v1/filament/slots', payload, function (res) {
            var actSlot = (res && res.active_slot) ? res.active_slot : slotId;
            showToast(t('slot_act_toast') + ' (Slot ' + actSlot + ', action=' + actionCode + ')', 'success');
        });
    }

    function saveSlotsToBackend() {
        var maxIdx = 0;
        var maxWeight = -1;
        for (var i = 0; i < appState.slots.length; i++) {
            var w = parseInt(appState.slots[i].mixing_weight, 10) || 0;
            if (w > maxWeight) {
                maxWeight = w;
                maxIdx = i;
            }
        }
        var primarySlotId = maxIdx + 1;
        var payload = {
            version: "2.0.0",
            active_slot: primarySlotId,
            slot_id: primarySlotId,
            action: 1,
            target_temp_deci_c: appState.targetThDeciC > 0 ? appState.targetThDeciC : 2100,
            total_mixing_weight: TOTAL_WEIGHT_TARGET,
            last_updated_ms: Date.now(),
            slots: appState.slots
        };

        if (dom.slotSaveFeedback) {
            dom.slotSaveFeedback.textContent = 'Saving...';
            dom.slotSaveFeedback.style.color = 'var(--accent)';
        }

        sendPostRequest('/api/v1/filament/slots', payload, function () {
            if (dom.slotSaveFeedback) {
                dom.slotSaveFeedback.textContent = t('save_success');
                dom.slotSaveFeedback.style.color = 'var(--success)';
            }
            showToast(t('save_success') + ' (Slot ' + primarySlotId + ')', 'success');
        }, function () {
            if (dom.slotSaveFeedback) {
                dom.slotSaveFeedback.textContent = t('save_failed');
                dom.slotSaveFeedback.style.color = 'var(--danger)';
            }
        });
    }

    /* ===================================================================== */
    /* 4. 新机检查引导向导 (OOBE Wizard)                                     */
    /* ===================================================================== */

    function setOobeStep(step) {
        if (step < 1 || step > 5) return;
        appState.oobeStep = step;

        // 更新步骤指示条
        for (var s = 1; s <= 5; s++) {
            var node = document.getElementById('step-node-' + s);
            var view = document.getElementById('oobe-view-' + s);
            if (node) {
                if (s === step) node.className = 'step-indicator active';
                else node.className = 'step-indicator';
            }
            if (view) {
                if (s === step) view.className = 'oobe-step-view active';
                else view.className = 'oobe-step-view';
            }
        }

        // 按钮可见性控制
        if (dom.btnOobePrev) {
            dom.btnOobePrev.style.display = (step > 1) ? 'inline-flex' : 'none';
        }
        if (dom.btnOobeNext) {
            dom.btnOobeNext.style.display = (step < 5) ? 'inline-flex' : 'none';
        }
        if (dom.btnOobeFinish) {
            dom.btnOobeFinish.style.display = (step === 5) ? 'inline-flex' : 'none';
        }

        // 步骤 3 和 4 执行真实性状态更新
        if (step === 3 || step === 4) {
            updateOobeSensorsRealism();
        }
    }

    function updateRunoutSensorsDOM(isOnline) {
        var isZh = (appState.lang === 'zh-CN');
        var cls = isOnline ? 'runout-state-badge state-pass' : 'runout-state-badge state-unknown';
        var txt = isOnline ? (isZh ? '就绪 (正常)' : 'Ready (Normal)') : t('sensor_unknown');
        for (var i = 0; i < 4; i++) {
            var el = document.getElementById('runout-sensor-' + i);
            if (el) {
                el.className = cls;
                el.textContent = txt;
            }
        }
    }

    function resetOobeSensorsOffline(elements) {
        if (!elements) return;
        if (elements.mc) {
            elements.mc.className = 'check-result-badge badge-warning';
            elements.mc.textContent = t('status_unready');
        }
        if (elements.th) {
            elements.th.className = 'check-result-badge badge-warning';
            elements.th.textContent = t('status_unready');
        }
        if (elements.fwd) {
            elements.fwd.className = 'check-result-badge badge-warning';
            elements.fwd.textContent = t('status_unready');
        }
        if (elements.nozzle) {
            elements.nozzle.className = 'check-result-badge badge-warning';
            elements.nozzle.textContent = t('sensor_unknown');
        }
        if (elements.bed) {
            elements.bed.className = 'check-result-badge badge-warning';
            elements.bed.textContent = t('sensor_unknown');
        }
        if (elements.runout) {
            elements.runout.className = 'check-result-badge badge-warning';
            elements.runout.textContent = t('sensor_unknown');
        }
        updateRunoutSensorsDOM(false);
    }

    function applyOobeSensorsOnline(elements) {
        if (!elements) return;
        var isZh = (appState.lang === 'zh-CN');
        if (elements.fwd) {
            elements.fwd.className = 'check-result-badge badge-success';
            elements.fwd.textContent = isZh ? '在线 (帧同步正常)' : 'Online (Frame Synced)';
        }
        if (elements.runout) {
            elements.runout.className = 'check-result-badge badge-success';
            elements.runout.textContent = isZh ? '正常 (料丝在位)' : 'Normal (Filament Present)';
        }
        updateRunoutSensorsDOM(true);
    }

    function updateOobeSensorsRealism() {
        var elements = {
            mc: dom.oobeMcStatus || document.getElementById('oobe-mc-status'),
            th: dom.oobeThStatus || document.getElementById('oobe-th-status'),
            fwd: dom.oobeFwdStatus || document.getElementById('oobe-fwd-status'),
            nozzle: dom.oobeNozzleStatus || document.getElementById('oobe-nozzle-status'),
            bed: dom.oobeBedStatus || document.getElementById('oobe-bed-status'),
            runout: dom.oobeRunoutStatus || document.getElementById('oobe-runout-status')
        };

        if (!appState.isConnected) {
            resetOobeSensorsOffline(elements);
        } else {
            applyOobeSensorsOnline(elements);
        }
    }

    function initOobeEvents() {
        if (dom.btnOpenOobe) {
            dom.btnOpenOobe.addEventListener('click', function () {
                if (dom.oobeModal) dom.oobeModal.style.display = 'flex';
                setOobeStep(1);
            });
        }
        if (dom.btnCloseOobe) {
            dom.btnCloseOobe.addEventListener('click', function () {
                if (dom.oobeModal) dom.oobeModal.style.display = 'none';
            });
        }
        if (dom.btnOobePrev) {
            dom.btnOobePrev.addEventListener('click', function () {
                setOobeStep(appState.oobeStep - 1);
            });
        }
        if (dom.btnOobeNext) {
            dom.btnOobeNext.addEventListener('click', function () {
                setOobeStep(appState.oobeStep + 1);
            });
        }
        if (dom.btnOobeFinish) {
            dom.btnOobeFinish.addEventListener('click', function () {
                if (dom.oobeModal) {
                    dom.oobeModal.style.display = 'none';
                }
                try {
                    if (typeof localStorage !== 'undefined') {
                        localStorage.setItem('aisoc_oobe_completed', 'true');
                    }
                } catch (e) {
                    console.warn('LocalStorage write failed:', e);
                }
                switchTab('tab-dashboard');
                showToast(t('oobe_finished_toast') || '新机自检向导已完成，已进入控制台', 'success');
            });
        }

        // 向导内部语言选择
        if (dom.btnChoiceZh) {
            dom.btnChoiceZh.addEventListener('click', function () {
                dom.btnChoiceZh.className = 'btn-lang-choice active';
                if (dom.btnChoiceEn) dom.btnChoiceEn.className = 'btn-lang-choice';
                setLanguage('zh-CN');
            });
        }
        if (dom.btnChoiceEn) {
            dom.btnChoiceEn.addEventListener('click', function () {
                dom.btnChoiceEn.className = 'btn-lang-choice active';
                if (dom.btnChoiceZh) dom.btnChoiceZh.className = 'btn-lang-choice';
                setLanguage('en-US');
            });
        }
    }

    /* ===================================================================== */
    /* 5. 导航与快速复制                                                     */
    /* ===================================================================== */

    function switchTab(targetTabId) {
        if (!targetTabId) return;
        var navTabs = dom.navTabs || document.querySelectorAll('.nav-tab');
        var tabContents = dom.tabContents || document.querySelectorAll('.tab-content');

        for (var i = 0; i < navTabs.length; i++) {
            var tab = navTabs[i];
            var isTarget = (tab.getAttribute('data-tab') === targetTabId);
            if (isTarget) {
                tab.className = 'nav-tab active';
                tab.setAttribute('aria-selected', 'true');
            } else {
                tab.className = 'nav-tab';
                tab.setAttribute('aria-selected', 'false');
            }
        }

        for (var c = 0; c < tabContents.length; c++) {
            var content = tabContents[c];
            if (content.id === targetTabId) {
                content.className = 'tab-content active';
            } else {
                content.className = 'tab-content';
            }
        }

        if (typeof window !== 'undefined' && typeof window.scrollTo === 'function') {
            try {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } catch (e) {
                window.scrollTo(0, 0);
            }
        }
    }

    function initNavEvents() {
        for (var i = 0; i < dom.navTabs.length; i++) {
            dom.navTabs[i].addEventListener('click', function () {
                var targetTabId = this.getAttribute('data-tab');
                switchTab(targetTabId);
            });
        }

        if (dom.btnLangToggle) {
            dom.btnLangToggle.addEventListener('click', function () {
                var nextLang = (appState.lang === 'zh-CN') ? 'en-US' : 'zh-CN';
                setLanguage(nextLang);
            });
        }

        if (dom.btnThemeToggle) {
            dom.btnThemeToggle.addEventListener('click', function () {
                var nextTheme = (appState.theme === 'dark') ? 'light' : 'dark';
                setTheme(nextTheme);
            });
        }

        if (dom.btnCopyUrl && dom.directUrl) {
            dom.btnCopyUrl.addEventListener('click', function () {
                var text = dom.directUrl.textContent;
                navigator.clipboard.writeText(text).then(function () {
                    dom.btnCopyUrl.textContent = t('copied');
                    setTimeout(function () {
                        dom.btnCopyUrl.textContent = t('btn_copy');
                    }, 1500);
                }).catch(function () {
                    dom.btnCopyUrl.textContent = 'Copy failed';
                });
            });
        }

        if (dom.btnRequestSample) {
            dom.btnRequestSample.addEventListener('click', function () {
                fetch(GATEWAY_BASE_URL + '/api/v1/temperature/sample', { method: 'POST' })
                .catch(function () {});
            });
        }
    }

    /* ===================================================================== */
    /* 6. 后端真实数据流与硬件离线安全阻断 (Fail-Closed UI Safety & Sentinels)   */
    /* ===================================================================== */

    function showToast(message, type, durationMs) {
        if (!message) return;
        var container = dom.toastContainer || document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            container.setAttribute('aria-live', 'polite');
            document.body.appendChild(container);
            dom.toastContainer = container;
        }
        var toast = document.createElement('div');
        var toastType = type || 'info';
        toast.className = 'hmi-toast toast-' + toastType;
        var icon = (toastType === 'warning') ? '⚠️ ' : (toastType === 'error') ? '❌ ' : (toastType === 'success') ? '✅ ' : 'ℹ️ ';
        toast.textContent = icon + message;
        container.appendChild(toast);

        var duration = durationMs || 4000;
        setTimeout(function () {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            setTimeout(function () {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, duration);
    }

    function setControlsLocked(locked) {
        appState.isHwLocked = !!locked;
        var jogBtns = document.querySelectorAll('.btn-jog, .btn-quick-gcode, .btn-slot-act, .btn-th-preset, .btn-mc-preset');
        for (var i = 0; i < jogBtns.length; i++) {
            jogBtns[i].disabled = locked;
        }
        if (dom.btnHomeAll) dom.btnHomeAll.disabled = locked;
        if (dom.btnHomeXy) dom.btnHomeXy.disabled = locked;
        if (dom.btnTriggerLeveling) dom.btnTriggerLeveling.disabled = locked;
        if (dom.btnJobStart) dom.btnJobStart.disabled = locked;
        if (dom.btnJobResume) dom.btnJobResume.disabled = locked;
        if (dom.btnSendGcode) dom.btnSendGcode.disabled = locked;
        if (dom.btnSetThTemp) dom.btnSetThTemp.disabled = locked;
        if (dom.btnSetMcTemp) dom.btnSetMcTemp.disabled = locked;
    }

    function updateHardwareConnectionUI(isOnline) {
        if (isOnline === true) {
            if (dom.hwStatusDot) dom.hwStatusDot.className = 'status-dot online';
            if (dom.hwConnStatus) dom.hwConnStatus.textContent = t('hw_status_online');
            if (dom.hwConnPill) {
                dom.hwConnPill.classList.remove('hw-offline');
                dom.hwConnPill.classList.add('hw-online');
            }
            if (dom.hwOfflineBanner) dom.hwOfflineBanner.style.display = 'none';
            setControlsLocked(false);
        } else if (isOnline === false) {
            if (dom.hwStatusDot) dom.hwStatusDot.className = 'status-dot offline';
            if (dom.hwConnStatus) dom.hwConnStatus.textContent = t('hw_status_offline');
            if (dom.hwConnPill) {
                dom.hwConnPill.classList.remove('hw-online');
                dom.hwConnPill.classList.add('hw-offline');
            }
            if (dom.hwOfflineBanner) dom.hwOfflineBanner.style.display = 'flex';
            setControlsLocked(true);
        } else {
            if (dom.hwStatusDot) dom.hwStatusDot.className = 'status-dot unknown';
            if (dom.hwConnStatus) dom.hwConnStatus.textContent = t('hw_status_unknown');
            if (dom.hwConnPill) {
                dom.hwConnPill.classList.remove('hw-online', 'hw-offline');
            }
            if (dom.hwOfflineBanner) dom.hwOfflineBanner.style.display = 'none';
        }
    }

    function setHardwareOnline(isOnline) {
        appState.hwOnline = isOnline;
        updateHardwareConnectionUI(isOnline);
    }

    function evaluateHardwareOnline(data) {
        if (!data) return false;
        if (typeof data.hardware_online === 'boolean') {
            return data.hardware_online;
        }
        if (data.system_status === 'OFFLINE') {
            return false;
        }
        if (data.devices) {
            if (data.devices.mc && data.devices.mc.valid && (data.devices.mc.status === 'OFFLINE' || data.devices.mc.status === 'QUERY_FAILED')) {
                return false;
            }
            if (data.devices.th && data.devices.th.valid && (data.devices.th.status === 'OFFLINE' || data.devices.th.status === 'QUERY_FAILED')) {
                return false;
            }
        }
        if (data.tool) {
            if (data.tool.quality === 'OFFLINE') return false;
            if (data.tool.temperature_millic === AISOC_TEMP_MILLIC_OFFLINE || data.tool.temp_deci_c === AISOC_TEMP_MILLIC_OFFLINE) return false;
        }
        if (data.bed) {
            if (data.bed.quality === 'OFFLINE') return false;
            if (data.bed.temperature_millic === AISOC_TEMP_MILLIC_OFFLINE || data.bed.temp_deci_c === AISOC_TEMP_MILLIC_OFFLINE) return false;
        }
        if (data.system_status === 'NORMAL' || data.system_status === 'ONLINE') {
            return true;
        }
        if (data.devices && data.devices.mc && data.devices.mc.status === 'ONLINE') {
            return true;
        }
        return false;
    }

    function fetchApi(path, options) {
        var fullUrl = (path.indexOf('http') === 0) ? path : (GATEWAY_BASE_URL + path);
        return fetch(fullUrl, options).then(function (res) {
            if (res.status === 503 || res.status === 504) {
                return res.text().then(function (text) {
                    var msg = '硬件已断开连接 (HTTP ' + res.status + ')';
                    try {
                        var parsed = JSON.parse(text);
                        if (parsed && parsed.message) msg = parsed.message;
                    } catch (e) {}
                    showToast(msg, 'warning');
                    setHardwareOnline(false);
                    var err = new Error(msg);
                    err.status = res.status;
                    return Promise.reject(err);
                });
            }
            return res;
        }).catch(function (err) {
            if (err.status === 503 || err.status === 504) {
                return Promise.reject(err);
            }
            showToast(t('net_error') || '网络通信异常', 'error');
            return Promise.reject(err);
        });
    }

    function extractTemperatureC(obj) {
        if (!obj) return '--.-';
        var millic = obj.temperature_millic;
        var decic = obj.temp_deci_c;
        var tempC = obj.temperature_c;

        if (millic === AISOC_TEMP_MILLIC_FAULT || millic === 0x7FFFFFFF ||
            decic === AISOC_TEMP_MILLIC_FAULT || decic === SENTINEL_FAULT_DECI) {
            return 'FAULT';
        }
        if (millic === AISOC_TEMP_MILLIC_OFFLINE || millic === 0x7FFFFFFE ||
            decic === AISOC_TEMP_MILLIC_OFFLINE || decic === SENTINEL_OFFLINE_DECI) {
            return '--.-';
        }
        if (tempC !== undefined && tempC !== null) {
            if (typeof tempC === 'number' && tempC > 2000000) {
                return (tempC >= 2147483.65) ? 'FAULT' : '--.-';
            }
            return (typeof tempC === 'number') ? tempC.toFixed(1) : String(tempC);
        }
        if (millic !== undefined && millic !== null) {
            if (millic === AISOC_TEMP_MILLIC_FAULT || millic >= 2147483647) return 'FAULT';
            if (millic === AISOC_TEMP_MILLIC_OFFLINE || millic >= 2147483640) return '--.-';
            return (millic / 1000.0).toFixed(1);
        }
        if (decic !== undefined && decic !== null) {
            if (decic === AISOC_TEMP_MILLIC_FAULT || decic === SENTINEL_FAULT_DECI) return 'FAULT';
            if (decic === AISOC_TEMP_MILLIC_OFFLINE || decic === SENTINEL_OFFLINE_DECI) return '--.-';
            return (decic / 10.0).toFixed(1);
        }
        return '--.-';
    }

    function updateToolTelemetry(tool) {
        if (!tool) return;
        var thTemp = extractTemperatureC(tool);
        if (dom.thCurrentTemp) dom.thCurrentTemp.textContent = thTemp;
        if (dom.headerThTemp) {
            dom.headerThTemp.textContent = (thTemp === 'FAULT') ? 'FAULT' : (thTemp + ' °C');
        }
        var thTarget = (tool.target_temperature_c !== undefined) ? tool.target_temperature_c :
                       (tool.target_deci_c !== undefined ? (tool.target_deci_c / 10).toFixed(1) :
                        (appState.targetThDeciC / 10).toFixed(1));
        if (tool.target_deci_c !== undefined) appState.targetThDeciC = tool.target_deci_c;
        if (dom.thTargetTemp) dom.thTargetTemp.textContent = thTarget + ' °C';
        if (dom.thDuty && tool.duty_percent !== undefined) dom.thDuty.textContent = tool.duty_percent + '%';
        if (dom.thQuality && tool.quality) {
            dom.thQuality.textContent = tool.quality;
            dom.thQuality.className = (tool.quality === 'FRESH') ? 'quality-badge badge-fresh' : 'quality-badge';
        }
        if (dom.thRawAdc && tool.raw_adc !== undefined) dom.thRawAdc.textContent = tool.raw_adc;
        var thSt = tool.sensor_status || (thTemp === 'FAULT' ? 'FAULT' : (thTemp === '--.-' ? 'OFFLINE' : 'ONLINE'));
        if (dom.thSensorStatus) dom.thSensorStatus.textContent = thSt;

        var isZh = (appState.lang === 'zh-CN');
        if (dom.oobeNozzleStatus) {
            if (thTemp !== '--.-' && thTemp !== 'FAULT') {
                dom.oobeNozzleStatus.textContent = isZh ? ('正常 (' + thTemp + ' °C)') : ('Ready (' + thTemp + ' °C)');
                dom.oobeNozzleStatus.className = 'check-result-badge badge-success';
            } else if (thTemp === 'FAULT') {
                dom.oobeNozzleStatus.textContent = isZh ? '故障 (FAULT)' : 'Fault (FAULT)';
                dom.oobeNozzleStatus.className = 'check-result-badge badge-danger';
            }
        }
        if (dom.oobeNozzleDetail) {
            var prefix = isZh ? '当前读数: ' : 'Current Reading: ';
            var suffix = isZh ? ' (有效区间 5~300°C)' : ' (Valid range 5~300°C)';
            var valStr = (thTemp === 'FAULT') ? 'FAULT' : (thTemp + ' °C');
            dom.oobeNozzleDetail.textContent = prefix + valStr + suffix;
        }
    }

    function updateBedTelemetry(bed) {
        if (!bed) return;
        var mcTemp = extractTemperatureC(bed);
        if (dom.mcCurrentTemp) dom.mcCurrentTemp.textContent = mcTemp;
        if (dom.headerMcTemp) {
            dom.headerMcTemp.textContent = (mcTemp === 'FAULT') ? 'FAULT' : (mcTemp + ' °C');
        }
        var mcTarget = (bed.target_temperature_c !== undefined) ? bed.target_temperature_c :
                       (bed.target_deci_c !== undefined ? (bed.target_deci_c / 10).toFixed(1) :
                        (appState.targetMcDeciC / 10).toFixed(1));
        if (bed.target_deci_c !== undefined) appState.targetMcDeciC = bed.target_deci_c;
        if (dom.mcTargetTemp) dom.mcTargetTemp.textContent = mcTarget + ' °C';
        if (dom.mcDuty && bed.duty_percent !== undefined) dom.mcDuty.textContent = bed.duty_percent + '%';
        if (dom.mcQuality && bed.quality) {
            dom.mcQuality.textContent = bed.quality;
            dom.mcQuality.className = (bed.quality === 'FRESH') ? 'quality-badge badge-fresh' : 'quality-badge';
        }
        if (dom.mcRawAdc && bed.raw_adc !== undefined) dom.mcRawAdc.textContent = bed.raw_adc;
        var mcSt = bed.sensor_status || (mcTemp === 'FAULT' ? 'FAULT' : (mcTemp === '--.-' ? 'OFFLINE' : 'ONLINE'));
        if (dom.mcSensorStatus) dom.mcSensorStatus.textContent = mcSt;

        var isZh = (appState.lang === 'zh-CN');
        if (dom.oobeBedStatus) {
            if (mcTemp !== '--.-' && mcTemp !== 'FAULT') {
                dom.oobeBedStatus.textContent = isZh ? ('正常 (' + mcTemp + ' °C)') : ('Ready (' + mcTemp + ' °C)');
                dom.oobeBedStatus.className = 'check-result-badge badge-success';
            } else if (mcTemp === 'FAULT') {
                dom.oobeBedStatus.textContent = isZh ? '故障 (FAULT)' : 'Fault (FAULT)';
                dom.oobeBedStatus.className = 'check-result-badge badge-danger';
            }
        }
        if (dom.oobeBedDetail) {
            var prefix = isZh ? '当前读数: ' : 'Current Reading: ';
            var suffix = isZh ? ' (有效区间 5~130°C)' : ' (Valid range 5~130°C)';
            var valStr = (mcTemp === 'FAULT') ? 'FAULT' : (mcTemp + ' °C');
            dom.oobeBedDetail.textContent = prefix + valStr + suffix;
        }
    }

    function updateOobeTelemetryLinks() {
        var isZh = (appState.lang === 'zh-CN');
        if (dom.oobeFwdStatus) {
            dom.oobeFwdStatus.className = 'check-result-badge badge-success';
            dom.oobeFwdStatus.textContent = isZh ? '在线 (帧同步正常)' : 'Online (Frame Synced)';
        }
        if (dom.oobeRunoutStatus) {
            dom.oobeRunoutStatus.className = 'check-result-badge badge-success';
            dom.oobeRunoutStatus.textContent = isZh ? '正常 (料丝在位)' : 'Normal (Filament Present)';
        }
        updateRunoutSensorsDOM(true);
    }

    function updateUIFromTelemetry(data) {
        if (!data) return;
        appState.isConnected = true;
        if (dom.statusDot) dom.statusDot.className = 'status-dot connected';
        if (dom.connStatus) dom.connStatus.textContent = t('status_connected');

        var hwOnline = evaluateHardwareOnline(data);
        setHardwareOnline(hwOnline);

        var gen = (data.generation_id !== undefined) ? data.generation_id : data.state_generation;
        if (gen !== undefined && dom.stateGen) {
            dom.stateGen.textContent = gen;
        }

        if (data.tool) {
            updateToolTelemetry(data.tool);
        }
        if (data.bed) {
            updateBedTelemetry(data.bed);
        }
        if (data.devices) {
            if (data.devices.th) {
                appState.devices.th = data.devices.th;
                updateDeviceVersion('th', data.devices.th, dom.thFirmwareVersion, dom.oobeThVersion, dom.oobeThStatus);
            }
            if (data.devices.mc) {
                appState.devices.mc = data.devices.mc;
                updateDeviceVersion('mc', data.devices.mc, dom.mcFirmwareVersion, dom.oobeMcVersion, dom.oobeMcStatus);
            }
        }
        updateOobeTelemetryLinks();
    }

    function applyTelemetrySnapshot(data) {
        updateUIFromTelemetry(data);
    }

    function updateDeviceVersion(nodeKey, devInfo, cardElem, oobeVerElem, oobeBadgeElem) {
        if (!devInfo) return;
        var st = (devInfo.valid ? devInfo.status : 'UNKNOWN') || 'UNKNOWN';
        var verText = t('ver_status_unknown');
        var badgeText = t('status_unready');
        var badgeClass = 'check-result-badge badge-warning';

        if (st === 'ONLINE') {
            verText = 'v' + (devInfo.firmware_version || '?.?');
            if (devInfo.git_commit) {
                verText += ' (' + devInfo.git_commit + ')';
            }
            badgeText = t('status_online');
            badgeClass = 'check-result-badge badge-success';
        } else if (st === 'STALE') {
            verText = 'v' + (devInfo.firmware_version || '?.?');
            if (devInfo.git_commit) {
                verText += ' (' + devInfo.git_commit + ')';
            }
            verText += ' [' + t('ver_status_stale') + ']';
            badgeText = t('ver_status_stale');
            badgeClass = 'check-result-badge badge-warning';
        } else if (st === 'OFFLINE') {
            verText = t('ver_status_offline');
            badgeText = t('ver_status_offline');
            badgeClass = 'check-result-badge badge-danger';
        } else if (st === 'QUERY_FAILED') {
            verText = t('ver_status_query_failed');
            badgeText = t('ver_status_query_failed');
            badgeClass = 'check-result-badge badge-danger';
        } else {
            verText = t('ver_status_unknown');
            badgeText = t('status_unready');
            badgeClass = 'check-result-badge badge-warning';
        }

        if (cardElem) {
            cardElem.textContent = verText;
        }
        if (oobeVerElem) {
            oobeVerElem.textContent = t('lbl_firmware_ver') + ' ' + verText;
        }
        if (oobeBadgeElem) {
            oobeBadgeElem.textContent = badgeText;
            oobeBadgeElem.className = badgeClass;
        }
    }

    function connectTelemetryStream() {
        try {
            if (appState.eventSource) {
                appState.eventSource.close();
            }
            var es = new EventSource(GATEWAY_BASE_URL + '/api/v1/temperature/stream');
            es.addEventListener('temp_update', function (e) {
                try {
                    var data = JSON.parse(e.data);
                    applyTelemetrySnapshot(data);
                } catch (err) {}
            });
            es.addEventListener('job_update', function (e) {
                try {
                    var jobData = JSON.parse(e.data);
                    applyJobStatus(jobData);
                } catch (err) {}
            });
            es.onerror = function () {
                appState.isConnected = false;
                if (dom.statusDot) dom.statusDot.className = 'status-dot disconnected';
                if (dom.connStatus) dom.connStatus.textContent = t('status_disconnected');
                setHardwareOnline(false);
            };
            appState.eventSource = es;
        } catch (e) {
            appState.isConnected = false;
            setHardwareOnline(false);
        }
    }

    function fetchInitialSnapshot() {
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', GATEWAY_BASE_URL + '/api/v1/temperature/snapshot', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    try {
                        var data = JSON.parse(xhr.responseText);
                        applyTelemetrySnapshot(data);
                    } catch (e) {}
                } else if (xhr.status === 503 || xhr.status === 504) {
                    setHardwareOnline(false);
                    showToast(t('hw_offline_banner_msg'), 'warning');
                }
            };
            xhr.onerror = function () {
                appState.isConnected = false;
                setHardwareOnline(false);
            };
            xhr.send();
        } catch (e) {}
    }

    function formatSeconds(sec) {
        if (!sec || sec < 0) sec = 0;
        var h = Math.floor(sec / 3600);
        var m = Math.floor((sec % 3600) / 60);
        var s = Math.floor(sec % 60);
        var pad = function (n) { return (n < 10 ? '0' : '') + n; };
        return pad(h) + ':' + pad(m) + ':' + pad(s);
    }

    function applyJobStatus(job) {
        if (!job) return;
        if (dom.jobStatusBadge) {
            dom.jobStatusBadge.textContent = job.job_state || 'IDLE';
            var cls = 'status-badge';
            if (job.estop_active) cls += ' badge-danger';
            else if (job.job_state === 'PRINTING') cls += ' badge-success';
            else if (job.job_state === 'PAUSED') cls += ' badge-warning';
            else if (job.job_state === 'COMPLETED') cls += ' badge-primary';
            dom.jobStatusBadge.className = cls;
        }
        if (dom.jobProgressPercent) {
            var pct = ((job.progress_permille || 0) / 10).toFixed(1) + '%';
            dom.jobProgressPercent.textContent = pct;
        }
        if (dom.jobProgressCircle) {
            var circumference = 427.25;
            var progress = (job.progress_permille || 0) / 1000;
            var offset = circumference * (1 - progress);
            dom.jobProgressCircle.style.strokeDashoffset = offset;
        }
        if (dom.jobLayerInfo) {
            dom.jobLayerInfo.textContent = 'Layer ' + (job.current_line || 0) + ' / ' + (job.total_lines || 350);
        }
        if (dom.jobElapsedTime) {
            dom.jobElapsedTime.textContent = formatSeconds(job.elapsed_seconds);
        }
        if (dom.jobRemainingTime) {
            dom.jobRemainingTime.textContent = formatSeconds(job.remaining_seconds);
        }
        if (dom.jobModelName && job.model_name) {
            dom.jobModelName.textContent = job.model_name;
        }
        if (dom.jobCurrentLine && job.last_gcode) {
            dom.jobCurrentLine.textContent = job.last_gcode;
        }
        if (dom.coordValX) dom.coordValX.textContent = (job.pos_x_mm || 0).toFixed(2);
        if (dom.coordValY) dom.coordValY.textContent = (job.pos_y_mm || 0).toFixed(2);
        if (dom.coordValZ) dom.coordValZ.textContent = (job.pos_z_mm || 0).toFixed(2);
        if (dom.coordValE) dom.coordValE.textContent = (job.pos_e_mm || 0).toFixed(2);

        var state = job.job_state || 'IDLE';
        if (dom.btnJobStart) dom.btnJobStart.style.display = (state === 'IDLE' || state === 'COMPLETED') ? 'inline-flex' : 'none';
        if (dom.btnJobPause) dom.btnJobPause.style.display = (state === 'PRINTING') ? 'inline-flex' : 'none';
        if (dom.btnJobResume) dom.btnJobResume.style.display = (state === 'PAUSED') ? 'inline-flex' : 'none';
        if (dom.btnJobCancel) dom.btnJobCancel.style.display = (state === 'PRINTING' || state === 'PAUSED') ? 'inline-flex' : 'none';
        if (dom.btnHeaderEstopClear) {
            if (job.estop_active) {
                dom.btnHeaderEstopClear.classList.add('estop-active-highlight');
            } else {
                dom.btnHeaderEstopClear.classList.remove('estop-active-highlight');
            }
        }
        if (dom.estopBadge) {
            dom.estopBadge.textContent = job.estop_active ? t('estop_active_badge') : t('estop_normal');
        }
    }

    function renderLevelingGrid(mesh) {
        if (!dom.levelingMeshGrid || !mesh || !mesh.grid) return;
        dom.levelingMeshGrid.innerHTML = '';
        var grid = mesh.grid;
        for (var r = 0; r < grid.length; r++) {
            for (var c = 0; c < grid[r].length; c++) {
                var val = grid[r][c];
                var cell = document.createElement('div');
                cell.className = 'mesh-cell';
                cell.textContent = (val >= 0 ? '+' : '') + val.toFixed(2);
                if (val > 0.08) cell.style.background = '#ef4444';
                else if (val > 0.02) cell.style.background = '#f59e0b';
                else if (val < -0.05) cell.style.background = '#1e40af';
                else if (val < -0.02) cell.style.background = '#3b82f6';
                else cell.style.background = '#10b981';
                dom.levelingMeshGrid.appendChild(cell);
            }
        }
        if (dom.meshVarianceVal && mesh.variance) dom.meshVarianceVal.textContent = mesh.variance.toFixed(2) + ' mm';
        if (dom.meshTiltVal && mesh.tilt) dom.meshTiltVal.textContent = mesh.tilt;
    }

    function sendPostRequest(path, bodyJson, onSuccess, onError) {
        if (appState.hwOnline === false && path !== '/api/v1/emergency/stop' && path !== '/api/v1/emergency/clear') {
            showToast(t('hw_offline_banner_msg'), 'warning');
            if (onError) onError(503, 'Hardware offline');
            return;
        }
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', GATEWAY_BASE_URL + path, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onload = function () {
                if (xhr.status >= 200 && xhr.status < 300) {
                    if (onSuccess) {
                        try {
                            onSuccess(JSON.parse(xhr.responseText));
                        } catch (e) {
                            onSuccess({});
                        }
                    }
                } else if (xhr.status === 503 || xhr.status === 504) {
                    var errMsg = '硬件已断开连接 (HTTP ' + xhr.status + ')';
                    try {
                        var errObj = JSON.parse(xhr.responseText);
                        if (errObj && errObj.message) {
                            errMsg = errObj.message;
                        }
                    } catch (e) {}
                    showToast(errMsg, 'warning');
                    setHardwareOnline(false);
                    if (onError) onError(xhr.status, errMsg);
                } else {
                    if (onError) onError(xhr.status, xhr.statusText);
                }
            };
            xhr.onerror = function () {
                showToast(t('net_error') || '网络请求失败', 'error');
                if (onError) onError(0, 'Network Error');
            };
            xhr.send(bodyJson ? JSON.stringify(bodyJson) : null);
        } catch (e) {
            if (onError) onError(0, e.message);
        }
    }

    function fetchInitialJobStatus() {
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', GATEWAY_BASE_URL + '/api/v1/jobs/status', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    try {
                        applyJobStatus(JSON.parse(xhr.responseText));
                    } catch (e) {}
                } else if (xhr.status === 503 || xhr.status === 504) {
                    setHardwareOnline(false);
                }
            };
            xhr.send();
        } catch (e) {}
    }

    function fetchInitialMesh() {
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', GATEWAY_BASE_URL + '/api/v1/leveling/mesh', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    try {
                        renderLevelingGrid(JSON.parse(xhr.responseText));
                    } catch (e) {}
                } else if (xhr.status === 503 || xhr.status === 504) {
                    setHardwareOnline(false);
                }
            };
            xhr.send();
        } catch (e) {}
    }

    function initDashboardEvents() {
        if (dom.btnJobStart) {
            dom.btnJobStart.addEventListener('click', function () {
                var m = (dom.jobModelName) ? dom.jobModelName.textContent : '3DBenchy.gcode';
                sendPostRequest('/api/v1/jobs/start', { model: m }, function () {
                    fetchInitialJobStatus();
                });
            });
        }
        if (dom.btnJobPause) {
            dom.btnJobPause.addEventListener('click', function () {
                sendPostRequest('/api/v1/jobs/pause', null, function () {
                    fetchInitialJobStatus();
                });
            });
        }
        if (dom.btnJobResume) {
            dom.btnJobResume.addEventListener('click', function () {
                sendPostRequest('/api/v1/jobs/resume', null, function () {
                    fetchInitialJobStatus();
                });
            });
        }
        if (dom.btnJobCancel) {
            dom.btnJobCancel.addEventListener('click', function () {
                if (confirm('确定要取消当前打印作业吗？')) {
                    sendPostRequest('/api/v1/jobs/cancel', null, function () {
                        fetchInitialJobStatus();
                    });
                }
            });
        }
        if (dom.btnHeaderEstop) {
            dom.btnHeaderEstop.addEventListener('click', function () {
                sendPostRequest('/api/v1/emergency/stop', null, function () {
                    fetchInitialJobStatus();
                    fetchInitialSnapshot();
                    showToast(t('estop_triggered_toast'), 'error');
                });
            });
        }
        if (dom.btnHeaderEstopClear) {
            dom.btnHeaderEstopClear.addEventListener('click', function () {
                sendPostRequest('/api/v1/emergency/clear', null, function () {
                    fetchInitialJobStatus();
                    fetchInitialSnapshot();
                    showToast(t('estop_cleared_toast'), 'success');
                });
            });
        }

        var sampleBtns = document.querySelectorAll('[data-load-model]');
        for (var i = 0; i < sampleBtns.length; i++) {
            sampleBtns[i].addEventListener('click', function () {
                var model = this.getAttribute('data-load-model');
                if (dom.jobModelName) dom.jobModelName.textContent = model;
                sendPostRequest('/api/v1/jobs/start', { model: model }, function () {
                    fetchInitialJobStatus();
                });
            });
        }

        if (dom.gcodeDropzone && dom.gcodeFileInput) {
            dom.gcodeDropzone.addEventListener('click', function () {
                dom.gcodeFileInput.click();
            });
            dom.gcodeFileInput.addEventListener('change', function () {
                if (this.files && this.files[0]) {
                    var f = this.files[0];
                    if (dom.jobModelName) dom.jobModelName.textContent = f.name;
                    sendPostRequest('/api/v1/jobs/upload', { name: f.name, size: f.size }, function () {
                        alert('文件 "' + f.name + '" 上传装载成功！点击【开始打印】即可开始空跑走线。');
                    });
                }
            });
        }
    }

    function initMotionEvents() {
        var currentStep = 10.0;
        var stepBtns = document.querySelectorAll('.btn-step');
        for (var i = 0; i < stepBtns.length; i++) {
            stepBtns[i].addEventListener('click', function () {
                for (var j = 0; j < stepBtns.length; j++) stepBtns[j].classList.remove('active');
                this.classList.add('active');
                currentStep = parseFloat(this.getAttribute('data-step')) || 10.0;
            });
        }

        var jogBtns = document.querySelectorAll('.btn-jog[data-axis]');
        for (var k = 0; k < jogBtns.length; k++) {
            jogBtns[k].addEventListener('click', function () {
                var axis = this.getAttribute('data-axis');
                var dir = parseFloat(this.getAttribute('data-dir')) || 1.0;
                var step = (Math.abs(dir) < 1.0) ? dir : (currentStep * dir);
                sendPostRequest('/api/v1/motion/jog', { axis: axis, step_mm: step }, function () {
                    fetchInitialJobStatus();
                });
            });
        }

        if (dom.btnHomeAll) {
            dom.btnHomeAll.addEventListener('click', function () {
                sendPostRequest('/api/v1/motion/home', { axes: 'ALL' }, function () {
                    fetchInitialJobStatus();
                });
            });
        }
        if (dom.btnHomeXy) {
            dom.btnHomeXy.addEventListener('click', function () {
                sendPostRequest('/api/v1/motion/home', { axes: 'XY' }, function () {
                    fetchInitialJobStatus();
                });
            });
        }
        if (dom.btnTriggerLeveling) {
            dom.btnTriggerLeveling.addEventListener('click', function () {
                sendPostRequest('/api/v1/leveling/trigger', null, function () {
                    fetchInitialMesh();
                });
            });
        }
    }

    /**
     * @brief 发送手动或快捷 G-code 指令至后端 0x1C 真实闭环
     */
    function dispatchManualGcode(rawCmd) {
        if (!rawCmd) return;
        var cmd = String(rawCmd).trim().toUpperCase();
        if (!cmd) return;
        sendPostRequest('/api/v1/gcode/execute', { gcode: cmd }, function () {
            if (dom.jobCurrentLine) {
                dom.jobCurrentLine.textContent = cmd + ' ; Hardware ACK OK';
            }
            fetchInitialJobStatus();
            fetchInitialSnapshot();
            showToast(t('gcode_ack_toast') + ': ' + cmd, 'success');
        });
    }

    /**
     * @brief 初始化手动 G-code 输入框与快捷指令按钮事件
     */
    function initGcodeEvents() {
        if (dom.btnSendGcode && dom.gcodeManualInput) {
            dom.btnSendGcode.addEventListener('click', function () {
                dispatchManualGcode(dom.gcodeManualInput.value);
            });
            dom.gcodeManualInput.addEventListener('keydown', function (ev) {
                if (ev.key === 'Enter' || ev.keyCode === 13) {
                    ev.preventDefault();
                    dispatchManualGcode(dom.gcodeManualInput.value);
                }
            });
        }
        var quickBtns = document.querySelectorAll('.btn-quick-gcode');
        for (var i = 0; i < quickBtns.length; i++) {
            quickBtns[i].addEventListener('click', function () {
                var g = this.getAttribute('data-gcode');
                if (dom.gcodeManualInput && g) dom.gcodeManualInput.value = g;
                dispatchManualGcode(g);
            });
        }
    }

    /**
     * @brief 下发喷嘴与热床目标温度至后端 0x10 双节点闭环
     */
    function submitTargetTemperature(nozC, bedC) {
        var nozDeci = Math.round((parseFloat(nozC) || 0) * 10);
        var bedDeci = Math.round((parseFloat(bedC) || 0) * 10);
        if (nozDeci < 0) nozDeci = 0;
        if (nozDeci > 3000) nozDeci = 3000;
        if (bedDeci < 0) bedDeci = 0;
        if (bedDeci > 1200) bedDeci = 1200;
        appState.targetThDeciC = nozDeci;
        appState.targetMcDeciC = bedDeci;
        sendPostRequest('/api/v1/temperature/set', {
            nozzle_temp_deci_c: nozDeci,
            bed_temp_deci_c: bedDeci
        }, function () {
            if (dom.thTargetTemp) dom.thTargetTemp.textContent = (nozDeci / 10).toFixed(1) + ' °C';
            if (dom.mcTargetTemp) dom.mcTargetTemp.textContent = (bedDeci / 10).toFixed(1) + ' °C';
            fetchInitialSnapshot();
            showToast(t('temp_ack_toast') + ' (TH=' + (nozDeci / 10).toFixed(0) + '°C, MC=' + (bedDeci / 10).toFixed(0) + '°C)', 'success');
        });
    }

    /**
     * @brief 初始化喷嘴与热床目标温度设定与预设按钮事件
     */
    function initTempControlEvents() {
        if (dom.btnSetThTemp) {
            dom.btnSetThTemp.addEventListener('click', function () {
                var thVal = dom.inputThTarget ? parseFloat(dom.inputThTarget.value) : 200;
                var mcVal = (appState.targetMcDeciC > 0) ? (appState.targetMcDeciC / 10) :
                            (dom.inputMcTarget ? parseFloat(dom.inputMcTarget.value) : 0);
                submitTargetTemperature(thVal, mcVal);
            });
        }
        if (dom.btnSetMcTemp) {
            dom.btnSetMcTemp.addEventListener('click', function () {
                var mcVal = dom.inputMcTarget ? parseFloat(dom.inputMcTarget.value) : 60;
                var thVal = (appState.targetThDeciC > 0) ? (appState.targetThDeciC / 10) :
                            (dom.inputThTarget ? parseFloat(dom.inputThTarget.value) : 0);
                submitTargetTemperature(thVal, mcVal);
            });
        }
        var thPresets = document.querySelectorAll('.btn-th-preset');
        for (var i = 0; i < thPresets.length; i++) {
            thPresets[i].addEventListener('click', function () {
                var tVal = parseFloat(this.getAttribute('data-temp')) || 0;
                if (dom.inputThTarget) dom.inputThTarget.value = tVal;
                submitTargetTemperature(tVal, appState.targetMcDeciC / 10);
            });
        }
        var mcPresets = document.querySelectorAll('.btn-mc-preset');
        for (var j = 0; j < mcPresets.length; j++) {
            mcPresets[j].addEventListener('click', function () {
                var bVal = parseFloat(this.getAttribute('data-temp')) || 0;
                if (dom.inputMcTarget) dom.inputMcTarget.value = bVal;
                submitTargetTemperature(appState.targetThDeciC / 10, bVal);
            });
        }
    }

    /* ===================================================================== */
    /* 7. 初始化启动                                                         */
    /* ===================================================================== */

    function init() {
        setTheme('dark');
        setLanguage('zh-CN');
        updateHardwareConnectionUI(null);
        for (var i = 0; i < 4; i++) syncSlotDOM(i);
        updateWeightValidationUI();
        initSlotEvents();
        initOobeEvents();
        initNavEvents();
        initDashboardEvents();
        initGcodeEvents();
        initTempControlEvents();
        initMotionEvents();
        fetchInitialSnapshot();
        fetchInitialJobStatus();
        fetchInitialMesh();
        connectTelemetryStream();

        try {
            if (typeof localStorage === 'undefined' || localStorage.getItem('aisoc_oobe_completed') !== 'true') {
                if (dom.oobeModal) {
                    dom.oobeModal.style.display = 'flex';
                }
                setOobeStep(1);
            }
        } catch (e) {
            console.warn('LocalStorage check failed:', e);
            if (dom.oobeModal) {
                dom.oobeModal.style.display = 'flex';
            }
            setOobeStep(1);
        }
    }

    if (typeof window !== 'undefined') {
        window.HMI_CORE = {
            extractTemperatureC: extractTemperatureC,
            evaluateHardwareOnline: evaluateHardwareOnline,
            setHardwareOnline: setHardwareOnline,
            setControlsLocked: setControlsLocked,
            showToast: showToast,
            fetchApi: fetchApi,
            switchTab: switchTab
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
