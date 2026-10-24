# 更新履歴 (ChangeLog)

各版の変更点です。原文は英語のまま載せています。

## Phase 9.2.0 (Core 4.2.0) (2026/10/23)

- Phase 9 can replace Phase 8 (8.2.x) as it is: the dictionaries, the SAORI modules and the baseware link of a Phase 8 ghost work by only replacing shiori.dll. There is no incompatible change like the one from Phase 7 to 8. The intended differences are the UTF-8 (BOM) files written by `save`/`savecrypt` (8.2.9 and earlier cannot read them), the Charset header, and the Unicode code point order (see 9.0.0 below)
- `date` and `mktime` use 64 bit seconds (the year 2038 problem). The 32-bit mingw-w64 (msvcrt) has a 32 bit time\_t, so the 64 bit CRT functions (\_time64, \_localtime64, \_mktime64) are called directly. `"date %s 4102444800"` and `"mktime 2100 1 1 0 0 0"` work. The limits of the C runtime of the Windows build (msvcrt) remain: a time before 1970 and a time after about the end of the year 3000 (`date` gives an empty string, `mktime` gives -1; measured: `date` up to 3001/01/01 00:00:00 UTC, `mktime` up to 3001 but not 3100). The POSIX build follows the time\_t of the OS. The integers of the expressions ($\[ \]) are still 32 bit, so a calculation with seconds of 2038 or later (a difference of two $(date %s)) is not correct yet. (misc: Int64ToString / StringToInt64)
- diagnostics: every error and warning of the compiler, the interpreter, the dictionary and the KIS commands/SAORI now has a code and a location, in one format:

  ```
      file(line): error K-E0028: undefined function "foo" called.
          in $(foo) at file(line)
          in ${OnBoot} at file(line)
  ```

  - the codes are K-E&lt;number\> / K-W&lt;number\>; the numbers are listed in kawari\_log.h (enum DiagCode) and are never changed or reused
  - the compile errors used to be `"file line: error: message"` (the format changed; the text of the messages is the same). The location of a runtime diagnostic is the dictionary file and the line of the word being run, found by (entry, word): a word that is shared by several entries has one location per entry. Words made at run time (adddict, set) have no location, and the location of a word that was freed is forgotten (IDs are reused). The statements of `"=kis"` zones have their own lines, and a `function` / `lambda` made there is located at its statement
  - the call chain (up to 8 frames) is printed under the diagnostic: `"in ${entry}"` for a word, `"in $(name)"` for a user function, `"in <kis zone>"` for the =kis zone being loaded. `decl` warnings print only the innermost frame
  - nothing is printed or recorded for a level that `loglevel` does not enable (quiet is still the default), and the meaning of a dictionary is not changed: an undefined entry is still empty. Running cost: a push and a pop of a small frame per word run, not measurable in the hot path
  - `"too few/many arguments"` of KIS commands are K-W1001 / K-W1002; the errors of regex\_\* are K-E1100..1102; other KIS errors are K-E1000 and SAORI errors are K-E1200 (the same text as before)
  - the lexer used the EOL message also for a quoted string that reaches the end of the file; it now uses the EOF one (K-E0002). The preprocessor adds a final newline, so a quote left open in a file is still reported as K-E0001 and K-E0002 is rarely reached
  - `"load/save failed"` has a space before the path
- add `"kosui --check"`: loads the dictionary in the sandbox, reports the diagnostics and quits, without reading the standard input

  ```
      kosui --check [--format text|json] [--werror] [--decl]
            [--eval <script>]... [--seed <n>] [<rcfile>]
  ```

  - exit code: 0 = nothing, 1 = warnings only, 2 = errors (--werror makes warnings errors), 3 = could not run (the rcfile cannot be read)
  - the output is only diagnostics (a line `"check: N error(s), M warning(s)"` at the end); the `echo` of KIS and `loglevel` / `logfile` do not change it. json prints one JSON document in UTF-8 whatever the console is
  - --eval runs a script after the load (as typed in kosui), so the diagnostics of the events can be found; it samples random choices, use --seed to repeat. --decl also reports reads of empty entries (K-W0003)
  - the sandbox (engine-\>SetSandbox) stops everything that reaches out of the dictionary: files are not written (save, textsave, logfile... succeed without writing), SAORI modules are not loaded (a call to a registered or internal\_\* module answers Result: 0), and the baseware is not reached (Direct SSTP). It is for static checking only: `"=kis"` is really run, so a loop that never ends hangs --check
