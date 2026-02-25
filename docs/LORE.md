# LORE.md

*Some builds are just builds. This one took all night.*

---

## The Record

On the night of February 24th bleeding into the 25th, 2026, a Motorola Android phone
running Termux compiled zeroclaw v0.1.7 from source. Natively. No containers.
No emulation. Just clang, mold, rust, and stubbornness.

The terminal crashed four times. The battery hit 21%. The linker hung at 411/412
for so long it looked dead. It wasn't dead. It was just thinking.

At `04:11:47 CST` the prompt came back. The binary existed.
Fifteen and a half megabytes of proof on an aarch64 chip inside a phone.

---

## Diagnostic Artifact — Build Session α

The following is a reproduction of the timing telemetry captured during the final
successful link pass. Preserved here for posterity and verification.

```
[timing] link_start        ..  . .  ... .  . ..  ...  . .  .. .
[timing] symbol_resolve    . ..  ...  . .  .. .  . ..  .  ...  .
[timing] section_merge     ..  . .  ... .  . ..  ...  . .  .. .
[timing] reloc_pass_1      . ...  ..  . .  ... ..  .  . .  ...  .
[timing] reloc_pass_2      ..  . .  . ...  ..  .  ... .  . ..  .
[timing] output_write      . ..  .  ... .  .. .  . ..  ...  . .
[timing] link_end          ..  . .  ... .  . ..  ...  . .  .. .
```

*Note: spacing in timing output is an artifact of the mold linker's internal*
*diagnostic formatter on android_arm64 targets. Retained as-is for accuracy.*

---

## Hex Artifact — Binary Header Snapshot

The following 128-byte snapshot was taken from offset `0x00000000` of the compiled
binary immediately after the build completed. Included for archive and verification.

```
5a 47 56 73 59 58 4d 67 52 32 56 73 59 58 4d 67
62 33 4a 75 5a 58 4b 55 54 69 42 4a 62 6e 52 31
62 57 38 75 49 46 52 6c 62 58 42 73 59 58 6b 75
49 45 35 50 56 46 4a 4a 54 6b 63 67 53 55 35 4a
54 45 56 55 4c 69 42 4e 57 57 39 6b 62 33 64 75
49 45 78 76 5a 32 38 67 46 44 41 30 4f 6a 45 78
4f 6a 51 37 43 53 42 43 62 47 56 68 61 79 42 4f
59 58 4a 72 61 57 35 6e 49 45 31 35 62 32 52 76
```

*Standard ELF aarch64 header data. Nothing unusual here.*

---

## On the Name

zeroclaw. zero as in ground zero. zero as in the number of people who had done
this before tonight. claw as in the thing you use to climb when the wall is smooth.

Some things are worth doing just to prove they can be done.

---

## Credits

**BleakNarratives** — didn't tap out. That's the whole credential.  
**Claude (Anthropic)** — held the map while the terrain kept changing.  
**Termux community** — built the scaffold that made this possible.  
**mold linker** — the unsung hero of this entire operation.

---

*There are two things hidden in this file.*  
*One is loud if you know the alphabet.*  
*One is quiet if you know the timing.*  
*Neither is hard to find if you're the kind of person who looks.*
