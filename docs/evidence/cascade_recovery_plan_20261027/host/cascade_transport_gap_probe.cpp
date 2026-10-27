#include "serial_posix.h"
#include <cerrno>
#include <cstdio>
#include <cstring>
#include <termios.h>
#include <unistd.h>

static bool g_zero_write = false;

extern "C" ssize_t __real_write(int fd, const void* data, size_t size);

extern "C" ssize_t __wrap_write(int fd, const void* data, size_t size) {
    if (g_zero_write) return 0;
    return __real_write(fd, data, size);
}

static int probe_write(minimc::SerialContext* ctx, const char* mode) {
    if (!ctx || !mode) return 2;
    uint8_t data[4096] = {};
    if (std::strcmp(mode, "eagain") == 0) {
        ssize_t count = 1;
        while (count > 0) count = __real_write(ctx->fd, data, sizeof(data));
        std::printf("FILL_RESULT=%zd ERRNO=%d\n", count, errno);
        std::fflush(stdout);
    }
    g_zero_write = std::strcmp(mode, "zero") == 0;
    size_t written = 0;
    const bool ok = minimc::serial_write(ctx, data, sizeof(data), &written);
    std::printf("SERIAL_WRITE_RETURN=%d COUNT=%zu\n", ok, written);
    return ok ? 0 : 1;
}

int main(int argc, char* argv[]) {
    if (!argv || argc != 3) return 2;
    const uint32_t baud = std::strcmp(argv[1], "baud") == 0 ? 921600 : 115200;
    minimc::SerialConfig cfg{argv[2], baud};
    minimc::SerialContext ctx{};
    if (!minimc::serial_open(&cfg, &ctx)) return 3;
    if (std::strcmp(argv[1], "baud") != 0) return probe_write(&ctx, argv[1]);
    termios tty{};
    if (tcgetattr(ctx.fd, &tty) != 0) return 4;
    std::printf("REQUEST=921600 ACTUAL_IS_115200=%d\n", cfgetospeed(&tty) == B115200);
    minimc::serial_close(&ctx);
    return 0;
}