- add the static check (lint) to `"kosui --check"`: after the load (and before --eval) it walks every word of the dictionary and every `"=kis"` zone, and warns about what is wrong without running it. `--no-lint` turns it off
  - K-W2001: a reference to an entry that is defined nowhere (${x}, ${a + x}, $x\[0\]), which is silently empty at run time
  - K-W2002: a command that is neither built in, nor defined by `function` (or as System.Function.&lt;name\>), nor a forced built-in call (`.name`)
  - K-W2003: a regex\_\* command with an unquoted ( ) in an argument. The parentheses of a bare word are the block syntax of Kawari and are removed, so the regular expression never sees them: regex\_match (a) x matches `a` without a group. Quote the pattern: regex\_match `"(a)"` x. This one is found by the compiler (the tree keeps no trace of the parentheses) while it loads the dictionary, only when checking
  - K-W2004: regex\_replace / regex\_replace\_first with an unquoted ${N} in the replacement string. It is expanded as a history reference before the command runs, so the back reference never reaches the regex
  - a comment line `"# lint:disable-next-line=K-W2001, K-W2003"` suppresses the listed lint warnings (K-W2xxx) on the next line of the file. Only a whole-line `"#"` is a comment in Kawari, so there is no end-of-line form. A warning in a multi-line word is located at the first line of the word, so the comment goes above the entry
  - to keep false positives down, these names count as defined: entries that exist after the load, any literal given as an argument of a statement (set / adddict / foreach variables...) or written in a `"$(...)"` inside a string, a name whose head is a literal and whose tail is built at run time (launch\_a\_${n}), System.\* and @local. Names built by ${...} are not checked at all. These are warnings: --werror makes them errors
  - the entries of the warnings are sorted by file and line. A multi-line word is located at its first line
  - the compiled `"=kis"` zones are kept (engine-\>SetKeepZones) until the check is done; they are freed right after the run as before otherwise
  - TKVMCode\_base::GetChildren() lists the children of a code node, for the walk. It is not used when running
- add the check suite to test/run.ps1 and test/run\_posix.py (test/check/\*)

## Phase 9.1.1 (Core 4.1.1) (2026/10/22)

- add `textload_charset`, `textsave_charset` and `textappend_charset`: the same as `textload`, `textsave` and `textappend` with the charset of the file as an argument (textload\_charset Entry File Charset, textsave\_charset File Charset Entry...). The charsets are Shift\_JIS, UTF-8, EUC-JP, ISO-2022-JP, EUC-KR and GB2312 (Windows uses the code pages 20932, 50220, 949 and 936, so GB2312 is GBK and EUC-KR is UHC; POSIX uses iconv). `auto` is also accepted by textload\_charset. An unknown or unsupported charset is an error: the entry is not changed and the file is not overwritten. `textload`, `textsave` and `textappend` are unchanged
- fixed crashes:
  - a dictionary word with `"$"` not followed by a substitution (x : ${$}) put a NULL code into the word and crashed on evaluation or `save`
  - `"$[ (-2147483647-1) / -1 ]"` (and `"%"`) raised a division fault
  - `date` with a time that localtime() cannot convert (a negative value) dereferenced NULL
  - an exception in `load`, `request` or `unload` (and the so\_\* object interface) went out of the module into the host; GlobalAlloc failure is now checked
- fixed bugs in the interpreter:
  - after a word of the form ${entry} was collected and its ID reused, the new word was dropped from the set operations (${a+b}, size etc.)
  - `char_at` on an empty string returned a NUL character
  - `inc` / `dec` overflowed at the int limits; they now stop at the limit
  - an integer value of INT\_MIN was printed as garbage, and `-` alone was taken as the integer 0
  - numbers out of the int range are now clamped also where long is 64 bit
  - `mktime` ignored daylight saving time (now the same as `date`)
  - `save` / `savecrypt` / `textsave` given an absolute path wrote the file name into the current directory of the host; it is now written into the ghost's directory, as with a relative path. `textsave` logged `"load failed"` on a write error
  - `"$(if cond)"` without a body leaked the condition
  - the lexer could read the last character again at the end of a file
  - the message table is built when the module is loaded, not on its first use from possibly several threads
