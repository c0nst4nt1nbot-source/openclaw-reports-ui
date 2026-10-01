# OpenClaw Reports UI - Quick Start Guide

## Installation & Launch

### Option 1: Automatic Setup (First Time)

```bash
cd /home/dg/openclaw-reports-ui
./start.sh
```

This will:
1. Create a Python virtual environment (first run only)
2. Install all dependencies automatically
3. Launch the web server on `http://localhost:8000`

### Option 2: Quick Launch (After Setup)

If you've already run `./start.sh` once:

```bash
cd /home/dg/openclaw-reports-ui
./run.sh
```

This is faster as it skips dependency checking.

### Option 3: Manual

```bash
cd /home/dg/openclaw-reports-ui

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the application
python app.py
```

## Access the Dashboard

Once running, open your web browser to:

```
http://localhost:8000
```

The server binds to **localhost only** (127.0.0.1) for security.

## First Steps

1. **Home Page** - View system statistics and latest reports
2. **Reports** - Browse all 131 intelligence reports
3. **Database** - Explore the SQLite intelligence database
4. **Query** - Run custom SQL queries (SELECT only)

## Stopping the Server

### Option 1: Keyboard Interrupt
Press `Ctrl+C` in the terminal where the server is running.

### Option 2: Stop Script
```bash
cd /home/dg/openclaw-reports-ui
./stop.sh
```

This will find and kill any process using port 8000.

**Note**: The `start.sh` script now automatically clears port 8000 before starting, so you usually don't need to manually stop the server.

## Features Overview

### Report Browser
- Browse 130+ markdown intelligence reports
- Search by filename, path, or content
- Filter by report type (Daily Brief, Country Report, etc.)
- View rendered markdown with syntax highlighting

### Database Explorer
- View all tables and views in intelligence.db
- Browse table contents with pagination
- Inspect table schemas
- View database statistics

### SQL Query Interface
- Execute custom SELECT queries
- Security-restricted (read-only access)
- Example queries provided
- Results displayed in table format

### Dark Mode 🌙
- Toggle between light and dark themes
- Preference saved automatically (localStorage)
- Click the theme button in the navigation bar
- Smooth transitions between themes

## Troubleshooting

### "externally-managed-environment" Error

If you see this error, it means pip is trying to install packages system-wide instead of in a virtual environment.

**Solution**: The updated `start.sh` script now properly activates the venv before installing packages. Just run:

```bash
cd /home/dg/openclaw-reports-ui
./start.sh
```

If the problem persists, manually create and activate the venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### "python: command not found" Error

Ubuntu uses `python3`, not `python`. The virtual environment automatically creates a `python` symlink, so this error means the venv isn't activated.

**Solution**: Run `./start.sh` which handles activation automatically.

### Port Already in Use

**Automatic Solution**: The `start.sh` script now automatically clears port 8000 before starting.

**Manual Solution**:
```bash
# Option 1: Use the stop script
./stop.sh

# Option 2: Find and kill manually
lsof -i :8000
kill -9 <PID>
```

### Dependencies Not Found
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Database Not Found
Verify path in `modules/db_browser.py` (default: `/home/dg/openclaw-reports/intelligence.db`)

### Virtual Environment Issues

If the venv gets corrupted, delete and recreate it:

```bash
cd /home/dg/openclaw-reports-ui
rm -rf venv
./start.sh
```

## Security Notes

- **Read-Only**: No write operations to database or filesystem
- **Local-Only**: Server only accessible from localhost
- **SQL Restrictions**: Only SELECT queries permitted
- **No External Calls**: Works offline

## System Requirements

- Python 3.7+
- 50MB disk space
- Access to `/home/dg/openclaw-reports/`
- Ubuntu Linux (NUC)

## File Locations

- **Reports**: `/home/dg/openclaw-reports/*.md`
- **Database**: `/home/dg/openclaw-reports/intelligence.db`
- **Application**: `/home/dg/openclaw-reports-ui/`

## Documentation

Full documentation available in `README.md`

---

**Version**: 1.0  
**Build Date**: 2026-03-05  
**Status**: Production Ready ✅
