# Root My Galaxy — Safe Root development

Development repository for a **separate, experimental** recovery build. No production APK or daemon has been validated.

## Sources
- Android app: https://github.com/BuSung-dev/Root-My-Galaxy
- KernelSU-Next daemon: https://github.com/0x11DFE/KernelSU-Next/tree/samsung-lateload-sync (use supplied source ZIP if branch unavailable)
- Payload feed (must remain unchanged until tested): https://github.com/gamer765/Root-My-Galaxy-Payloads

## Safety requirements
- Safe Root must skip third-party module loading, scripts, and mounts before zygote initialization.
- The Android helper must pass `--late-load` and `--safe-mode` as **separate argv tokens**; a single string is not sufficient.
- Normal Root must remain the default; never auto-root after a crash.
- Build daemon, package a distinct app ID, and test artifact hashes and a rollback path before publishing to the feed.

The prior source patch is **incomplete**: it does not implement the UI, and helper argument handling is unverified. Do not flash or install a test build without further review.
