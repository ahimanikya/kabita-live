// Reader-only shortcuts must leave editing and browser/assistive shortcuts alone.
export function readerKeyAction(event, {open, settingsOpen, selectionActive = false}) {
  if (!open || settingsOpen || selectionActive || event.defaultPrevented || event.isComposing ||
      event.repeat || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target?.isContentEditable || event.target?.closest?.('input,select,textarea,[role=textbox],[role=slider],[role=spinbutton]')) return null;
  if (event.key === 'ArrowRight' || event.key === 'PageDown') return 'next';
  if (event.key === 'ArrowLeft' || event.key === 'PageUp') return 'previous';
  if (event.key.toLowerCase() === 'f') return 'fullscreen';
  return null;
}

// Only leave fullscreen on reader close when this reader entered it.
export function createReaderFullscreen({document, root, isOpen, onChange, announce}) {
  const supported = !!(document.fullscreenEnabled && root.requestFullscreen && document.exitFullscreen);
  let owned = false, pending = false;
  const active = () => document.fullscreenElement === root;
  async function leave() {
    if (!owned) return;
    owned = false;
    if (active()) {
      try { await document.exitFullscreen(); }
      catch { announce('Use Esc or your browser controls to leave full screen.'); }
    }
  }
  async function toggle() {
    if (!supported || pending || !isOpen()) return;
    pending = true;
    try {
      if (document.fullscreenElement) {
        await document.exitFullscreen(); owned = false;
      } else {
        await root.requestFullscreen(); owned = active();
        if (!isOpen()) await leave();
      }
    } catch { announce('Full screen is not available. You can keep reading here.'); }
    finally { pending = false; onChange(active()); }
  }
  document.addEventListener('fullscreenchange', () => {
    if (!active()) owned = false;
    onChange(active());
  });
  return {supported, active, toggle, leave, sync: () => onChange(active())};
}
