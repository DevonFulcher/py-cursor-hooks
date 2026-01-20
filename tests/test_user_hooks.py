import json

from hooks import interfaces, models
from hooks.models import HookEvent
from hooks.runner import build_hook_table, dispatch


class ExampleHooks(interfaces.CursorHooks):
    def before_read_file(
        self, input: models.BeforeReadFileInput
    ) -> models.BeforeReadFileOutput:
        if input.file_path.endswith(".env"):
            return models.BeforeReadFileOutput(
                permission="deny",
                user_message="No env files",
                agent_message="Blocked reading .env",
            )
        return models.BeforeReadFileOutput(permission="allow")

    def stop(self, input: models.StopInput) -> models.StopOutput:
        if input.status == "completed" and input.loop_count == 0:
            return models.StopOutput(
                followup_message="Please verify the changes before we finish."
            )
        return models.StopOutput()


def test_before_read_file_denies_env() -> None:
    hooks = ExampleHooks()
    table = build_hook_table(hooks)

    payload = {
        "hook_event_name": "beforeReadFile",
        "conversation_id": "c",
        "generation_id": "g",
        "workspace_roots": ["/repo"],
        "file_path": "/repo/.env",
        "content": "SECRET=1",
    }

    out = dispatch(
        hook_table=table, raw_json=json.dumps(payload), hook=HookEvent.beforeReadFile
    )
    assert isinstance(out, models.BeforeReadFileOutput)
    assert out.permission == "deny"
    assert out.user_message == "No env files"
    assert out.agent_message == "Blocked reading .env"


def test_stop_followup_serializes() -> None:
    hooks = ExampleHooks()
    table = build_hook_table(hooks)

    payload = {
        "hook_event_name": "stop",
        "conversation_id": "c",
        "generation_id": "g",
        "workspace_roots": [],
        "status": "completed",
        "loop_count": 0,
    }

    out = dispatch(hook_table=table, raw_json=json.dumps(payload), hook=HookEvent.stop)
    out_json = out.to_json_line()
    parsed = json.loads(out_json)
    assert parsed == {"followup_message": "Please verify the changes before we finish."}
