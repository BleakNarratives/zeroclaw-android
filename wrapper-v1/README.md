# Setup and Deployment Guide

This project is designed to be easily deployed to Android devices and provides a Python TCP bridge.

## Directory Structure
- `wrapper-v1/`: Main wrapper directory for the project.
- `wrapper-v1/bridge.py`: Python TCP bridge script.
- `wrapper-v1/app/src/main/AndroidManifest.xml`: Android manifest.
- `wrapper-v1/app/src/main/java/com/bleaknarratives/zeroclaw_wrapper/MainActivity.kt`: Main Compose activity.
- `wrapper-v1/app/build.gradle.kts`: Gradle build config.
- `wrapper-v1/app/src/main/res/values/strings.xml`: String resources.
- `wrapper-v1/.github/workflows/android-build.yml`: CI/CD for Android builds.
- `wrapper-v1/.github/workflows/bridge-test.yml`: Python bridge testing.
- `wrapper-v1/scripts/deploy.sh`: Automated deployment script to Termux.
