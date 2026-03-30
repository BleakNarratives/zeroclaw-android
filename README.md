# zeroclaw-android

> **First confirmed native zeroclaw build on Android/Termux.**  
> No proot. No emulation. No compromise. Pure aarch64.

---

## What This Is

This repo documents and delivers the first successful compilation of [zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) on Android using Termux — built natively on `aarch64-unknown-linux-android`, without any Linux container, proot environment, or cross-compilation trickery.

The binary runs directly in Termux. That's it. That's the flex.

**Build completed:** `Wed Feb 25 04:11:47 CST 2026`  
**Device arch:** `aarch64`  
**Kernel:** `Linux 5.4.284-moto`  
**Node:** `v24.13.0` | **Rust/Cargo:** via Termux  
**Build time:** `23m 55s`  
**Binary size:** `15.5MB`

---

## Why It Was Hard

Three things conspire against you on Termux:

1. **The linker is a memory hog.** Android kills processes that spike RAM during the final link stage. zeroclaw's dependency tree is large enough to trigger this reliably.
2. **`make -j` without a number dies.** Termux's `make` is stricter than desktop GNU make — koffi's build script passes `-j` bare, which errors out on `aarch64-unknown-linux-android`.
3. **No swap.** Android blocks `swapon` for unprivileged processes, so you can't just throw a swapfile at the RAM problem the normal way.

The fix wasn't one thing — it was three things at once.

---

## Prerequisites

```bash
pkg update && pkg upgrade
pkg install clang cmake make python nodejs-lts rust binutils-cross mold git
```

---

## Build Instructions

### 1. Clone zeroclaw

```bash
git clone https://github.com/zeroclaw-labs/zeroclaw.git
cd zeroclaw
```

### 2. Create the cargo config

This is the critical step. Create `.cargo/config.toml` inside the zeroclaw directory:

```bash
mkdir -p .cargo && cat > .cargo/config.toml << 'EOF'
[target.aarch64-linux-android]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]

[profile.release]
codegen-units = 1
opt-level = "z"
lto = "thin"
EOF
```

**What each flag does:**
- `mold` — replaces the default linker with one that uses a fraction of the RAM
- `codegen-units = 1` — serializes compilation, reduces peak memory usage
- `opt-level = "z"` — optimize for size, not speed (lighter on RAM during compile)
- `lto = "thin"` — link-time optimization without the full memory cost of `lto = true`

### 3. Build

```bash
cargo build --release 2>&1 | tee build_log.txt
```

Drop `--locked` if you hit dependency resolution errors. Watch the output — it will compile 412 crates and take 20-30 minutes on most Android hardware. The last step (linking `zeroclaw` itself) is the longest and will appear to hang. **It is not hung.** Let it finish.

### 4. Confirm

```bash
date && ls -la target/release/zeroclaw
./target/release/zeroclaw --version
```

---

## Prebuilt Binary

A prebuilt binary for `aarch64-android` is included in this repo at `bin/zeroclaw`.

```bash
chmod +x bin/zeroclaw
./bin/zeroclaw --version
```

Built on a Motorola device running kernel `5.4.284-moto`. Should run on any aarch64 Android device with Termux.

---

## What Failed Before This Worked

In the interest of saving you the same pain:

- `npm install -g openclaw` — fails because koffi passes `make -j` with no number; Termux make rejects it
- `cargo build --release --locked` without the cargo config — terminal crashes during link step (OOM)
- `swapon` — blocked by Android for unprivileged users, don't bother
- `wait <pid>` to monitor the build — also kills the terminal on some Android versions
- Gemini CLI — tried. Failed.
- Gemini Android app — tried. Failed.

---

## License

MIT — see [LICENSE](LICENSE)

---

## Lore

See [LORE.md](LORE.md). There's something hidden in there. Find it.

---

*Built by [@BleakNarratives](https://github.com/BleakNarratives) with an assist from Claude.*  
*If this helped you, star the repo. If it didn't work, open an issue.*

## Support
https://ko-fi.com/bleaknarratives

## Support
https://ko-fi.com/bleaknarratives

## Support
https://ko-fi.com/bleaknarratives
