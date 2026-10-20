# v2.0 开发前协议算术核对

[protocol_preflight.json](protocol_preflight.json)记录本地协议原稿 SHA256、五个黄金物理帧、独立计算 CRC、声明长度及实际总长、版本位，以及 CRC 查表全部 256 项的核对结果。

计算方法为标准库 `binascii.crc_hqx(frame_without_crc, 0xFFFF)`，与帧尾小端 CRC 比较；查表逐项按多项式 `0x1021`、不反射方式逐位推导。没有借用待开发编解码器的输出作为预期。

结果：五帧结构/CRC 匹配，表项全部匹配。V04 的 `L=0` 与命令注册/结构中的急停 2 字节长度冲突仍然存在，不能以 CRC 正确消除语义问题。此记录是作者的文档预核对，不是生产实现测试、独立 QA 验收或硬件通信结果。

下一步与边界见[首轮开发安排](../../planning/minimc_v2_first_increment_20261020.md)。
