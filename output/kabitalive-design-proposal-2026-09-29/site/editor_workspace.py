def render_editor_workspace(root):
    (root/"editor-workspace.html").write_text((root/"data/editor-workspace.html.template").read_text())