- fixed bugs in SAORI and the platform layer:
  - loading the same SAORI DLL twice left an extra LoadLibrary reference, so the DLL stayed loaded after the last unload
  - a SAORI without `request` got `unload` without `load`; on POSIX, dlclose(NULL) was called for a library that failed to open
  - POSIX: an unencodable character in ISO-2022-JP output was written in the kanji shift state and garbled the rest; errno was read too late
  - POSIX: Direct SSTP to ninix could die by SIGPIPE, and failed when the 4-byte length header arrived in pieces
  - Windows: environment variables are read with GetEnvironmentVariableW, so the values set by the host after start are seen
  - a base path at the root (`/` or `/a` with `../b`) lost the root
- fixed bugs in the tools:
  - kosui no longer loops forever at the end of its input without `exit`
  - kosui (Direct SSTP mode) read past the WM\_COPYDATA data, could keep the mutex, and lost replies that came after SendMessageTimeout returned
  - kawari\_encode / kawari\_encode2 / kawari\_decode2 took a `.` in a folder name as the extension, and could overwrite the input file with the output (such a file is now skipped)
  - the ghost list of kosui read the FMO size with sign extension
  - shiori/py\_shiori.cpp passed the handle with a wrong format code
- merged the pull requests #7 and #8 of the upstream (Narazaka):
  - MACH\_TYPE = js exports the utility functions of Emscripten (ccall, cwrap, intArrayFromString and intArrayToString), which newer Emscripten does not export unless it is told to (and the build is -Os)
  - add MACH\_TYPE = wasm (WebAssembly, loaded asynchronously)
  - the JavaScript API is changed: `Kawari` is replaced by `"newKawari (onRuntimeInitialized)"`, which calls the callback with { Module, FS, PATH, ERRNO\_CODES, NODEFS, IDBFS, WORKERFS } once the runtime is ready

## Phase 9.1.0 (Core 4.1.0) (2026/10/19)

- add `lambda`: defines an anonymous function and returns its name (System.Lambda.&lt;n\>, never the same as a defined function). The body is written like that of `function`, and the returned name is used as a command name ($(${f} args)) or passed to another function. It is not a closure: the local entries (@arg etc.) of the place where it was defined are not carried. Remove it with `rmfunc`
- updated uka\_regexp (build/src/uka\_regexp):
  - (\*UCP) at the head of a pattern makes \d \w \s \b and the POSIX classes use the Unicode properties (the default is still ASCII only)
  - where wchar\_t is 16 bit (Windows), a surrogate pair is one character in a pattern (. and \[^a\] match a whole emoji, and a match never starts or ends in the middle of a pair). The positions given to KIS are still counted in wchar\_t
  - a{,m} is accepted as a{0,m}, \K in a lookaround is rejected, and catastrophic backtracking now ends in polynomial time
  - fixed the output string aliasing the subject or the template in Replace(), and the capacity overflow of the internal buffers (it now throws ERR\_MEMORY); a start offset inside a surrogate pair is moved to the next character boundary
- removed the notes of the unimplemented `expr` and `test` from the manual, and the finished or abandoned items (boost regex, rexpr, SAORI/2.0, i18n patch) from the plan in README.md

## Phase 9.0.0 beta4 (Core 4.0.0) (2026/10/18)

- add the regular expression commands `regex_match`, `regex_find`, `regex_findall`, `regex_count`, `regex_replace`, `regex_replace_first`, `regex_erase`, `regex_erase_first`, `regex_split` and `regex_escape`, on the engine uka\_regexp (build/src/uka\_regexp, a git submodule; clone with --recursive or run `"git submodule update --init"`). The syntax is close to PCRE2; \d \w \s \b match ASCII only. The matches, the groups and the pieces are stored to the entry given as an argument
- a subroutine call in a pattern, (?&name) or \g&lt;name\>, whose name the pattern does not define is replaced with the expansion of the entry ${name}. A pattern with parentheses must be quoted (`...`) in the dictionary and the script
- makedepend.rb resolves #include `foo.h` of the same folder (needed by uka\_regexp) and is converted from CP932 to EUC-JP

