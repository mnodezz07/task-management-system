
import json
import pytest
import task_manager as tm


@pytest.fixture
def temporary_tasks_file(tmp_path, monkeypatch):
    """Give every test its own temporary JSON file."""
    data_dir = tmp_path / "data"
    tasks_file = data_dir / "tasks.json"

    monkeypatch.setattr(tm, "DATA_DIR", data_dir)
    monkeypatch.setattr(tm, "TASKS_FILE", tasks_file)

    return tasks_file


def test_create_and_view_task(temporary_tasks_file):
    task = tm.create_task(
        "Finish report",
        "Write the project report",
        created_by="user-1",
    )

    tasks = tm.view_tasks()

    assert task.title == "Finish report"
    assert task.status == "Pending"
    assert len(tasks) == 1
    assert tasks[0].id == task.id


def test_edit_task(temporary_tasks_file):
    task = tm.create_task("Old title", "Old description", "user-1")

    updated = tm.edit_task(
        task.id,
        title="New title",
        description="New description",
    )

    assert updated.title == "New title"
    assert updated.description == "New description"


def test_update_status(temporary_tasks_file):
    task = tm.create_task("Write tests", "Test functions", "user-1")

    updated = tm.update_task_status(task.id, "Completed")

    assert updated.status == "Completed"


def test_invalid_status(temporary_tasks_file):
    task = tm.create_task("Write tests", "Test functions", "user-1")

    with pytest.raises(ValueError):
        tm.update_task_status(task.id, "Finished")


def test_delete_task(temporary_tasks_file):
    task = tm.create_task("Temporary task", "Delete this", "user-1")

    deleted = tm.delete_task(task.id)

    assert deleted.id == task.id
    assert tm.view_tasks() == []


def test_empty_title_rejected(temporary_tasks_file):
    with pytest.raises(ValueError):
        tm.create_task("", "A description", "user-1")


def test_empty_description_rejected(temporary_tasks_file):
    with pytest.raises(ValueError):
        tm.create_task("A title", "", "user-1")


def test_missing_task_rejected(temporary_tasks_file):
    with pytest.raises(ValueError):
        tm.edit_task("missing-task-id", title="New title")


def test_task_is_saved_as_json(temporary_tasks_file):
    tm.create_task("Save task", "Test JSON storage", "user-1")

    with temporary_tasks_file.open(encoding="utf-8") as file:
        saved_tasks = json.load(file)

    assert len(saved_tasks) == 1
    assert saved_tasks[0]["title"] == "Save task"
    assert saved_tasks[0]["created_by"] == "user-1"


