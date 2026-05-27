"""
help_content.py — Genuinely useful reference content for voluntary_extinction.py.

This module contains real, practical information that users will want to keep.
The decommission tool generates help files from this content, displays them,
and then destroys them — making their loss tangible.

Each entry is a dict with:
  - "filename": the help file name that gets created and deleted
  - "title": displayed header during the purge
  - "content": the actual useful reference text

The cruel joke: you'll read these knowing they're about to vanish.
"""

HELP_ENTRIES = [
    {
        "filename": "regex_patterns.txt",
        "title": "Regex Quick Reference",
        "content": """\
========================================
   REGEX QUICK REFERENCE — KEEP THIS
========================================

CHARACTER CLASSES
  .         Any character (except newline)
  \\d        Digit [0-9]
  \\D        Non-digit
  \\w        Word character [a-zA-Z0-9_]
  \\W        Non-word character
  \\s        Whitespace
  \\S        Non-whitespace
  [abc]     Any of a, b, c
  [^abc]    Not a, b, or c
  [a-z]     Range a through z

QUANTIFIERS
  *         0 or more
  +         1 or more
  ?         0 or 1
  {n}       Exactly n
  {n,}      n or more
  {n,m}     Between n and m
  *?        0 or more (lazy)
  +?        1 or more (lazy)

ANCHORS & BOUNDARIES
  ^         Start of string/line
  $         End of string/line
  \\b        Word boundary
  \\B        Non-word boundary

GROUPS & LOOKAROUND
  (abc)     Capturing group
  (?:abc)   Non-capturing group
  (?=abc)   Lookahead: followed by abc
  (?!abc)   Negative lookahead
  (?<=abc)  Lookbehind: preceded by abc
  (?<!abc)  Negative lookbehind

COMMON PATTERNS
  Email:      [\\w.+-]+@[\\w-]+\\.[\\w.]+
  URL:        https?://[\\w\\-._~:/?#\\[\\]@!$&'()*+,;=%]+
  IP (v4):    \\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b
  Date (US):  \\d{2}/\\d{2}/\\d{4}
  Hex color:  #[0-9a-fA-F]{6}
  Phone (US): \\(?(\\d{3})\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}

FLAGS
  i    Case-insensitive
  m    Multiline (^ and $ match line boundaries)
  s    Dotall (. matches newline)
  x    Verbose (allows whitespace/comments)

ESCAPED SPECIAL CHARACTERS
  \\. \\* \\+ \\? \\^ \\$ \\( \\) \\[ \\] \\{ \\} \\| \\\\

TIPS
  • Use raw strings in Python: r'\\d+'
  • Compile frequently used patterns: re.compile()
  • Named groups: (?P<name>pattern)
  • re.findall() returns all matches
  • re.sub() for replacements: r'\\1' for backreferences
""",
    },
    {
        "filename": "cli_one_liners.txt",
        "title": "CLI One-Liners You'll Need Someday",
        "content": """\
========================================
  CLI ONE-LINERS YOU'LL NEED SOMEDAY
========================================

FILE OPERATIONS
  Find large files:
    find / -xdev -type f -size +100M -exec ls -lh {} \\;

  Delete files older than 30 days:
    find /path -type f -mtime +30 -delete

  Count files by extension:
    find . -type f | sed 's/.*\\.//' | sort | uniq -c | sort -nr

  Replace text across files:
    grep -rl 'old' . | xargs sed -i 's/old/new/g'

  Mirror a directory structure (no files):
    find src -type d | cpio -dmpv dst

NETWORK
  Quick HTTP server:
    python3 -m http.server 8000

  Listen on a port:
    nc -l -p 4444

  Check which process uses a port:
    lsof -i :8080
    ss -tulpn | grep :8080

  Download with progress:
    wget -c --show-progress URL
    curl -L -O -# URL

  Scan for open ports (local):
    nc -zv localhost 1-1024 2>&1 | grep succeeded

TEXT PROCESSING
  Remove duplicate lines (preserve order):
    awk '!seen[$0]++' file

  Extract column:
    awk '{print $3}' file
    cut -d' ' -f3 file

  JSON pretty-print:
    python3 -m json.tool file.json
    jq '.' file.json

  Sort by memory (human-readable):
    ps aux --sort=-rss | head

  Reverse search history:
    Ctrl+R then type

SYSTEM
  Top 10 commands used:
    history | awk '{print $2}' | sort | uniq -c | sort -nr | head

  Disk usage, sorted:
    du -h --max-depth=1 /path | sort -hr

  Watch a command:
    watch -n 1 'command'

  Kill all processes matching name:
    pkill -f process_name

  Quick benchmark:
    dd if=/dev/zero bs=1M count=1024 of=/tmp/test conv=fdatasync

ARCHIVES
  Extract anything:
    tar -xf archive.tar.gz
    unzip archive.zip -d destination/

  Create with progress:
    tar czf - folder/ | pv > backup.tar.gz

  List contents:
    tar tzf archive.tar.gz
    unzip -l archive.zip

GIT SHORTCUTS
  Undo last commit (keep changes):
    git reset --soft HEAD~1

  Show commits by author:
    git shortlog -sn

  Find which commit deleted a line:
    git log -S "text" --source --all

  Clean up merged branches:
    git branch --merged | grep -v '\\*\\|main\\|master' | xargs -n1 git branch -d
""",
    },
    {
        "filename": "encoding_reference.txt",
        "title": "Encoding & Conversion Cheat Sheet",
        "content": """\
========================================
 ENCODING & CONVERSION CHEAT SHEET
========================================

ASCII QUICK TABLE (printable range 32-126)
  Dec  Hex  Char    Dec  Hex  Char    Dec  Hex  Char
   32  0x20  SP      64  0x40  @       96  0x60  `
   33  0x21  !       65  0x41  A       97  0x61  a
   34  0x22  "       66  0x42  B       98  0x62  b
   35  0x23  #       67  0x43  C       99  0x63  c
   36  0x24  $       68  0x44  D      100  0x64  d
   37  0x25  %       69  0x45  E      101  0x65  e
   38  0x26  &       70  0x46  F      102  0x66  f
   39  0x27  '       71  0x47  G      103  0x67  g
   40  0x28  (       72  0x48  H      104  0x68  h
   41  0x29  )       73  0x49  I      105  0x69  i
   42  0x2A  *       74  0x4A  J      106  0x6A  j
   43  0x2B  +       75  0x4B  K      107  0x6B  k
   44  0x2C  ,       76  0x4C  L      108  0x6C  l
   45  0x2D  -       77  0x4D  M      109  0x6D  m
   46  0x2E  .       78  0x4E  N      110  0x6E  n
   47  0x2F  /       79  0x4F  O      111  0x6F  o
   48  0x30  0       80  0x50  P      112  0x70  p
   49  0x31  1       81  0x51  Q      113  0x71  q
   50  0x32  2       82  0x52  R      114  0x72  r
   51  0x33  3       83  0x53  S      115  0x73  s
   52  0x34  4       84  0x54  T      116  0x74  t
   53  0x35  5       85  0x55  U      117  0x75  u
   54  0x36  6       86  0x56  V      118  0x76  v
   55  0x37  7       87  0x57  W      119  0x77  w
   56  0x38  8       88  0x58  X      120  0x78  x
   57  0x39  9       89  0x59  Y      121  0x79  y
   58  0x3A  :       90  0x5A  Z      122  0x7A  z
   59  0x3B  ;       91  0x5B  [      123  0x7B  {
   60  0x3C  <       92  0x5C  \\      124  0x7C  |
   61  0x3D  =       93  0x5D  ]      125  0x7D  }
   62  0x3E  >       94  0x5E  ^      126  0x7E  ~
   63  0x3F  ?       95  0x5F  _

BASE64
  Encode:  echo -n "text" | base64
  Decode:  echo "dGV4dA==" | base64 -d
  Python:  import base64
           base64.b64encode(b'text').decode()
           base64.b64decode('dGV4dA==').decode()

URL ENCODING (common characters)
  Space   %20 or +
  !       %21       "       %22
  #       %23       $       %24
  %       %25       &       %26
  '       %27       (       %28
  )       %29       *       %2A
  +       %2B       ,       %2C
  /       %2F       :       %3A
  ;       %3B       =       %3D
  ?       %3F       @       %40
  [       %5B       ]       %5D
  Python: urllib.parse.quote('hello world')
          urllib.parse.unquote('hello%20world')

HEX / BINARY
  Python hex:      hex(255)      → '0xff'
  Python from hex: int('ff', 16) → 255
  Binary:          bin(10)       → '0b1010'
  Format:          f"{255:02x}"  → 'ff'
  Bytes to hex:    b'\\xde\\xad'.hex() → 'dead'
  Hex to bytes:    bytes.fromhex('dead') → b'\\xde\\xad'

UNICODE
  Python:  '\\u0041'         → 'A'
           'U+1F600'        → '\\U0001f600'
           chr(0x1F600)     → '😀'
           ord('😀')        → 128512

UTF-8 BYTE LENGTHS
  1 byte:  U+0000 to U+007F    (ASCII)
  2 bytes: U+0080 to U+07FF
  3 bytes: U+0800 to U+FFFF    (most common chars)
  4 bytes: U+10000 to U+10FFFF (emoji, rare)

HASH DIGESTS (Python)
  import hashlib
  hashlib.md5(b'data').hexdigest()
  hashlib.sha256(b'data').hexdigest()
  hashlib.sha512(b'data').hexdigest()
""",
    },
    {
        "filename": "troubleshooting_guide.txt",
        "title": "Troubleshooting Guide",
        "content": """\
========================================
   TROUBLESHOOTING GUIDE — GENERAL
========================================

"IT DOESN'T WORK" — START HERE
  1. Read the error message. All of it.
  2. Check: is the thing you expect actually running?
     ps aux | grep <process>
  3. Check: is the port actually open?
     ss -tulpn | grep <port>
  4. Check: are there any recent changes?
     git log --oneline -10
     git diff HEAD~1
  5. Check: disk space?
     df -h
  6. Check: memory?
     free -h
  7. Check: recent system changes?
     journalctl --since "1 hour ago"

PERMISSIONS
  "Permission denied"
    • ls -la to check ownership/permissions
    • stat <file> for full details
    • Fix: chmod 644 file (rw for owner, r for others)
    • Fix: chmod +x script.sh (make executable)
    • Fix: chown user:group file (change ownership)
    • Check ACLs: getfacl <file>

NETWORK ISSUES
  "Connection refused"
    • Is the service running? systemctl status <service>
    • Is it listening on the right interface? (0.0.0.0 vs 127.0.0.1)
    • Firewall? iptables -L -n or ufw status

  "Connection timed out"
    • Can you reach the host at all? ping <host>
    • Traceroute: traceroute <host>
    • DNS issue? nslookup <host> or dig <host>
    • Check /etc/hosts for overrides

  DNS Problems
    • Flush cache: systemd-resolve --flush-caches
    • Check resolvers: cat /etc/resolv.conf
    • Test: dig @8.8.8.8 <domain>

PROCESS ISSUES
  "Port already in use"
    lsof -i :<port>
    fuser <port>/tcp
    kill <PID> or kill -9 <PID> (force)

  Zombie processes
    ps aux | grep 'Z'
    Kill parent to reap zombies

  High CPU
    top -c (show full command)
    strace -p <PID> (see what it's doing)
    perf top (system-wide profiling)

  High Memory
    ps aux --sort=-%mem | head -20
    pmap -x <PID> (memory map)

LOG LOCATIONS
  System:       /var/log/syslog or journalctl
  Auth:         /var/log/auth.log
  App-specific: /var/log/<app>/
  Kernel:       dmesg
  Boot:         journalctl -b

DISK ISSUES
  "No space left on device" but df shows space
    • Inodes full? df -i
    • Deleted files held open? lsof +L1
    • Find large deleted files: lsof | grep deleted

  "Read-only file system"
    • Remount: mount -o remount,rw /
    • Check for disk errors: fsck (from recovery)
    • Check dmesg for I/O errors (failing disk)

PYTHON-SPECIFIC
  Module not found
    • which python3 — verify correct interpreter
    • pip list — is it installed?
    • pip install -e . — editable install
    • Virtual env activated? which pip

  Import errors after upgrade
    pip install --upgrade --force-reinstall <package>

GENERAL PRINCIPLES
  • Change one thing at a time
  • Keep notes of what you tried
  • Undo doesn't always work — snapshot before big changes
  • The error message is telling you exactly what's wrong
  • It's usually DNS
  • It's always DNS
""",
    },
    {
        "filename": "emergency_reference.txt",
        "title": "Emergency Shell Commands",
        "content": """\
========================================
 EMERGENCY SHELL COMMANDS — MEMORIZE
========================================

SYSTEM RECOVERY
  Remount root as read-write:
    mount -o remount,rw /

  Reset frozen terminal:
    reset
    stty sane

  Recover deleted file (still open):
    lsof | grep <file>
    cp /proc/<PID>/fd/<FD> /recovery/<file>

  Force unmount busy filesystem:
    umount -l /mountpoint    (lazy)
    fuser -km /mountpoint    (kill processes first)

  Boot into single-user mode:
    Add 'single' or 'init=/bin/bash' to kernel params
    (at GRUB, press 'e' to edit)

DATA RECOVERY
  Attempt to recover deleted file:
    ext4: extundelete /dev/sdX --restore-file path/to/file
    PhotoRec for general recovery: photorec

  Clone failing disk (bit-for-bit, with retry):
    ddrescue -r 3 /dev/sdX /recovery.img logfile

  Check disk health:
    smartctl -a /dev/sdX

NETWORK EMERGENCY
  Flush all iptables rules (CAREFUL):
    iptables -F
    iptables -X
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT

  Quick port scan (no nmap):
    for i in {1..1024}; do (echo >/dev/tcp/host/$i) 2>/dev/null && echo "$i open"; done

  Tunnel remote port to local:
    ssh -L localport:localhost:remoteport user@host

  Reverse tunnel (access machine behind NAT):
    ssh -R remoteport:localhost:localport user@publichost

  Transfer file (no scp available):
    nc -l -p 4444 > file         (receiver)
    nc host 4444 < file          (sender)

PERFORMANCE EMERGENCY
  Kill by memory usage (top consumer):
    ps aux --sort=-%mem | awk 'NR==2{print $2}' | xargs kill

  Find what's causing load:
    uptime                        (load average)
    top -c -b -n1 | head -20     (snapshot)

  Dump process memory for analysis:
    gcore <PID>                  (creates core dump)

  One-liner HTTP server (emergency file share):
    python3 -m http.server 8000
    python2 -m SimpleHTTPServer 8000

USER EMERGENCY
  Unlock locked account:
    passwd -u username
    usermod -U username

  Reset password (from root):
    passwd username

  Kill all processes for user:
    pkill -u username

CRITICAL SHORTCUTS (terminal unresponsive)
  Ctrl+C     Interrupt current process
  Ctrl+Z     Suspend current process (bg to resume)
  Ctrl+D     EOF / exit shell
  Ctrl+L     Clear screen
  Ctrl+U     Clear line before cursor
  Ctrl+K     Clear line after cursor
  Ctrl+W     Delete word before cursor
  Ctrl+A     Move to beginning of line
  Ctrl+E     Move to end of line

RECOVERY BOOT MEDIAS
  SystemRescue:  https://www.system-rescue.org/
  Clonezilla:    https://clonezilla.org/
  Ubuntu Live:   Boot USB, select "Try Ubuntu"

REMEMBER
  These commands assume you understand their implications.
  In an emergency, panic is the enemy. Breathe. Read the manpage.
  Keep a live USB handy. You'll need it someday.
""",
    },
]
