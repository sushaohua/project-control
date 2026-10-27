import os
import pty
import select
import subprocess
import time

EXE = '/tmp/independent_host_review_20261027_build/bin/soc-ap'
LOG = '/tmp/cascade_host_gap_probes_20261027.log'


def emit(text):
    print(text)
    with open(LOG, 'a') as output:
        output.write(text + '\n')


def transport_case(mode):
    master, slave = pty.openpty()
    proc = subprocess.Popen(['/tmp/cascade_transport_gap_probe', mode, os.ttyname(slave)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = proc.communicate(timeout=0.3)
        emit(f'TRANSPORT {mode} EXIT={proc.returncode}\n{out}{err}')
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        emit(f'TRANSPORT {mode} WATCHDOG=300ms PROCESS_KILLED EXIT={proc.returncode}\n{out}{err}')
    os.close(master)
    os.close(slave)


def host_case(name, extra, inject=None):
    master, slave = pty.openpty()
    args = [EXE, '--query-version', '--device', os.ttyname(slave), '--timeout-ms', '80'] + extra
    start = time.monotonic()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ready, _, _ = select.select([master], [], [], 0.3)
    tx = os.read(master, 4096) if ready else b''
    if inject == 'hangup':
        os.close(master)
        master = None
    elif inject is not None:
        os.write(master, inject)
    out, err = proc.communicate(timeout=2)
    emit(f'HOST {name} ARGS={extra!r} EXIT={proc.returncode} ELAPSED={time.monotonic() - start:.3f}s TX={tx.hex()}\n{out}{err}')
    if master is not None:
        os.close(master)
    os.close(slave)


with open(LOG, 'w') as output:
    output.write('Host software audit only; no physical hardware / no HIL.\n')
for mode in ['baud', 'eagain', 'zero']:
    transport_case(mode)
for name, extra in [
    ('nonnumeric_timeout', ['--timeout-ms', 'garbage']),
    ('negative_timeout', ['--timeout-ms', '-1']),
    ('nonnumeric_cmd', ['--cmd-id', 'garbage']),
    ('trailing_garbage_cmd', ['--cmd-id', '3junk']),
    ('overflow_cmd', ['--cmd-id', '0x103']),
    ('negative_cmd', ['--cmd-id', '-1']),
    ('overflow_dst', ['--dst-id', '0x102']),
]:
    host_case(name, extra)
host_case('peer_hangup', [], 'hangup')
host_case('noise_capture_truncation', [], bytes([0x5a]) * 600)
