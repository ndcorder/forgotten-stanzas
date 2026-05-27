/**
 * desktop.js \u2014 Core application logic for Soft Estate
 *
 * Manages the frozen macOS Catalina desktop:
 * Window manager, file system navigation, evidence tagging,
 * and the Mira Voss presence system.
 *
 * Clock frozen at 3:47 AM, November 18, 2023.
 *
 * Depends on: FileSystem (global), Viewers (global)
 */

var Desktop = (function () {
  'use strict';

  /* \u2500\u2500\u2500 State \u2500\u2500\u2500 */

  var state = {
    windows: [],
    windowCounter: 0,
    activeWindow: null,
    dragState: null,
    evidence: [],
    introComplete: false
  };

  var Z_BASE = 10;
  var zCounter = Z_BASE;


  /* \u2500\u2500\u2500 DOM Helper \u2500\u2500\u2500 */

  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'className')       e.className = attrs[k];
        else if (k === 'innerHTML')  e.innerHTML = attrs[k];
        else if (k === 'textContent') e.textContent = attrs[k];
        else if (k.indexOf('on') === 0)
          e.addEventListener(k.slice(2).toLowerCase(), attrs[k]);
        else e.setAttribute(k, attrs[k]);
      });
    }
    if (children) {
      if (typeof children === 'string')
        e.textContent = children;
      else if (Array.isArray(children))
        children.forEach(function (c) { if (c) e.appendChild(c); });
      else if (children instanceof HTMLElement)
        e.appendChild(children);
    }
    return e;
  }


  /* \u2500\u2500\u2500 Intro Screen \u2500\u2500\u2500 */

  function showIntro() {
    var intro = el('div', {
      className: 'intro-screen',
      id: 'intro-screen'
    });
    intro.appendChild(el('div', {
      className: 'intro-title',
      textContent: 'SOFT ESTATE'
    }));
    intro.appendChild(el('div', {
      className: 'intro-subtitle',
      textContent: 'A digital archaeology'
    }));
    intro.appendChild(el('div', {
      className: 'intro-start',
      textContent: 'Click anywhere to begin'
    }));
    intro.appendChild(el('div', {
      className: 'intro-meta',
      textContent: 'Phase 1 \u2014 Forensic Inference'
    }));
    document.body.appendChild(intro);

    intro.addEventListener('click', function () {
      intro.style.transition = 'opacity 0.8s ease-out';
      intro.style.opacity = '0';
      setTimeout(function () {
        intro.remove();
        showLoading();
      }, 800);
    });
  }


  /* \u2500\u2500\u2500 Loading Screen \u2500\u2500\u2500 */

  function showLoading() {
    var loading = el('div', {
      className: 'loading-screen',
      id: 'loading-screen'
    });
    loading.appendChild(el('div', {
      className: 'loading-text',
      textContent: 'Restoring session\u2026'
    }));
    loading.appendChild(el('div', {
      className: 'loading-bar'
    }, [el('div', { className: 'loading-bar-fill' })]));
    document.body.appendChild(loading);

    setTimeout(function () {
      loading.classList.add('fade-out');
      setTimeout(function () {
        loading.remove();
        initDesktop();
      }, 800);
    }, 2800);
  }


  /* \u2500\u2500\u2500 Desktop Initialisation \u2500\u2500\u2500 */

  function initDesktop() {
    var desktop = el('div', { id: 'desktop' });
    document.body.appendChild(desktop);

    buildMenuBar();
    buildDesktopIcons();
    buildStickies();
    buildDock();
    buildEvidencePanel();
    setupGlobalEvents();

    state.introComplete = true;

    /* First Mira observation \u2014 delayed for atmosphere */
    setTimeout(function () {
      showCursorNote('Evidence case #2023-1118. Estate of Marsh, Elena V.');
    }, 2000);
  }


  /* \u2500\u2500\u2500 Menu Bar \u2500\u2500\u2500 */

  function buildMenuBar() {
    var menubar = el('div', { id: 'menubar' });
    var left  = el('div', { className: 'menubar-left' });
    var right = el('div', { className: 'menubar-right' });

    left.appendChild(el('span', {
      className: 'menubar-apple',
      textContent: '\uF8FF'
    }));
    left.appendChild(el('span', {
      className: 'menubar-app-name',
      textContent: 'Finder',
      id: 'menubar-appname'
    }));

    ['File', 'Edit', 'View', 'Window', 'Help'].forEach(function (n) {
      left.appendChild(el('span', {
        className: 'menubar-item',
        textContent: n
      }));
    });

    right.appendChild(el('span', { className: 'menubar-item', textContent: '\u266A' }));
    right.appendChild(el('span', { className: 'menubar-item', textContent: 'WiFi' }));
    right.appendChild(el('span', { className: 'menubar-item', textContent: '\uD83D\uDD0B 2%' }));
    right.appendChild(el('span', {
      className: 'menubar-clock',
      textContent: 'Sat Nov 18  3:47 AM'
    }));

    menubar.appendChild(left);
    menubar.appendChild(right);
    document.body.appendChild(menubar);
  }


  /* \u2500\u2500\u2500 Desktop Icons \u2500\u2500\u2500 */

  function buildDesktopIcons() {
    var container = el('div', { id: 'desktop-icons' });
    var desktopFiles = getDesktopChildren();

    desktopFiles.forEach(function (file) {
      var icon = el('div', { className: 'desktop-icon' });
      icon.appendChild(el('div', {
        className: 'desktop-icon-image',
        innerHTML: Viewers.getFileIcon(file)
      }));
      icon.appendChild(el('div', {
        className: 'desktop-icon-label',
        textContent: file.name
      }));

      icon.addEventListener('click', function (e) {
        e.stopPropagation();
        document.querySelectorAll('.desktop-icon.selected').forEach(function (i) {
          i.classList.remove('selected');
        });
        icon.classList.add('selected');
      });

      icon.addEventListener('dblclick', function (e) {
        e.stopPropagation();
        openFile(file);
      });

      container.appendChild(icon);
    });

    document.getElementById('desktop').appendChild(container);
  }

  function getDesktopChildren() {
    try {
      return Object.values(
        FileSystem.root.children.Users.children['elena.marsh'].children.Desktop.children
      );
    } catch (e) {
      return [];
    }
  }


  /* \u2500\u2500\u2500 Stickies \u2500\u2500\u2500 */

  function buildStickies() {
    if (!FileSystem.stickies || !FileSystem.stickies.length) return;
    var container = el('div', { className: 'stickies-container' });

    FileSystem.stickies.forEach(function (sticky) {
      var note = el('div', {
        className: 'sticky-note sticky-' + (sticky.color || 'yellow')
      });
      note.appendChild(el('div', {
        style: 'white-space:pre-wrap;',
        textContent: sticky.text
      }));
      note.appendChild(el('div', {
        className: 'sticky-meta',
        textContent: Viewers.formatDate(sticky.modified)
      }));
      container.appendChild(note);
    });

    document.getElementById('desktop').appendChild(container);
  }


  /* \u2500\u2500\u2500 Dock \u2500\u2500\u2500 */

  function buildDock() {
    var dock = el('div', { id: 'dock' });

    var apps = [
      { name: 'Finder',              cls: 'dock-icon-finder',    symbol: '\uD83D\uDD0D' },
      { name: 'Safari',              cls: 'dock-icon-safari',    symbol: '\uD83E\uDDF1' },
      { name: 'Mail',                cls: 'dock-icon-mail',      symbol: '\u2709',
        badge: FileSystem.emailInbox.length },
      { name: 'Calendar',            cls: 'dock-icon-calendar',  symbol: '17\nSAT' },
      { name: 'Photos',              cls: 'dock-icon-photos',    symbol: '\uD83C\uDFDE' },
      { name: 'TextEdit',            cls: 'dock-icon-textedit',  symbol: 'T' },
      { name: 'Terminal',            cls: 'dock-icon-terminal',  symbol: '>_' },
      { name: 'System Preferences',  cls: 'dock-icon-settings',  symbol: '\u2699' }
    ];

    apps.forEach(function (app) {
      var icon = el('div', {
        className: 'dock-icon ' + app.cls,
        'data-name': app.name,
        innerHTML: app.symbol
      });

      if (app.badge) {
        icon.appendChild(el('span', {
          className: 'notification-badge',
          textContent: String(app.badge)
        }));
      }

      icon.addEventListener('click', function () {
        handleDockClick(app.name);
      });
      dock.appendChild(icon);
    });

    document.body.appendChild(dock);
  }

  function handleDockClick(appName) {
    switch (appName) {
      case 'Finder':             openFinder(); break;
      case 'Safari':             openBrowserHistory(); break;
      case 'Mail':               openMail(); break;
      case 'Calendar':           openCalendar(); break;
      case 'Photos':             openPhotos(); break;
      case 'TextEdit':           openTextEditor(); break;
      case 'Terminal':           openTerminal(); break;
      case 'System Preferences':
        showCursorNote('System Preferences locked. Forensic mode.');
        break;
    }
  }


  /* \u2500\u2500\u2500 Evidence Panel \u2500\u2500\u2500 */

  function buildEvidencePanel() {
    var panel = el('div', {
      className: 'evidence-panel',
      id: 'evidence-panel'
    });

    var header = el('div', { className: 'evidence-header' });
    header.appendChild(el('span', {
      className: 'evidence-title',
      textContent: 'Evidence Tags'
    }));
    header.appendChild(el('span', {
      className: 'evidence-badge',
      id: 'evidence-count',
      textContent: '0'
    }));
    panel.appendChild(header);

    panel.appendChild(el('div', {
      className: 'evidence-list',
      id: 'evidence-list'
    }));

    /* Input area for manual notes */
    var inputArea = el('div', { className: 'evidence-input-area' });
    var input = el('input', {
      className: 'evidence-input',
      id: 'evidence-input',
      type: 'text',
      placeholder: 'Add observation\u2026'
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && input.value.trim()) {
        addEvidence('(Manual note)', input.value.trim());
        input.value = '';
      }
    });
    inputArea.appendChild(input);

    var btn = el('button', {
      className: 'evidence-tag-btn',
      textContent: '+'
    });
    btn.addEventListener('click', function () {
      if (input.value.trim()) {
        addEvidence('(Manual note)', input.value.trim());
        input.value = '';
      }
    });
    inputArea.appendChild(btn);
    panel.appendChild(inputArea);

    document.body.appendChild(panel);
  }

  function addEvidence(path, note) {
    state.evidence.push({
      path: path,
      note: note,
      timestamp: Date.now()
    });
    renderEvidenceList();
  }

  function renderEvidenceList() {
    var list = document.getElementById('evidence-list');
    if (!list) return;
    list.innerHTML = '';

    state.evidence.forEach(function (item) {
      var entry = el('div', { className: 'evidence-item' });
      entry.appendChild(el('div', {
        className: 'evidence-item-path',
        textContent: item.path
      }));
      entry.appendChild(el('div', {
        className: 'evidence-item-note',
        textContent: item.note
      }));
      list.appendChild(entry);
    });

    var badge = document.getElementById('evidence-count');
    if (badge) badge.textContent = String(state.evidence.length);
    list.scrollTop = list.scrollHeight;
  }


  /* \u2500\u2500\u2500 Window Manager \u2500\u2500\u2500 */

  function createWindow(options) {
    var id = 'win-' + (++state.windowCounter);
    var w = options.width  || 720;
    var h = options.height || 480;
    var x = options.x !== undefined
      ? options.x
      : 80 + (state.windowCounter % 5) * 30;
    var y = options.y !== undefined
      ? options.y
      : 60 + (state.windowCounter % 5) * 25;

    var win = el('div', {
      className: 'window opening',
      id: id,
      style: 'left:' + x + 'px;top:' + y + 'px;width:' + w + 'px;height:' + h +
             'px;z-index:' + (++zCounter)
    });

    /* Title bar */
    var titlebar = el('div', { className: 'window-titlebar' });
    var buttons = el('div', { className: 'window-buttons' });

    var closeBtn = el('div', {
      className: 'window-btn window-btn-close',
      innerHTML: '<svg viewBox="0 0 8 8"><line x1="1" y1="1" x2="7" y2="7"/>' +
                 '<line x1="7" y1="1" x2="1" y2="7"/></svg>'
    });
    var minBtn = el('div', {
      className: 'window-btn window-btn-minimize',
      innerHTML: '<svg viewBox="0 0 8 8"><line x1="1" y1="4" x2="7" y2="4"/></svg>'
    });
    var maxBtn = el('div', {
      className: 'window-btn window-btn-maximize',
      innerHTML: '<svg viewBox="0 0 8 8"><line x1="1" y1="1" x2="7" y2="7"/>' +
                 '<line x1="7" y1="1" x2="1" y2="7"/></svg>'
    });

    closeBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeWindow(id);
    });
    minBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeWindow(id);
    });

    buttons.appendChild(closeBtn);
    buttons.appendChild(minBtn);
    buttons.appendChild(maxBtn);

    titlebar.appendChild(buttons);
    titlebar.appendChild(el('div', {
      className: 'window-title',
      textContent: options.title || 'Untitled'
    }));
    win.appendChild(titlebar);

    /* Body: optional sidebar + content */
    var contentArea;

    if (options.sidebar) {
      var body    = el('div', { className: 'window-body' });
      var sidebar = el('div', { className: 'finder-sidebar' });
      options.sidebar.forEach(function (item) { sidebar.appendChild(item); });
      body.appendChild(sidebar);
      contentArea = el('div', {
        className: 'window-content',
        id: id + '-content'
      });
      body.appendChild(contentArea);
      win.appendChild(body);
    } else {
      contentArea = el('div', {
        className: 'window-content',
        id: id + '-content'
      });
      win.appendChild(contentArea);
    }

    /* Dragging */
    titlebar.addEventListener('mousedown', function (e) {
      if (e.target.closest('.window-btn')) return;
      focusWindow(id);
      var rect = win.getBoundingClientRect();
      state.dragState = {
        windowId: id,
        offsetX: e.clientX - rect.left,
        offsetY: e.clientY - rect.top
      };
      e.preventDefault();
    });

    win.addEventListener('mousedown', function () { focusWindow(id); });

    /* Track window */
    state.windows.push({
      id: id,
      title: options.title || 'Untitled',
      element: win
    });
    document.getElementById('desktop').appendChild(win);

    setTimeout(function () { win.classList.remove('opening'); }, 200);
    focusWindow(id);

    return {
      id: id,
      contentElement: contentArea,
      windowElement: win
    };
  }

  function closeWindow(id) {
    var winData = state.windows.find(function (w) { return w.id === id; });
    if (!winData) return;

    winData.element.classList.add('closing');
    setTimeout(function () {
      winData.element.remove();
      state.windows = state.windows.filter(function (w) { return w.id !== id; });
      if (state.activeWindow === id) {
        state.activeWindow = null;
        updateMenuBarAppName();
      }
    }, 150);
  }

  function focusWindow(id) {
    state.windows.forEach(function (w) { w.element.classList.remove('focused'); });

    var winData = state.windows.find(function (w) { return w.id === id; });
    if (winData) {
      winData.element.classList.add('focused');
      winData.element.style.zIndex = ++zCounter;
      state.activeWindow = id;
      updateMenuBarAppName();
    }
  }

  function updateMenuBarAppName() {
    var appNameEl = document.getElementById('menubar-appname');
    if (!appNameEl) return;

    if (!state.activeWindow) {
      appNameEl.textContent = 'Finder';
      return;
    }

    var winData = state.windows.find(function (w) {
      return w.id === state.activeWindow;
    });
    if (winData) {
      var t = winData.title;
      appNameEl.textContent = t.indexOf(' \u2014 ') !== -1
        ? t.split(' \u2014 ')[1]
        : t;
    }
  }


  /* \u2500\u2500\u2500 File Opening Dispatch \u2500\u2500\u2500 */

  function openFile(file) {
    if (file.type === 'folder') {
      openFinderAt(file);
      return;
    }

    var name = file.name || '';

    /* Auto-evidence for dont_open drafts */
    if (name.indexOf('untitled') === 0 &&
        !state.evidence.some(function (e) { return e.path.indexOf(name) !== -1; })) {
      addEvidence('dont_open/' + name, 'Unsent draft found');
    }

    /* Dispatch by extension */
    if (name.endsWith('.eml'))                    openEmlFile(file);
    else if (name.endsWith('.jpg') || name.endsWith('.png')) openImageFile(file);
    else if (name.endsWith('.log'))               openLogFile(file);
    else if (name.endsWith('.ics'))               openIcsFile(file);
    else if (name.endsWith('.pdf'))               openPdfFile(file);
    else if (file.content)                        openTxtFile(file);
    else                                          openGenericFile(file);
  }


  /* \u2500\u2500\u2500 Finder \u2500\u2500\u2500 */

  function openFinder() {
    var userFolder = FileSystem.root.children.Users.children['elena.marsh'];
    openFinderAt(userFolder);
  }

  function openFinderAt(folder) {
    if (folder.type !== 'folder') return;

    var sidebarItems = buildFinderSidebar();
    var result = createWindow({
      title: folder.name + ' \u2014 Finder',
      width: 780,
      height: 500,
      sidebar: sidebarItems
    });

    renderFileList(result.contentElement, folder);

    /* Sidebar navigation */
    result.contentElement.parentElement
      .querySelector('.finder-sidebar')
      .addEventListener('click', function (e) {
        var item = e.target.closest('.finder-sidebar-item');
        if (!item) return;
        var path = item.getAttribute('data-path');
        if (!path) return;
        var targetFolder = resolvePath(path);
        if (targetFolder && targetFolder.type === 'folder') {
          renderFileList(result.contentElement, targetFolder);
          var winData = state.windows.find(function (w) { return w.id === result.id; });
          if (winData) {
            winData.title = targetFolder.name + ' \u2014 Finder';
            winData.element.querySelector('.window-title').textContent = winData.title;
            updateMenuBarAppName();
          }
        }
      });
  }

  function buildFinderSidebar() {
    var items = [];
    items.push(el('div', {
      className: 'finder-sidebar-heading',
      textContent: 'Favorites'
    }));

    var favorites = [
      { name: 'Desktop',   path: 'Users/elena.marsh/Desktop',   icon: '\uD83D\uDDA5' },
      { name: 'Documents', path: 'Users/elena.marsh/Documents', icon: '\uD83D\uDCC4' },
      { name: 'Downloads', path: 'Users/elena.marsh/Downloads', icon: '\u2B07' },
      { name: 'Pictures',  path: 'Users/elena.marsh/Pictures',  icon: '\uD83D\uDDBC' },
      { name: 'dont_open', path: 'Users/elena.marsh/dont_open', icon: '\uD83D\uDD12' }
    ];

    favorites.forEach(function (fav) {
      var item = el('div', {
        className: 'finder-sidebar-item',
        'data-path': fav.path
      });
      item.appendChild(el('span', {
        className: 'finder-sidebar-icon',
        textContent: fav.icon
      }));
      item.appendChild(el('span', { textContent: fav.name }));
      items.push(item);
    });

    return items;
  }

  function resolvePath(path) {
    var parts = path.split('/');
    var current = FileSystem.root;
    for (var i = 0; i < parts.length; i++) {
      if (!current.children || !current.children[parts[i]]) return null;
      current = current.children[parts[i]];
    }
    return current;
  }

  function renderFileList(container, folder) {
    Viewers.renderFileList(
      container,
      folder,
      function (file) { openFile(file); },
      function (x, y, fileName, fldr) { showContextMenu(x, y, fileName, fldr); }
    );

    /* Special observation for dont_open */
    if (folder.name === 'dont_open') {
      var count = folder.children ? Object.keys(folder.children).length : 0;
      setTimeout(function () {
        showCursorNote(count + ' drafts in a folder she called "dont_open".');
        if (!state.evidence.some(function (e) { return e.note.indexOf('unsent drafts') !== -1; })) {
          addEvidence('dont_open/', count + ' unsent drafts found \u2014 possible goodbye letters');
        }
      }, 800);
    }
  }


  /* \u2500\u2500\u2500 Context Menu \u2500\u2500\u2500 */

  function showContextMenu(x, y, fileName, folder) {
    closeContextMenu();

    var menu = el('div', {
      className: 'context-menu',
      style: 'left:' + x + 'px;top:' + y + 'px;'
    });

    var openItem = el('div', {
      className: 'context-menu-item',
      textContent: 'Open'
    });
    openItem.addEventListener('click', function () {
      closeContextMenu();
      var f = findFileInFolder(fileName, folder);
      if (f) openFile(f);
    });
    menu.appendChild(openItem);

    menu.appendChild(el('div', { className: 'context-menu-separator' }));

    var tagItem = el('div', {
      className: 'context-menu-item',
      textContent: 'Tag as Evidence'
    });
    tagItem.addEventListener('click', function () {
      closeContextMenu();
      addEvidence(fileName, '(Tagged for review)');
      showCursorNote('Tagged: ' + fileName);
    });
    menu.appendChild(tagItem);

    menu.appendChild(el('div', { className: 'context-menu-separator' }));

    var infoItem = el('div', {
      className: 'context-menu-item',
      textContent: 'Get Info'
    });
    infoItem.addEventListener('click', function () {
      closeContextMenu();
      var f = findFileInFolder(fileName, folder);
      if (f) openFileInfo(f);
    });
    menu.appendChild(infoItem);

    document.body.appendChild(menu);

    /* Keep menu on screen */
    var rect = menu.getBoundingClientRect();
    if (rect.right > window.innerWidth)
      menu.style.left = (x - rect.width) + 'px';
    if (rect.bottom > window.innerHeight)
      menu.style.top = (y - rect.height) + 'px';
  }

  function closeContextMenu() {
    document.querySelectorAll('.context-menu').forEach(function (m) { m.remove(); });
  }

  function findFileInFolder(name, folder) {
    if (!folder || !folder.children) return null;
    return Object.values(folder.children).find(function (f) {
      return f.name === name;
    });
  }


  /* \u2500\u2500\u2500 File Viewers (dispatch to Viewers) \u2500\u2500\u2500 */

  function openTxtFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 TextEdit',
      width: 620, height: 460
    });
    Viewers.renderTextFile(result.contentElement, file);
  }

  function openEmlFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Mail',
      width: 640, height: 480
    });
    Viewers.renderEmailFile(result.contentElement, file);
  }

  function openImageFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Preview',
      width: 680, height: 520
    });
    Viewers.renderImage(result.contentElement, file);

    /* Special observations for key photos */
    if (file.name === 'IMG_1403.jpg') {
      setTimeout(function () {
        showCursorNote('Last photo. November 17. The table before dinner.');
        addEvidence(
          'Pictures/nov_17/' + file.name,
          'Last photo taken \u2014 table setting before dinner'
        );
      }, 1500);
    }

    if (file.name === 'IMG_1404.jpg') {
      setTimeout(function () {
        showCursorNote('Taken at 3:47 AM. The same time as the frozen clock. She\'s smiling.');
        addEvidence(
          'Pictures/nov_17/' + file.name,
          'Selfie timestamped 3:47 AM \u2014 matches frozen clock. Front-facing camera.'
        );
      }, 1500);
    }

    if (file.name && file.name.indexOf('mochi') !== -1) {
      setTimeout(function () {
        showCursorNote('She took a lot of pictures of her cat.');
      }, 2000);
    }
  }

  function openLogFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Console',
      width: 700, height: 460
    });
    Viewers.renderTerminal(result.contentElement, file);
  }

  function openIcsFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Calendar',
      width: 400, height: 280
    });
    Viewers.renderCalendarEvent(result.contentElement, file);
  }

  function openPdfFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Preview',
      width: 600, height: 450
    });
    Viewers.renderPDF(result.contentElement, file);
  }

  function openGenericFile(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Preview',
      width: 400, height: 300
    });
    Viewers.renderGeneric(result.contentElement, file);
  }

  function openFileInfo(file) {
    var result = createWindow({
      title: file.name + ' \u2014 Info',
      width: 380, height: 320
    });
    Viewers.renderFileInfo(result.contentElement, file);
  }


  /* \u2500\u2500\u2500 App Launchers \u2500\u2500\u2500 */

  function openBrowserHistory() {
    var result = createWindow({
      title: 'Browser History \u2014 Safari',
      width: 780, height: 540
    });
    Viewers.renderBrowserHistory(result.contentElement, FileSystem.browserHistory);
  }

  function openMail() {
    var result = createWindow({
      title: 'Inbox \u2014 Mail',
      width: 780, height: 540
    });
    Viewers.renderInbox(result.contentElement, FileSystem.emailInbox, function (email) {
      openEmailContent(email);
    });
  }

  function openEmailContent(email) {
    var result = createWindow({
      title: email.subject + ' \u2014 Mail',
      width: 640, height: 480
    });
    Viewers.renderEmailContent(result.contentElement, email);

    /* Auto-tag oncology emails */
    if (email.from && email.from.indexOf('schen@westside-oncology') !== -1) {
      if (!state.evidence.some(function (e) { return e.note.indexOf('oncology') !== -1; })) {
        setTimeout(function () {
          showCursorNote('Medical records. She was seeing an oncologist alone.');
          addEvidence('Mail > ' + email.subject, 'Medical correspondence \u2014 oncology');
        }, 1200);
      }
    }
  }

  function openCalendar() {
    var result = createWindow({
      title: 'Calendar \u2014 November 2023',
      width: 520, height: 520
    });
    Viewers.renderCalendar(result.contentElement, FileSystem.calendarEvents);
  }

  function openPhotos() {
    var result = createWindow({
      title: 'Photos',
      width: 700, height: 500
    });
    var allPhotos = Viewers.collectAllPhotos(FileSystem.root);
    Viewers.renderPhotosGrid(result.contentElement, allPhotos, function (photo) {
      openImageFile(photo);
    });
  }

  function openTextEditor() {
    var result = createWindow({
      title: 'Untitled \u2014 TextEdit',
      width: 560, height: 400
    });
    Viewers.renderTextEditor(result.contentElement);
  }

  function openTerminal() {
    var logFile = resolvePath('Library/Logs/system.log');
    var result = createWindow({
      title: 'Terminal',
      width: 700, height: 460
    });
    Viewers.renderTerminal(result.contentElement, logFile);
  }


  /* \u2500\u2500\u2500 Mira Voss Cursor Notes \u2500\u2500\u2500 */

  var cursorNoteEl    = null;
  var cursorNoteTimer = null;

  function showCursorNote(text) {
    if (!cursorNoteEl) {
      cursorNoteEl = el('div', {
        className: 'cursor-note',
        id: 'cursor-note'
      });
      document.body.appendChild(cursorNoteEl);
    }
    cursorNoteEl.textContent = text;
    cursorNoteEl.classList.add('visible');

    clearTimeout(cursorNoteTimer);
    cursorNoteTimer = setTimeout(function () {
      if (cursorNoteEl) cursorNoteEl.classList.remove('visible');
    }, 4500);
  }


  /* \u2500\u2500\u2500 Global Events \u2500\u2500\u2500 */

  function setupGlobalEvents() {
    /* Window dragging */
    document.addEventListener('mousemove', function (e) {
      if (state.dragState) {
        var win = document.getElementById(state.dragState.windowId);
        if (win) {
          win.style.left = Math.max(0, e.clientX - state.dragState.offsetX) + 'px';
          win.style.top  = Math.max(25, e.clientY - state.dragState.offsetY) + 'px';
        }
      }

      /* Cursor note follows pointer */
      if (cursorNoteEl && cursorNoteEl.classList.contains('visible')) {
        cursorNoteEl.style.left = (e.clientX + 16) + 'px';
        cursorNoteEl.style.top  = (e.clientY + 16) + 'px';
      }
    });

    document.addEventListener('mouseup', function () {
      state.dragState = null;
    });

    /* Click to dismiss */
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.context-menu')) closeContextMenu();

      if (!e.target.closest('.desktop-icon')) {
        document.querySelectorAll('.desktop-icon.selected').forEach(function (i) {
          i.classList.remove('selected');
        });
      }
    });

    /* Keyboard shortcuts */
    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'w') {
        e.preventDefault();
        if (state.activeWindow) closeWindow(state.activeWindow);
      }
    });

    /* Mira periodic observations */
    setupMiraObservations();
  }


  /* \u2500\u2500\u2500 Mira Voss AI \u2500\u2500\u2500 */

  function setupMiraObservations() {
    var openedCount = 0;

    var observations = [
      {
        trigger: function () { return openedCount >= 3; },
        message: 'Everything looks normal so far. Grocery lists. Work files.',
        used: false
      },
      {
        trigger: function () { return state.evidence.length >= 2; },
        message: 'Starting to build a picture. Tag everything.',
        used: false
      },
      {
        trigger: function () { return state.windows.length >= 4; },
        message: 'Multiple windows open. She was working on something.',
        used: false
      },
      {
        trigger: function () { return openedCount >= 8; },
        message: 'The deeper you go, the less normal it gets.',
        used: false
      },
      {
        trigger: function () { return state.evidence.length >= 5; },
        message: 'Enough evidence. The story is starting to come together.',
        used: false
      }
    ];

    setInterval(function () {
      observations.forEach(function (obs) {
        if (!obs.used && obs.trigger()) {
          obs.used = true;
          showCursorNote(obs.message);
        }
      });
    }, 5000);

    document.addEventListener('dblclick', function () { openedCount++; });
  }


  /* \u2500\u2500\u2500 Boot \u2500\u2500\u2500 */

  function boot() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', showIntro);
    } else {
      showIntro();
    }
  }

  boot();


  /* \u2500\u2500\u2500 Public API (for Viewers callbacks) \u2500\u2500\u2500 */

  return {
    addEvidence:   addEvidence,
    showCursorNote: showCursorNote
  };

})();
