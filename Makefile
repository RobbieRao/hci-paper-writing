PYTHON ?= python3
SKILL_DIR := skills/hci-paper-writing

.PHONY: test validate audit init

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) $(SKILL_DIR)/scripts/validate_skill.py $(SKILL_DIR)

audit:
	@test -n "$(FILE)" || (echo "Usage: make audit FILE=path/to/paper.tex" && exit 2)
	$(PYTHON) $(SKILL_DIR)/scripts/manuscript_audit.py "$(FILE)"

init:
	@test -n "$(DIR)" || (echo "Usage: make init DIR=path/to/paper [MANUSCRIPT=paper.tex]" && exit 2)
	$(PYTHON) $(SKILL_DIR)/scripts/project_workspace.py "$(DIR)" --manuscript "$(MANUSCRIPT)"
