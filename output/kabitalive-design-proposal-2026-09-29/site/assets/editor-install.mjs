// Installation is optional. Shared editing continues to use the existing online service.
export function setupEditorInstall(win, doc) {
  const panel = doc.getElementById('editor-install');
  const button = doc.getElementById('editor-install-button');
  const status = doc.getElementById('editor-install-status');
  if (!panel || !button || !status) return;
  const display = win.matchMedia('(display-mode: standalone)');
  let pending = null;
  let installed = false;
  const isStandalone = () => installed || display.matches || win.navigator.standalone === true;
  const update = () => {
    const standalone = isStandalone();
    if (standalone && panel.contains(doc.activeElement)) {
      // Keep keyboard focus in the workspace when installation removes its UI.
      const next = ['cloud-logout', 'cloud-login', 'studio-home', 'cloud-status']
        .map(id => doc.getElementById(id))
        .find(element => element && !element.hidden && !element.disabled);
      next?.focus();
    } else if (!pending && doc.activeElement === button) {
      panel.querySelector('summary')?.focus();
    }
    panel.hidden = standalone;
    button.hidden = !pending || panel.hidden;
    if (panel.hidden) panel.open = false;
  };
  win.addEventListener('beforeinstallprompt', event => {
    if (isStandalone()) return;
    event.preventDefault();
    pending = event;
    status.textContent = '';
    update();
  });
  win.addEventListener('appinstalled', () => {
    installed = true;
    pending = null;
    update();
  });
  display.addEventListener?.('change', update);
  button.addEventListener('click', async () => {
    if (!pending) return;
    const prompt = pending;
    pending = null; // Browsers permit a prompt event to be used only once.
    try {
      const result = await prompt.prompt();
      const choice = result || await prompt.userChoice;
      status.textContent = choice?.outcome === 'accepted'
        ? 'Installation requested. Follow your browser’s instructions to finish.'
        : 'Installation cancelled. You can continue using Studio here.';
    } catch {
      status.textContent = 'Installation is unavailable right now. Try your browser’s install option, or continue here.';
    } finally {
      update();
    }
  });
  update();
}
if (typeof window !== 'undefined' && typeof document !== 'undefined') setupEditorInstall(window, document);
