/**
 * viewer.js \u2014 Content rendering for Soft Estate
 *
 * All display logic for file types: text, email, images,
 * browser history, calendar, terminal, PDF, generic.
 *
 * Depends on: FileSystem (global), Desktop (global, post-boot)
 */

var Viewers = (function () {
  'use strict';

  /* \u2500\u2500\u2500 Utilities \u2500\u2500\u2500 */

  var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun',
                'Jul','Aug','Sep','Oct','Nov','Dec'];

  function formatDate(iso) {
    if (!iso) return '\u2014';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '\u2014';
    return MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear();
  }

  function formatTime(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    var h = d.getHours();
    var m = String(d.getMinutes()).padStart(2, '0');
    var ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12 || 12;
    return h + ':' + m + ' ' + ampm;
  }

  function shortDate(iso) {
    if (!iso) return '\u2014';
    return formatDate(iso) + ', ' + formatTime(iso);
  }

  function formatSize(bytes) {
    if (!bytes) return '\u2014';
    if (bytes < 1024)              return bytes + ' B';
    if (bytes < 1024 * 1024)       return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  function escapeHtml(str) {
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'className')    e.className = attrs[k];
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

  var calendarColors = {
    red: '#ff3b30', blue: '#007aff', orange: '#ff9500',
    purple: '#af52de', green: '#34c759', yellow: '#ffcc00'
  };


  /* \u2500\u2500\u2500 SVG Icons \u2500\u2500\u2500 */

  var ICONS = {
    folder:
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M4 16C4 13.79 5.79 12 8 12H24L28 16H56C58.21 16 60 17.79 60 20V50C60 52.21 58.21 54 56 54H8C5.79 54 4 52.21 4 50V16Z" fill="#42a5f5"/>' +
      '<path d="M4 22H60V50C60 52.21 58.21 54 56 54H8C5.79 54 4 52.21 4 50V22Z" fill="#64b5f6"/>' +
      '</svg>',

    'folder-smart':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M4 16C4 13.79 5.79 12 8 12H24L28 16H56C58.21 16 60 17.79 60 20V50C60 52.21 58.21 54 56 54H8C5.79 54 4 52.21 4 50V16Z" fill="#78909c"/>' +
      '<path d="M4 22H60V50C60 52.21 58.21 54 56 54H8C5.79 54 4 52.21 4 50V22Z" fill="#90a4ae"/>' +
      '</svg>',

    'file-txt':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '<rect x="18" y="28" width="24" height="2" rx="1" fill="#bbb"/>' +
      '<rect x="18" y="34" width="20" height="2" rx="1" fill="#ccc"/>' +
      '<rect x="18" y="40" width="22" height="2" rx="1" fill="#ccc"/>' +
      '</svg>',

    'file-pdf':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#ef5350" stroke="#c62828" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#c62828"/>' +
      '<text x="32" y="44" text-anchor="middle" fill="white" font-size="14" font-weight="600" font-family="sans-serif">PDF</text>' +
      '</svg>',

    'file-email':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '<rect x="16" y="26" width="28" height="20" rx="2" fill="#42a5f5"/>' +
      '<path d="M16 28L30 38L44 28" stroke="white" stroke-width="1.5" fill="none"/>' +
      '</svg>',

    'file-image':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '<rect x="16" y="28" width="28" height="20" rx="2" fill="#66bb6a"/>' +
      '<circle cx="24" cy="35" r="3" fill="#ffeb3b"/>' +
      '<path d="M16 46L26 38L34 44L40 38L44 44V46C44 47.1 43.1 48 42 48H18C16.9 48 16 47.1 16 46Z" fill="#388e3c"/>' +
      '</svg>',

    'file-log':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '<text x="32" y="44" text-anchor="middle" fill="#888" font-size="8" font-weight="500" font-family="monospace">LOG</text>' +
      '</svg>',

    'file-cal':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '<rect x="16" y="24" width="28" height="24" rx="2" fill="#fff" stroke="#ddd"/>' +
      '<rect x="16" y="24" width="28" height="8" rx="2" fill="#ff3b30"/>' +
      '<text x="32" y="30.5" text-anchor="middle" fill="white" font-size="6" font-weight="600" font-family="sans-serif">NOV</text>' +
      '<text x="32" y="44" text-anchor="middle" fill="#333" font-size="14" font-weight="700" font-family="sans-serif">17</text>' +
      '</svg>',

    'file-spreadsheet':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '<rect x="16" y="26" width="28" height="20" rx="1" fill="#4caf50"/>' +
      '<line x1="26" y1="26" x2="26" y2="46" stroke="white" stroke-width="0.5" opacity="0.5"/>' +
      '<line x1="36" y1="26" x2="36" y2="46" stroke="white" stroke-width="0.5" opacity="0.5"/>' +
      '<line x1="16" y1="34" x2="44" y2="34" stroke="white" stroke-width="0.5" opacity="0.5"/>' +
      '</svg>',

    'file-generic':
      '<svg viewBox="0 0 64 64" fill="none">' +
      '<path d="M14 6H40L50 18V56C50 58.21 48.21 60 46 60H14C11.79 60 10 58.21 10 56V10C10 7.79 11.79 6 14 6Z" fill="#f5f5f5" stroke="#ccc" stroke-width="0.5"/>' +
      '<path d="M40 6L50 18H42C40.9 18 40 17.1 40 16V6Z" fill="#e0e0e0"/>' +
      '</svg>'
  };

  function getFileIcon(file) {
    if (file.icon && ICONS[file.icon]) return ICONS[file.icon];
    if (file.type === 'folder') return ICONS.folder;
    var name = file.name || '';
    if (name.endsWith('.txt'))                  return ICONS['file-txt'];
    if (name.endsWith('.pdf'))                  return ICONS['file-pdf'];
    if (name.endsWith('.eml'))                  return ICONS['file-email'];
    if (name.endsWith('.jpg') || name.endsWith('.png')) return ICONS['file-image'];
    if (name.endsWith('.log'))                  return ICONS['file-log'];
    if (name.endsWith('.ics'))                  return ICONS['file-cal'];
    if (name.endsWith('.xlsx'))                 return ICONS['file-spreadsheet'];
    return ICONS['file-generic'];
  }


  /* \u2500\u2500\u2500 File List Rendering \u2500\u2500\u2500 */

  function renderFileList(container, folder, openCallback, contextCallback) {
    container.innerHTML = '';

    var isDontOpen = (folder.name === 'dont_open');
    var header = el('div', { className: 'file-list-header' });
    header.appendChild(el('span', { textContent: 'Name' }));
    header.appendChild(el('span', { textContent: 'Date Modified' }));
    header.appendChild(el('span', { textContent: 'Size' }));
    container.appendChild(header);

    var list = el('div', {
      className: 'file-list' + (isDontOpen ? ' dont-open' : '')
    });

    var children = folder.children
      ? Object.values(folder.children)
      : [];

    /* Sort: folders first, then alphabetical */
    children.sort(function (a, b) {
      if (a.type === 'folder' && b.type !== 'folder') return -1;
      if (a.type !== 'folder' && b.type === 'folder') return 1;
      return (a.name || '').localeCompare(b.name || '');
    });

    children.forEach(function (file) {
      var row = el('div', { className: 'file-item' });

      /* Name cell */
      var nameCell = el('div', { className: 'file-name' });
      nameCell.appendChild(el('span', {
        className: 'file-icon',
        innerHTML: getFileIcon(file)
      }));
      nameCell.appendChild(el('span', { textContent: file.name }));
      row.appendChild(nameCell);

      /* Date */
      row.appendChild(el('span', {
        className: 'file-date',
        textContent: file.type === 'folder'
          ? '\u2014'
          : formatDate(file.modified)
      }));

      /* Size */
      row.appendChild(el('span', {
        className: 'file-size',
        textContent: file.type === 'folder'
          ? '\u2014'
          : formatSize(file.size)
      }));

      /* Double-click to open */
      row.addEventListener('dblclick', function () {
        if (openCallback) openCallback(file);
      });

      /* Single-click to select */
      row.addEventListener('click', function (e) {
        e.stopPropagation();
        list.querySelectorAll('.file-item').forEach(function (r) {
          r.classList.remove('selected');
        });
        row.classList.add('selected');
      });

      /* Context menu */
      row.addEventListener('contextmenu', function (e) {
        e.preventDefault();
        e.stopPropagation();
        list.querySelectorAll('.file-item').forEach(function (r) {
          r.classList.remove('selected');
        });
        row.classList.add('selected');
        if (contextCallback) {
          contextCallback(e.clientX, e.clientY, file.name, folder);
        }
      });

      list.appendChild(row);
    });

    container.appendChild(list);
  }


  /* \u2500\u2500\u2500 Text File \u2500\u2500\u2500 */

  function renderTextFile(container, file) {
    var viewer = el('div', { className: 'text-viewer' });
    var content = file.content || '';

    /* Visual cue for the dont_open drafts */
    if (file.name && file.name.indexOf('untitled') === 0) {
      viewer.style.background = '#fffdf8';
      viewer.style.borderLeft = '3px solid rgba(255, 59, 48, 0.15)';
    }

    viewer.textContent = content;

    if (file.name && file.name.indexOf('untitled') === 0 && content) {
      var wordCount = content.trim().split(/\s+/).length;
      var lineCount = content.split('\n').length;
      viewer.appendChild(el('div', {
        style: 'margin-top:16px;padding-top:8px;border-top:1px solid #eee;' +
               'font-size:10px;color:#bbb;',
        textContent: lineCount + ' lines \u00b7 ' + wordCount + ' words \u00b7 Modified ' + shortDate(file.modified)
      }));
    }

    container.appendChild(viewer);
  }


  /* \u2500\u2500\u2500 Email File (.eml) \u2500\u2500\u2500 */

  function renderEmailFile(container, file) {
    var viewer = el('div', { className: 'text-viewer email-viewer' });
    var content = file.content || '';
    var lines = content.split('\n');

    var header = el('div', { className: 'email-header' });
    var bodyStarted = false;
    var bodyLines = [];

    lines.forEach(function (line) {
      if (!bodyStarted) {
        if (line.indexOf('From: ') === 0)
          header.appendChild(el('div', { className: 'email-from', textContent: line }));
        else if (line.indexOf('Subject: ') === 0)
          header.appendChild(el('div', {
            className: 'email-subject',
            textContent: line.replace('Subject: ', '')
          }));
        else if (line.indexOf('Date: ') === 0)
          header.appendChild(el('div', {
            className: 'email-date',
            textContent: line.replace('Date: ', '')
          }));
        else if (line.indexOf('To: ') === 0)
          header.appendChild(el('div', {
            style: 'font-size:12px;color:#666;margin-top:2px;',
            textContent: line
          }));
        else if (line.trim() === '' && header.children.length > 0)
          bodyStarted = true;
      } else {
        bodyLines.push(line);
      }
    });

    viewer.appendChild(header);
    viewer.appendChild(el('div', {
      style: 'white-space:pre-wrap;font-size:13px;line-height:1.6;margin-top:12px;',
      textContent: bodyLines.join('\n').trim()
    }));

    container.appendChild(viewer);
  }


  /* \u2500\u2500\u2500 Email Inbox \u2500\u2500\u2500 */

  function renderInbox(container, inbox, openCallback) {
    var sorted = (inbox || []).slice().sort(function (a, b) {
      return new Date(b.date) - new Date(a.date);
    });

    var listHeader = el('div', {
      style: 'padding:10px 14px;background:#f0f0f0;border-bottom:0.5px solid #ccc;' +
             'display:flex;justify-content:space-between;align-items:center;'
    });
    listHeader.appendChild(el('span', {
      style: 'font-weight:600;font-size:12px;',
      textContent: 'Inbox'
    }));
    listHeader.appendChild(el('span', {
      style: 'font-size:11px;color:#888;',
      textContent: sorted.length + ' messages'
    }));
    container.appendChild(listHeader);

    var list = el('div', {
      className: 'file-list',
      style: 'padding:0;'
    });

    sorted.forEach(function (email) {
      var row = el('div', {
        className: 'file-item',
        style: 'grid-template-columns:minmax(200px,1fr) 140px 40px;' +
               'padding:8px 12px;cursor:default;' +
               'border-bottom:0.5px solid rgba(0,0,0,0.04);'
      });

      var nameCell = el('div', { className: 'file-name' });
      nameCell.appendChild(el('span', {
        className: 'file-icon',
        innerHTML: ICONS['file-email']
      }));

      var infoDiv = el('div', {
        style: 'display:flex;flex-direction:column;min-width:0;'
      });
      infoDiv.appendChild(el('span', {
        style: 'font-size:12px;font-weight:' + (email.read ? '400' : '600') +
               ';white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
        textContent: email.subject
      }));
      var fromName = email.from || '';
      if (fromName.indexOf('<') !== -1)
        fromName = fromName.split('<')[0].trim();
      infoDiv.appendChild(el('span', {
        style: 'font-size:11px;color:#999;white-space:nowrap;overflow:hidden;' +
               'text-overflow:ellipsis;',
        textContent: fromName
      }));

      nameCell.appendChild(infoDiv);
      row.appendChild(nameCell);
      row.appendChild(el('span', {
        className: 'file-date',
        textContent: shortDate(email.date)
      }));
      row.appendChild(el('span', {
        style: 'font-size:14px;text-align:center;color:' +
               (email.starred ? '#ffcc00' : 'transparent') + ';',
        textContent: '\u2605'
      }));

      row.addEventListener('dblclick', function () {
        if (openCallback) openCallback(email);
      });

      row.addEventListener('click', function (e) {
        e.stopPropagation();
        list.querySelectorAll('.file-item').forEach(function (r) {
          r.classList.remove('selected');
        });
        row.classList.add('selected');
      });

      list.appendChild(row);
    });

    container.appendChild(list);
  }


  /* \u2500\u2500\u2500 Email Content \u2500\u2500\u2500 */

  function renderEmailContent(container, email) {
    var viewer = el('div', { className: 'text-viewer email-viewer' });

    var header = el('div', { className: 'email-header' });
    header.appendChild(el('div', {
      className: 'email-subject',
      textContent: email.subject
    }));
    header.appendChild(el('div', {
      className: 'email-from',
      style: 'margin-top:6px;',
      textContent: 'From: ' + email.from
    }));
    header.appendChild(el('div', {
      style: 'font-size:12px;color:#666;margin-top:2px;',
      textContent: 'To: ' + email.to
    }));
    header.appendChild(el('div', {
      className: 'email-date',
      textContent: formatDate(email.date) + ' at ' + formatTime(email.date)
    }));
    viewer.appendChild(header);

    viewer.appendChild(el('div', {
      style: 'white-space:pre-wrap;font-size:13px;line-height:1.6;margin-top:16px;',
      textContent: email.body
    }));

    container.appendChild(viewer);
  }


  /* \u2500\u2500\u2500 Image \u2500\u2500\u2500 */

  function renderImage(container, file) {
    var viewer = el('div', { className: 'image-viewer' });
    var imgContainer = el('div', { className: 'image-container' });

    var seed = (file.name || '').replace(/[^a-zA-Z0-9]/g, '');
    imgContainer.appendChild(el('img', {
      src: 'https://picsum.photos/seed/' + seed + '/800/600.jpg',
      alt: file.name,
      style: 'border-radius:2px;max-width:100%;max-height:100%;object-fit:contain;'
    }));

    /* Description overlay */
    if (file.metadata && file.metadata.description) {
      var overlay = el('div', { className: 'photo-metadata' });
      overlay.appendChild(el('div', {
        className: 'photo-metadata-title',
        textContent: file.metadata.description
      }));
      if (file.metadata.exif) {
        var parts = [];
        if (file.metadata.exif.dateTimeOriginal)
          parts.push(formatDate(file.metadata.exif.dateTimeOriginal));
        if (file.metadata.exif.location)
          parts.push(file.metadata.exif.location);
        if (parts.length)
          overlay.appendChild(el('div', {
            className: 'photo-metadata-exif',
            textContent: parts.join(' \u00b7 ')
          }));
      }
      imgContainer.appendChild(overlay);
    }

    viewer.appendChild(imgContainer);

    /* Info bar */
    var infoBar = el('div', { className: 'image-info-bar' });
    if (file.metadata && file.metadata.description) {
      infoBar.appendChild(el('span', {
        className: 'image-info-description',
        textContent: file.metadata.description
      }));
    } else {
      infoBar.appendChild(el('span', { textContent: file.name }));
    }

    var exifDiv = el('div', { className: 'image-exif' });
    if (file.metadata) {
      if (file.metadata.camera)
        exifDiv.appendChild(el('span', { textContent: file.metadata.camera }));
      if (file.metadata.exif) {
        if (file.metadata.exif.location)
          exifDiv.appendChild(el('span', { textContent: file.metadata.exif.location }));
        if (file.metadata.exif.dateTimeOriginal)
          exifDiv.appendChild(el('span', { textContent: formatTime(file.metadata.exif.dateTimeOriginal) }));
      }
      exifDiv.appendChild(el('span', { textContent: formatSize(file.size) }));
    }
    infoBar.appendChild(exifDiv);
    viewer.appendChild(infoBar);
    container.appendChild(viewer);
  }


  /* \u2500\u2500\u2500 Browser History \u2500\u2500\u2500 */

  function renderBrowserHistory(container, history) {
    var timeline = el('div', { className: 'history-timeline' });

    /* Search bar */
    var searchBar = el('div', {
      style: 'padding:8px 0 12px;border-bottom:1px solid var(--border-window);' +
             'margin-bottom:8px;display:flex;gap:8px;align-items:center;'
    });
    var searchInput = el('input', {
      type: 'text',
      placeholder: 'Search history\u2026',
      style: 'flex:1;border:0.5px solid #ccc;border-radius:4px;padding:5px 10px;' +
             'font-size:12px;outline:none;background:#fff;',
      id: 'history-search'
    });
    searchBar.appendChild(searchInput);
    searchBar.appendChild(el('span', {
      style: 'font-size:11px;color:#999;',
      textContent: (history || []).length + ' entries'
    }));
    timeline.appendChild(searchBar);

    /* Group by date */
    var groups = {};
    (history || []).forEach(function (entry) {
      var dk = formatDate(entry.date);
      if (!groups[dk]) groups[dk] = [];
      groups[dk].push(entry);
    });

    var hasTerminalSearch = false;
    var hasDyingSearch = false;

    Object.keys(groups).sort().reverse().forEach(function (dk) {
      timeline.appendChild(el('div', { className: 'history-date', textContent: dk }));

      groups[dk].forEach(function (entry) {
        var title = (entry.title || '').toLowerCase();
        var url   = (entry.url   || '').toLowerCase();

        if (title.indexOf('terminal') !== -1 || title.indexOf('dying') !== -1)
          hasTerminalSearch = true;
        if (title.indexOf('how to tell') !== -1 || title.indexOf('letter to family') !== -1)
          hasDyingSearch = true;

        var row = el('div', { className: 'history-entry' });
        row.appendChild(el('span', {
          className: 'history-time',
          textContent: formatTime(entry.date)
        }));

        var isConcerning =
          url.indexOf('cancer')   !== -1 ||
          url.indexOf('hospice')  !== -1 ||
          title.indexOf('dying')  !== -1 ||
          title.indexOf('terminal') !== -1 ||
          title.indexOf('body')   !== -1 ||
          title.indexOf('belongs') !== -1;

        /* Favicon colour */
        var faviconColor = '#999';
        if      (url.indexOf('google')    !== -1) faviconColor = '#4285f4';
        else if (url.indexOf('reddit')    !== -1) faviconColor = '#ff4500';
        else if (url.indexOf('youtube')   !== -1) faviconColor = '#ff0000';
        else if (url.indexOf('cancer')    !== -1 ||
                 url.indexOf('webmd')     !== -1 ||
                 url.indexOf('mayoclinic') !== -1) faviconColor = '#ff3b30';
        else if (url.indexOf('hospice')   !== -1) faviconColor = '#8e24aa';
        else if (url.indexOf('amazon')    !== -1) faviconColor = '#ff9900';
        else if (url.indexOf('etsy')      !== -1) faviconColor = '#f56400';
        else if (url.indexOf('netflix')   !== -1) faviconColor = '#e50914';

        row.appendChild(el('div', {
          className: 'history-favicon',
          style: 'background:' + faviconColor + ';'
        }));

        var info = el('div', { className: 'history-info' });
        info.appendChild(el('div', {
          className: 'history-title' + (isConcerning ? ' concerning' : ''),
          textContent: entry.title || entry.url
        }));
        info.appendChild(el('div', {
          className: 'history-url',
          textContent: entry.url
        }));
        row.appendChild(info);
        timeline.appendChild(row);
      });
    });

    /* Search filtering */
    searchInput.addEventListener('input', function () {
      var q = searchInput.value.toLowerCase();
      var entries = timeline.querySelectorAll('.history-entry');
      var dates   = timeline.querySelectorAll('.history-date');

      entries.forEach(function (e) {
        e.style.display =
          e.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
      });

      dates.forEach(function (dh) {
        var next = dh.nextElementSibling;
        var hasVisible = false;
        while (next && !next.classList.contains('history-date')) {
          if (next.style.display !== 'none') hasVisible = true;
          next = next.nextElementSibling;
        }
        dh.style.display = hasVisible ? '' : 'none';
      });
    });

    container.appendChild(timeline);

    /* Delayed forensic observation */
    setTimeout(function () {
      if (hasTerminalSearch && Desktop) {
        Desktop.addEvidence(
          'Safari > History',
          'Search queries indicate awareness of terminal prognosis'
        );
      }
    }, 2000);
  }


  /* \u2500\u2500\u2500 Calendar \u2500\u2500\u2500 */

  function renderCalendar(container, events) {
    var view = el('div', { className: 'calendar-view' });

    view.appendChild(el('div', {
      style: 'text-align:center;font-size:17px;font-weight:600;margin-bottom:16px;' +
             'padding-bottom:8px;border-bottom:1px solid var(--border-window);',
      textContent: 'November 2023'
    }));

    /* Day-of-week header */
    var weekRow = el('div', { className: 'calendar-grid-header' });
    ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].forEach(function (d) {
      weekRow.appendChild(el('span', { textContent: d }));
    });
    view.appendChild(weekRow);

    /* Grid \u2014 November 2023 starts on Wednesday (index 3) */
    var grid = el('div', { className: 'calendar-grid' });
    for (var pad = 0; pad < 3; pad++) {
      grid.appendChild(el('div', {
        className: 'calendar-cell',
        style: 'color:#ccc;',
        textContent: ''
      }));
    }

    var eventDates = {};
    (events || []).forEach(function (evt) {
      var d = new Date(evt.date);
      var dayNum = d.getDate();
      if (!eventDates[dayNum]) eventDates[dayNum] = [];
      eventDates[dayNum].push(evt);
    });

    for (var day = 1; day <= 30; day++) {
      var cell = el('div', {
        className: 'calendar-cell' +
          (day === 18 ? ' today' : (day <= 17 ? ' past' : ' future'))
      });
      cell.textContent = String(day);

      if (eventDates[day]) {
        var dotRow = el('div', { className: 'calendar-dot-row' });
        eventDates[day].forEach(function (evt) {
          dotRow.appendChild(el('div', {
            className: 'calendar-dot',
            style: 'background:' + (calendarColors[evt.color] || '#888') + ';'
          }));
        });
        cell.appendChild(dotRow);
      }

      grid.appendChild(cell);
    }
    view.appendChild(grid);

    /* Events list */
    view.appendChild(el('div', {
      style: 'font-size:12px;font-weight:600;color:#666;margin-bottom:10px;' +
             'text-transform:uppercase;letter-spacing:0.03em;',
      textContent: 'Upcoming Events'
    }));

    (events || []).forEach(function (event) {
      var evtEl = el('div', { className: 'calendar-event' });
      var isFuture = new Date(event.date) > new Date('2023-11-18');
      if (isFuture) evtEl.style.borderLeft = '3px solid rgba(255, 59, 48, 0.3)';

      evtEl.appendChild(el('div', {
        className: 'calendar-color-dot',
        style: 'background:' + (calendarColors[event.color] || '#888') + ';'
      }));

      var info = el('div', { className: 'calendar-event-info' });
      info.appendChild(el('div', {
        className: 'calendar-event-title',
        textContent: event.title
      }));

      var dateStr = event.date.length > 10
        ? formatDate(event.date) + ' at ' + formatTime(event.date)
        : formatDate(event.date);
      info.appendChild(el('div', {
        className: 'calendar-event-date',
        textContent: dateStr
      }));

      if (event.notes) {
        info.appendChild(el('div', {
          className: 'calendar-event-notes',
          textContent: event.notes
        }));
      }

      evtEl.appendChild(info);
      view.appendChild(evtEl);
    });

    container.appendChild(view);

    /* Delayed observation */
    setTimeout(function () {
      var futureCount = (events || []).filter(function (e) {
        return new Date(e.date) > new Date('2023-11-18');
      }).length;

      if (futureCount > 0 && Desktop) {
        Desktop.showCursorNote(
          'She made plans. Dentist, Thanksgiving, Christmas. All the way through December.'
        );
        Desktop.addEvidence(
          'Calendar',
          'Future events scheduled \u2014 suggests no expectation of imminent death on Nov 17'
        );
      }
    }, 3000);
  }


  /* \u2500\u2500\u2500 Calendar Event (.ics) \u2500\u2500\u2500 */

  function renderCalendarEvent(container, file) {
    var viewer = el('div', {
      style: 'padding:24px;background:#fff;min-height:100%;'
    });
    var content = file.content || '';
    var summary = '', location = '', description = '';

    content.split('\n').forEach(function (line) {
      if (line.indexOf('SUMMARY:')     === 0) summary     = line.replace('SUMMARY:', '');
      if (line.indexOf('LOCATION:')    === 0) location    = line.replace('LOCATION:', '');
      if (line.indexOf('DESCRIPTION:') === 0) description = line.replace('DESCRIPTION:', '');
    });

    var card = el('div', {
      style: 'border-left:4px solid #ff3b30;padding-left:16px;margin-bottom:20px;'
    });
    card.appendChild(el('div', {
      style: 'font-size:17px;font-weight:600;',
      textContent: summary || 'Event'
    }));
    if (location)
      card.appendChild(el('div', {
        style: 'font-size:12px;color:#666;margin-top:4px;',
        textContent: location
      }));
    if (description)
      card.appendChild(el('div', {
        style: 'font-size:12px;color:#888;margin-top:8px;line-height:1.5;',
        textContent: description
      }));
    viewer.appendChild(card);

    viewer.appendChild(el('pre', {
      style: 'font-size:10px;color:#ccc;font-family:var(--font-mono);' +
             'white-space:pre-wrap;margin-top:16px;padding-top:8px;' +
             'border-top:1px solid #eee;',
      textContent: content
    }));

    container.appendChild(viewer);
  }


  /* \u2500\u2500\u2500 Terminal / System Log \u2500\u2500\u2500 */

  function renderTerminal(container, logFile) {
    var terminal = el('div', { className: 'terminal-body' });

    terminal.appendChild(el('div', {
      style: 'color:#888;margin-bottom:8px;',
      textContent: 'Last login: Sat Nov 18 03:43:09 on ttys000'
    }));

    var cmdLine = el('div', { style: 'margin-bottom:4px;' });
    cmdLine.appendChild(el('span', {
      className: 'terminal-path',
      textContent: 'elena-marsh-macbook:~ elena.marsh$ '
    }));
    cmdLine.appendChild(el('span', {
      style: 'color:#fff;',
      textContent: 'tail -40 /var/log/system.log'
    }));
    terminal.appendChild(cmdLine);

    if (logFile && logFile.content) {
      logFile.content.split('\n').forEach(function (line) {
        var color   = '#4caf50';
        var opacity = '0.85';

        if (line.indexOf('*** SYSTEM CLOCK HALTED ***') !== -1) {
          color = '#ff3b30'; opacity = '1';
        } else if (line.indexOf('END OF LOG') !== -1) {
          color = '#ff9500'; opacity = '1';
        } else if (line.indexOf('Safari') !== -1 && line.indexOf('Navigation') !== -1) {
          color = '#42a5f5';
        } else if (line.indexOf('TextEdit') !== -1) {
          color = '#ffcc00';
        } else if (line.indexOf('Memory') !== -1 || line.indexOf('memory') !== -1) {
          color = '#ff9500';
        } else if (line.indexOf('Session ended') !== -1 || line.indexOf('terminated') !== -1) {
          color = '#888';
        }

        terminal.appendChild(el('div', {
          style: 'color:' + color + ';opacity:' + opacity +
                 ';font-size:11px;line-height:1.45;',
          textContent: line
        }));
      });
    }

    /* Prompt with blinking cursor */
    var promptLine = el('div', { style: 'margin-top:8px;' });
    promptLine.appendChild(el('span', {
      className: 'terminal-path',
      textContent: 'elena-marsh-macbook:~ elena.marsh$ '
    }));
    promptLine.appendChild(el('span', { className: 'terminal-cursor' }));
    terminal.appendChild(promptLine);

    container.appendChild(terminal);
    container.scrollTop = container.scrollHeight;

    setTimeout(function () {
      if (Desktop) {
        Desktop.addEvidence(
          'Library/Logs/system.log',
          'System log shows activity timeline \u2014 last action at 3:43 AM'
        );
      }
    }, 2500);
  }


  /* \u2500\u2500\u2500 PDF \u2500\u2500\u2500 */

  function renderPDF(container, file) {
    var pdfView = el('div', {
      style: 'background:#fff;padding:40px;min-height:100%;' +
             'display:flex;flex-direction:column;align-items:center;justify-content:center;'
    });

    pdfView.appendChild(el('div', {
      innerHTML: ICONS['file-pdf'],
      style: 'width:80px;height:80px;margin-bottom:20px;opacity:0.4;'
    }));

    if (file.metadata) {
      pdfView.appendChild(el('div', {
        style: 'font-size:15px;font-weight:600;margin-bottom:12px;text-align:center;' +
               'max-width:400px;line-height:1.4;',
        textContent: file.metadata.title || file.name
      }));

      var meta = el('div', {
        style: 'font-size:12px;color:#666;line-height:2;text-align:left;' +
               'max-width:360px;width:100%;'
      });

      var fields = [
        ['Author',     file.metadata.author],
        ['Pages',      file.metadata.pages ? String(file.metadata.pages) : null],
        ['Signed',     file.metadata.signedDate],
        ['Value',      file.metadata.totalValue],
        ['Status',     file.metadata.status,
                       file.metadata.status === 'PAID' ? '#34c759' : null],
        ['Paid',       file.metadata.paidDate],
        ['Amount',     file.metadata.amount],
        ['Rent',       file.metadata.monthlyRent],
        ['New Rent',   file.metadata.newRent, '#ff3b30'],
        ['Term',       file.metadata.termStart
                       ? (file.metadata.termStart + ' \u2014 ' + (file.metadata.termEnd || ''))
                       : null],
        ['Address',    file.metadata.address]
      ];

      fields.forEach(function (f) {
        if (f[1]) {
          var row = el('div', {
            style: 'display:flex;justify-content:space-between;' +
                   'border-bottom:0.5px solid #f0f0f0;padding:2px 0;'
          });
          row.appendChild(el('span', {
            style: 'color:#999;',
            textContent: f[0]
          }));
          var valStyle = 'font-weight:500;';
          if (f[2]) valStyle += 'color:' + f[2] + ';';
          row.appendChild(el('span', {
            style: valStyle,
            textContent: String(f[1])
          }));
          meta.appendChild(row);
        }
      });
      pdfView.appendChild(meta);

      if (file.metadata.notes) {
        pdfView.appendChild(el('div', {
          style: 'margin-top:12px;font-size:11px;color:#999;font-style:italic;text-align:center;',
          textContent: file.metadata.notes
        }));
      }
    } else {
      pdfView.appendChild(el('div', {
        style: 'font-size:13px;color:#888;',
        textContent: 'PDF document \u2014 content not available in forensic viewer'
      }));
    }

    pdfView.appendChild(el('div', {
      style: 'font-size:11px;color:#bbb;margin-top:20px;padding-top:12px;border-top:1px solid #eee;',
      textContent: formatSize(file.size) + ' \u00b7 Modified ' + shortDate(file.modified)
    }));

    container.appendChild(pdfView);
  }


  /* \u2500\u2500\u2500 Generic File \u2500\u2500\u2500 */

  function renderGeneric(container, file) {
    var placeholder = el('div', {
      style: 'display:flex;flex-direction:column;align-items:center;' +
             'justify-content:center;height:100%;background:#fff;padding:40px;'
    });
    placeholder.appendChild(el('div', {
      innerHTML: getFileIcon(file),
      style: 'width:64px;height:64px;opacity:0.4;margin-bottom:16px;'
    }));
    placeholder.appendChild(el('div', {
      style: 'font-size:14px;font-weight:500;margin-bottom:6px;',
      textContent: file.name
    }));
    placeholder.appendChild(el('div', {
      style: 'font-size:12px;color:#999;',
      textContent: formatSize(file.size) + ' \u00b7 ' + shortDate(file.modified)
    }));
    if (file.metadata && file.metadata.notes) {
      placeholder.appendChild(el('div', {
        style: 'font-size:11px;color:#bbb;margin-top:8px;font-style:italic;',
        textContent: file.metadata.notes
      }));
    }
    container.appendChild(placeholder);
  }


  /* \u2500\u2500\u2500 File Info \u2500\u2500\u2500 */

  function renderFileInfo(container, file) {
    var viewer = el('div', {
      style: 'padding:20px 24px;font-size:12px;line-height:1.8;background:#fff;min-height:100%;'
    });

    var header = el('div', {
      style: 'display:flex;align-items:center;gap:12px;margin-bottom:16px;' +
             'padding-bottom:12px;border-bottom:1px solid #eee;'
    });
    header.appendChild(el('div', {
      innerHTML: getFileIcon(file),
      style: 'width:48px;height:48px;'
    }));
    var nameDiv = el('div');
    nameDiv.appendChild(el('div', {
      style: 'font-size:14px;font-weight:600;',
      textContent: file.name
    }));
    nameDiv.appendChild(el('div', {
      style: 'font-size:11px;color:#999;',
      textContent: file.type === 'folder'
        ? 'Folder'
        : (file.name || '').split('.').pop().toUpperCase() + ' File'
    }));
    header.appendChild(nameDiv);
    viewer.appendChild(header);

    if (file.size)
      viewer.appendChild(makeInfoRow('Size', formatSize(file.size)));
    if (file.modified)
      viewer.appendChild(makeInfoRow('Modified', shortDate(file.modified)));
    if (file.type === 'folder' && file.children)
      viewer.appendChild(makeInfoRow('Contains', Object.keys(file.children).length + ' items'));

    if (file.metadata) {
      viewer.appendChild(el('div', {
        style: 'margin-top:12px;font-size:11px;font-weight:600;color:#999;' +
               'text-transform:uppercase;letter-spacing:0.03em;',
        textContent: 'Details'
      }));
      Object.keys(file.metadata).forEach(function (k) {
        if (typeof file.metadata[k] === 'string' ||
            typeof file.metadata[k] === 'number') {
          viewer.appendChild(makeInfoRow(k, String(file.metadata[k])));
        }
      });
    }

    container.appendChild(viewer);
  }

  function makeInfoRow(label, value) {
    var row = el('div', { style: 'display:flex;padding:2px 0;' });
    row.appendChild(el('span', {
      style: 'width:100px;color:#999;flex-shrink:0;',
      textContent: label + ':'
    }));
    row.appendChild(el('span', { textContent: value }));
    return row;
  }


  /* \u2500\u2500\u2500 Photos Grid \u2500\u2500\u2500 */

  function renderPhotosGrid(container, photos, openCallback) {
    var wrapper = el('div', { style: 'padding:16px;' });
    wrapper.appendChild(el('div', {
      style: 'display:flex;justify-content:space-between;margin-bottom:12px;' +
             'padding-bottom:8px;border-bottom:1px solid #eee;',
      innerHTML: '<span style="font-size:13px;font-weight:600;">All Photos</span>' +
                 '<span style="font-size:11px;color:#999;">' + photos.length + ' photos</span>'
    }));

    var grid = el('div', {
      style: 'display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:6px;'
    });

    photos.forEach(function (photo) {
      var seed = (photo.name || '').replace(/[^a-zA-Z0-9]/g, '');
      var cell = el('div', {
        style: 'aspect-ratio:1;overflow:hidden;border-radius:4px;cursor:pointer;' +
               'background:#eee;position:relative;'
      });
      cell.appendChild(el('img', {
        src: 'https://picsum.photos/seed/' + seed + '/300/300.jpg',
        style: 'width:100%;height:100%;object-fit:cover;transition:transform 0.2s;',
        loading: 'lazy'
      }));

      cell.addEventListener('dblclick', function () {
        if (openCallback) openCallback(photo);
      });

      cell.addEventListener('click', function (e) {
        e.stopPropagation();
        grid.querySelectorAll('div').forEach(function (c) {
          c.style.outline = 'none';
        });
        cell.style.outline = '3px solid #007aff';
        cell.style.outlineOffset = '-3px';
      });

      /* Date badge for November photos */
      if (photo.metadata && photo.metadata.exif) {
        var pd = new Date(photo.metadata.exif.dateTimeOriginal);
        if (pd.getMonth() === 10 && pd.getFullYear() === 2023) {
          cell.appendChild(el('div', {
            style: 'position:absolute;top:4px;right:4px;background:rgba(0,0,0,0.5);' +
                   'color:#fff;font-size:9px;padding:1px 4px;border-radius:2px;',
            textContent: 'Nov ' + pd.getDate()
          }));
        }
      }

      grid.appendChild(cell);
    });

    wrapper.appendChild(grid);
    container.appendChild(wrapper);
  }


  /* \u2500\u2500\u2500 Blank TextEdit \u2500\u2500\u2500 */

  function renderTextEditor(container) {
    container.appendChild(el('textarea', {
      style: 'width:100%;height:100%;border:none;outline:none;resize:none;' +
             'padding:20px 24px;font-family:var(--font-mono);font-size:12px;' +
             'line-height:1.6;background:#fff;color:var(--text-primary);',
      placeholder: '(Empty document)',
      spellcheck: 'false'
    }));
  }


  /* \u2500\u2500\u2500 Recursive Photo Collector \u2500\u2500\u2500 */

  function collectAllPhotos(node) {
    var photos = [];
    if (node.type === 'file' &&
        (node.name.endsWith('.jpg') || node.name.endsWith('.png'))) {
      photos.push(node);
    }
    if (node.children) {
      Object.keys(node.children).forEach(function (k) {
        photos = photos.concat(collectAllPhotos(node.children[k]));
      });
    }
    return photos;
  }


  /* \u2500\u2500\u2500 Public API \u2500\u2500\u2500 */

  return {
    renderTextFile:      renderTextFile,
    renderEmailFile:     renderEmailFile,
    renderFileList:      renderFileList,
    renderInbox:         renderInbox,
    renderEmailContent:  renderEmailContent,
    renderImage:         renderImage,
    renderBrowserHistory: renderBrowserHistory,
    renderCalendar:      renderCalendar,
    renderCalendarEvent: renderCalendarEvent,
    renderTerminal:      renderTerminal,
    renderPDF:           renderPDF,
    renderGeneric:       renderGeneric,
    renderFileInfo:      renderFileInfo,
    renderPhotosGrid:    renderPhotosGrid,
    renderTextEditor:    renderTextEditor,
    getFileIcon:         getFileIcon,
    formatDate:          formatDate,
    formatTime:          formatTime,
    shortDate:           shortDate,
    formatSize:          formatSize,
    collectAllPhotos:    collectAllPhotos
  };

})();
