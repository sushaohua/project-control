"""AST-only extraction, all probe I/O replaced. Never import/run hardware scripts."""
import ast
import contextlib
import io
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional
ROOT=Path('/home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools')

def extract(name,names):
    tree=ast.parse((ROOT/name).read_text())
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'Any':Any,'Dict':Dict,'List':List,'Optional':Optional}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(ROOT/name),'exec'),ns)
    return ns,tree

d,_=extract('device_discovery.py',{'inspect_probe','discover_all','probe_memory_word'})
# Contradictory fingerprint: TH flash plus MC-like firmware stack still classified MC.
def fake_read(binary,probe,chip,addr,**kw):
    return {0x1FFFF7E0:[256],0x08000000:[0x20060000],0x1FFFF7E8:[1,2,3]}[addr]
d['probe_memory_word']=fake_read
print('conflicting_fingerprint_role',d['inspect_probe']('FAKE','probe-A')['role'])
# A role maps to the final probe, never rejects ambiguity.
d['find_probe_rs_bin']=lambda:'FAKE'
d['list_raw_probes']=lambda _:['probe-A','probe-B']
print('duplicate_role_selected',d['discover_all']()['target_mapping']['MC']['probe_id'])
# Read parses unrelated address and incorrect count without validation.
d,_=extract('device_discovery.py',{'probe_memory_word'})
d['run_cmd']=lambda *a,**kw:SimpleNamespace(returncode=0,stdout='deadbeef: 00000100\n')
print('wrong_address_count_read',d['probe_memory_word']('FAKE','probe-A','chip',0x1FFFF7E8,count=3))

f,tree=extract('probe_fault_injector.py',{'disable_uart','enable_uart','glitch_uart','reset_all_uarts','resolve_target_probe','get_uart_status','decode_ctrl1'})
for n in tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PERIPHERAL_REGISTERS' for t in n.targets):
        f['PERIPHERAL_REGISTERS']=ast.literal_eval(n.value)
print('manual_target_unchecked',f['resolve_target_probe']('FAKE','TH','probe-MC'))
# Failed snapshot must prevent writes; tool currently proceeds to write zero.
writes=[]
f['probe_memory_word']=lambda *a,**kw:None
f['resolve_target_probe']=lambda *a,**kw:('probe-A','AT32F423CCT7')
f['save_cached_state']=lambda *a:None
f['write_memory_word']=lambda *a:(writes.append(a[-1]) or True)
f['get_uart_status']=lambda *a,**kw:{'raw_hex':'0x00000000'}
f['disable_uart']('FAKE','TH','USART1')
print('write_after_failed_snapshot',writes)
# A sleep exception after disable does not call restore.
events=[]
f['disable_uart']=lambda *a,**kw:events.append('disabled')
f['enable_uart']=lambda *a,**kw:events.append('restored')
def fail_sleep(_):raise ValueError('simulated negative duration')
f['time']=SimpleNamespace(sleep=fail_sleep)
try:f['glitch_uart']('FAKE','TH','USART1',-1)
except ValueError:pass
print('glitch_cleanup_events',events)
# Reset-all ignores failed write and returns normally with success message.
f['discover_all']=lambda:{'target_mapping':{'TH':{'probe_id':'probe-A','chip':'AT32F423CCT7'}}}
f['write_memory_word']=lambda *a:False
output=io.StringIO()
with contextlib.redirect_stdout(output):result=f['reset_all_uarts']('FAKE')
print('reset_all_false_write_result',result)
print('reset_all_false_write_stdout',output.getvalue().strip().replace('\n',' | '))
# Negative duration bypasses any parser constraint; function scale and params are AST facts.
for name in ('device_discovery.py','probe_fault_injector.py'):
    tree=ast.parse((ROOT/name).read_text())
    violations=[]
    for n in tree.body:
        if isinstance(n,ast.FunctionDef):
            lines=n.end_lineno-n.lineno+1
            params=len(n.args.posonlyargs)+len(n.args.args)+len(n.args.kwonlyargs)
            if lines>50 or params>4:violations.append((n.name,lines,params))
    print('scale_violations',name,json.dumps(violations))
