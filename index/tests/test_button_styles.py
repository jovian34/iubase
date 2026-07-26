import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup


TEMPLATES_ROOT = Path(__file__).parents[2] / "django_project" / "templates"
BUTTON_CLASSES = (
    ("add", "add-button"),
    ("edit", "edit-button"),
)


def get_button_context(button):
    context = f"{button.get_text(' ', strip=True)} {button}"
    action_parent = button.find_parent(["a", "form"])
    if action_parent:
        context = f"{context} {action_parent}"
    return context


def button_action(button):
    context = get_button_context(button)
    if re.search(r"\bedit(?:ed)?\b|edit_", context, re.IGNORECASE):
        return "edit"
    if re.search(r"\badd\b|add_", context, re.IGNORECASE):
        return "add"
    return None


def find_buttons_for_action(action):
    matching_buttons = []
    for template_path in TEMPLATES_ROOT.rglob("*.html"):
        template = BeautifulSoup(template_path.read_text(), "html.parser")
        for button in template.find_all("button"):
            if button_action(button) == action:
                matching_buttons.append((template_path, button))
    return matching_buttons


@pytest.mark.parametrize(("action", "expected_class"), BUTTON_CLASSES)
def test_add_and_edit_buttons_use_semantic_css_class(action, expected_class):
    incorrectly_styled_buttons = []
    action_buttons = find_buttons_for_action(action)

    assert action_buttons
    for template_path, button in action_buttons:
        if expected_class not in button.get("class", []):
            relative_path = template_path.relative_to(TEMPLATES_ROOT)
            button_text = button.get_text(" ", strip=True)
            incorrectly_styled_buttons.append(f"{relative_path}: {button_text}")

    assert not incorrectly_styled_buttons, (
        f"{action.title()} buttons missing {expected_class}: "
        + ", ".join(incorrectly_styled_buttons)
    )
