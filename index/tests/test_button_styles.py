import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup


TEMPLATES_ROOT = Path(__file__).parents[2] / "django_project" / "templates"
STYLESHEET_PATH = (
    Path(__file__).parents[2]
    / "django_project"
    / "static"
    / "index"
    / "css"
    / "style.css"
)
BUTTON_CLASSES = (
    ("add", "add-button"),
    ("edit", "edit-button"),
    ("delete", "delete-button"),
)


def get_button_context(button):
    context = f"{button.get_text(' ', strip=True)} {button}"
    action_parent = button.find_parent(["a", "form"])
    if action_parent:
        context = f"{context} {action_parent}"
    return context


def button_action(button):
    context = get_button_context(button)
    if re.search(r"\bdelete\b|delete_", context, re.IGNORECASE):
        return "delete"
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


def get_css_declarations(selector):
    stylesheet = STYLESHEET_PATH.read_text()
    rule = re.search(rf"{re.escape(selector)}\s*{{([^}}]+)}}", stylesheet)
    assert rule is not None
    return {
        property_name.strip(): value.strip()
        for declaration in rule.group(1).split(";")
        if ":" in declaration
        for property_name, value in [declaration.split(":", 1)]
    }


@pytest.mark.parametrize(("action", "expected_class"), BUTTON_CLASSES)
def test_action_buttons_use_semantic_css_class(action, expected_class):
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


@pytest.mark.parametrize("selector", (".edit-button", ".delete-button"))
def test_edit_and_delete_buttons_are_unshaded_with_thin_red_border(selector):
    declarations = get_css_declarations(selector)

    assert declarations["border"] == "1px solid var(--red)"
    assert declarations["background-color"] == "transparent"


def test_roster_heading_places_actions_beside_title():
    declarations = get_css_declarations(".roster-heading")
    action_declarations = get_css_declarations(".record-actions")

    assert declarations["align-items"] == "center"
    assert declarations["display"] == "flex"
    assert declarations["flex-wrap"] == "wrap"
    assert action_declarations["gap"] == "0.75rem"
