"""Lightweight, local-only Switch YAML smoke validation.

This is NOT the official Switch import/validation engine. It never talks to
Switch or changes the user's live agents, rooms, credentials or messaging apps.
"""
from pathlib import Path
import sys
try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing. Install it with: python -m pip install PyYAML")

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / 'exam-rescue-telegram.template.yaml', ROOT / 'exam-rescue-new-room.template.yaml']
EXPECTED_PARAM_TYPES = {'string','number','boolean','enum','agent','bridge','room','user','provider','location','directory','machine'}


def check(path):
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    assert isinstance(data, dict), f'{path.name}: document must be a mapping'
    assert data.get('version') == 1, f'{path.name}: expected Switch template version 1'
    assert len(data.get('agents', [])) == 2, f'{path.name}: expected two agents'
    params = data.get('params')
    assert isinstance(params, dict) and params, f'{path.name}: missing params'
    for name, p in params.items():
        assert p.get('type') in EXPECTED_PARAM_TYPES, f'{path.name}: invalid param type {name}'
    agent_names = set()
    for agent in data['agents']:
        for key in ('name', 'display_name', 'instructions', 'provider', 'location', 'directory', 'model'):
            assert agent.get(key), f'{path.name}: missing agent field {key}'
        assert agent['name'] not in agent_names, f'{path.name}: duplicated agent name'
        agent_names.add(agent['name'])
        assert agent.get('auto_approve') is False, f'{path.name}: unsafe bypass enabled'
        assert agent.get('auto_mode') is True, f'{path.name}: auto mode should remain on'
        assert agent.get('addressing') == 'anyone', f'{path.name}: expected human room member addressing'
    if path.name.endswith('telegram.template.yaml'):
        assert 'room' not in data, 'Telegram template must NOT attempt group creation'
        assert params['where']['type'] == 'room', 'Telegram needs an existing Switch room'
        assert all(agent.get('join') == ['{where}'] for agent in data['agents']), 'Missing existing-room join'
    else:
        assert params['bridge']['type'] == 'bridge', 'New-room template needs selectable bridge'
        assert data['room']['bridge'] == '{bridge}', 'New-room bridge must be configured'
        assert len(data['room']['agents']) == 2, 'Room must include both agents'
    return f'PASS — {path.name}: valid YAML and basic expected Switch structure'


if __name__ == '__main__':
    for f in FILES:
        print(check(f))
    print('NOTE: Runtime import, room creation, and permissions were NOT tested.')