## Phase 9.0.0 beta3 (Core 4.0.0) (2026/10/18)

- fixed: the module names of SAORI over DirectSSTP were lowercased with towlower(), which depends on the LC\_CTYPE of the host (with tr\_TR, `I` became U+0131 and `INTERNAL_...` was not recognized). Only ASCII letters are lowercased now
- fixed the misuse of the STL:
  - the destructor of the unique SAORI module factory used an iterator after erase()
  - the result of find() was kept in `"unsigned int"` and compared with npos. On 64-bit POSIX the comparison never became true, so `gsub` (when no more match is left) threw an exception, `tr` read out of bounds, and `isexist` did not append the separator. `split`, the `match` family and the status line of SAORI are changed to size\_type too (no change of behavior). On 32-bit Windows nothing changes
  - the length given to `substr` could overflow
  - decoding a broken Base64 text with more `"="` than the decoded length threw an exception
  - internal only (not reachable from KIS so far): TEntry::Pop on an entry emptied by Clear() called back() on an empty vector, and TEntry::Replace accepted the index just past the last word

## Phase 9.0.0 beta2 (Core 4.0.0) (2026/10/18)

- add `getproperty`, `setproperty` and `executesstp`/`executesstpx`: property system and SSTP EXECUTE commands sent to the baseware (SSP, ninix) by Direct SSTP. The window of the baseware is taken from `"NOTIFY hwnd"`. The response code is stored to System.SSTP.ResponseCode and the additional data to System.SSTP.Data (`executesstpx` also stores it to the given entry)
- SAORI over DirectSSTP: the modules built in the baseware (internal\_\*, and the compatible ones such as houchi/httpc/string) can be called with `callsaori` like a SAORI without a DLL. `saoriregist` a name without a DLL file, or call an unregistered `"internal_*"` name (checked with ListModules of internal\_system). A DLL file, if it exists, is loaded as before
- the commands above are refused for requests whose SecurityLevel is not local
- Linux: link with -lrt -lpthread (FMO of ninix)
- fixed: System.Sender.Path was never set, so `callsaori` always sent `"SecurityLevel: Local"` to SAORI. It is now set for every request (local / external / unknown) and used as the SecurityLevel of the SAORI request

## Phase 9.0.0 beta1 (Core 4.0.0) (2026/10/18)

- changed the internal strings to wchar\_t (UTF-16 on Windows, UTF-32 on POSIX). Characters outside the BMP (e.g. emoji) count as 2 characters on Windows
- fixed the file/folder name problem with Shift\_JIS characters whose second byte is 0x5C etc. and with IBM/NEC extension characters (isdir, isexist, readdir...)
- changed string comparison (`compare`, `"<"` `">"` in expression, the order of entry enumeration) to Unicode code point order instead of Shift\_JIS byte order (no change for ASCII)
- dictionary files: auto-detect UTF-8 (BOM, or valid UTF-8 as a whole) and Shift\_JIS (CP932). Encrypted lines (!KAWA0000/!KAWA0001) are read as UTF-8 when the file has a BOM, otherwise as Shift\_JIS
- `save`/`savecrypt` now write UTF-8 with BOM (a dictionary saved by `save` or `savecrypt` cannot be read correctly by 8.2.9 or earlier: the BOM breaks the first line and Japanese text is read as Shift\_JIS)
- `textload` detects UTF-8/Shift\_JIS automatically. `textsave`/`textappend` write UTF-8 without BOM (`textappend` appends UTF-8 even to a Shift\_JIS file)
- kawari\_encode/kawari\_encode2 add a BOM to the output when the input is UTF-8. kawari\_decode2 adds a BOM when the input has a BOM
- SHIORI: interpret the request by its Charset header and answer in the same charset (Shift\_JIS when absent or unknown). Every response has a Charset header; System.Response.Charset (Shift\_JIS/UTF-8) can select it
- SHIORI: export `loadu` (load with a UTF-8 path)
- SAORI: start with UTF-8, follow the Charset of the GET Version response (Shift\_JIS when absent), interpret responses by their Charset, and call `loadu` of the SAORI DLL if it is exported
- `rccharset` accepts UTF-8 as well as Shift\_JIS (Japanese messages)
- `logfile` writes UTF-8 without BOM. kosui console I/O uses the ANSI code page (UTF-8 on POSIX)
- `chr`, `toupper/tolower` and `escape` keep their behavior (ASCII only / Shift\_JIS code interpretation)
- Win32 API: W versions (UNICODE), WINVER=0x0500 (Windows 2000)
- non-Windows builds use iconv for charset conversion (-liconv on FreeBSD/darwin)

