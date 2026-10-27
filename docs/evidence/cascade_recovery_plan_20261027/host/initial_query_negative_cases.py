import binascii
import os
import pty
import select
import struct
import subprocess

EXE = '/tmp/independent_host_review_20261027_build/bin/soc-ap'


def frame(src=2, dst=1, flags=6, cmd=2, seq=1, payload=bytes(16)):
    header = bytes([0x55, 0xaa, src, dst, flags, cmd, 4, 0])
    body = header + struct.pack('<HH', seq, len(payload)) + payload
    return body + struct.pack('<H', binascii.crc_hqx(body, 0xffff))


def run_case(name, reply):
    master, slave = pty.openpty()
    args = [EXE, '--query-version', '--device', os.ttyname(slave), '--timeout-ms', '150']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ready, _, _ = select.select([master], [], [], 2)
    tx = os.read(master, 4096) if ready else b''
    if reply is not None:
        os.write(master, reply)
    out, err = proc.communicate(timeout=3)
    print('CASE', name, 'EXIT', proc.returncode, 'TX', tx.hex(' '))
    print('RX', None if reply is None else reply.hex(' '))
    print(out, end='')
    print(err, end='')
    os.close(master)
    os.close(slave)


run_case('silence', None)
run_case('echo_of_transmitted_request', bytes.fromhex('55aa01020503040001000000ae08'))
run_case('wrong_source', frame(src=3))
run_case('wrong_destination', frame(dst=3))
run_case('unknown_command', frame(cmd=0x7f))
run_case('not_response', frame(flags=4))
run_case('wrong_sequence', frame(seq=400))
run_case('short_version_payload', frame(payload=bytes([2, 0, 1, 9])))