## Phase 8.2.9 (2026/10/17)

- add the Win32 version information resource to the mingw binaries
- speed up: small-object allocator (mingw only, FASTALLOC option in gcc.mak) and cheaper word comparison in the dictionary

## Phase 8.2.8 (2008/03/30)

- fixed `textsave` command (ignore 3rd,4th... argument) (Thanks: Don, ukya, xenon)

## Phase 8.2.7 (2008/02/16)

- fixed `insertstr` command (work as `insert` command) (Thanks: Phantom 9)
- fixed `entrycount` command (answer wrong number) (Thanks: Phantom 9)

## Phase 8.2.6 (2008/01/27)

- fixed `gsub` command (the substitution leakage when consecutive pattern is substituted by null) (Thanks: C.Ponapalt)

## Phase 8.2.5 (2008/01/26)

- fixed the midpoint(0xa5) problem in Japanese character code (gcc optimize option: -Os =\> -O1. enbuged by UPX!)
- fixed `isexist` command (do not work in root directory)
- add `quiet`mode option for kosui (--quiet). After the initialization file is read, kosui ends at once when quiet mode.
- fixed compile error for ninix-aya environment (Thanks: paulliu)

## Phase 8.2.4 (2005/10/30)

- fixed `rfind` command (do not work)
- add project files for Visual C++ 7.1(Thanks: Shiba-yan)
- fixed compile problem for Visual C++ 7.1 in 'misc/l10.cpp ctow' function (Thanks: Shiba-yan)
- fixed a typo in 'gcc.mak' for 'ninix-aya' (Thanks: jado)

## Phase 8.2.3 (2005/07/03)

- arranged the index management code of dictionary commands
- changed `inc/dec` commands to enable to use the index value which likes dictionary commands

## Phase 8.2.3RC (closed) (2005/06/21)

- fixed auto type judgement feature(number or character) in expression
- release compiler: MinGW 2.0.0-3 -\> MinGW 4.1.0(gcc.3.4.2)
- built shiori.dll binary by 'gcc -shared' instead of 'dllwrap'
- supported gcc3.x(warning messages)
- fixed `split` command (NULL pointer violation!)
- fixed `inc/dec` command (freezed when using the negative index value)
- added `mktime` command

## Phase8.2.2 (2004/09/05)

- fixed dictionary commands which cannot use the negative index value from Phase 8.2.1

## Phase8.2.1 (2004/09/04)

- fixed dictionary commands which cannot use some S-JIS characters for entry name when using index (Thanks 89@OpenKEEPS thread)
- include patches for 'ninix-aya' and 'Nise-Ringo' (Thanks ABE, phonohawk)

## Phase8.2.0 (2004/02/01)

- changed `date` command to enable to format a second from the Epoc
- fixed `split` command (NULL string separator problem)
- changed `split` command. When you omit 3rd argument or set "", it splits by char.
- changed `join` command. You chan omit 3rd argument.
- fixed `listsub` command (`ghost` entrytree problem)
- fixed string search/replace commands. (fix differences from specification)
- fixed string search/replace commands. (illegular index problem)
- added `rsub` command
- added `getenv` command
- added `textappend` command
- added `continue` syntax. It can execute in loop syntax only.
- changed `break` syntax. It can execute in loop syntax only.
