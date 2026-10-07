# jaquelin-hellenberg

A personal working repo that collects a few unrelated scratch projects. The repo README is just the title "llmswarm" and the root `main.go` is empty.

## Features

- **ReceiptGen** — a Streamlit app that generates PDF receipts with store logos (Best Buy, Apple, Target, Walmart, GameStop), barcodes, and QR codes. It can call a local Ollama model and ships with `launch.sh` / `run.sh` / `run.bat` launch scripts and a SQLite database (`receipts.db`).
- **Desktop/app** — a Vite + React + Tailwind (shadcn-style components) single-page site showcasing a Teton Peaks property, with a built `dist/` bundle and photos (`hero-teton-view.jpg`, `property-aerial.jpg`, `interior-view.jpg`).
- **Desktop/YouTubeGo** and **Desktop/TetonPeaksViewHome** — project directories (one is an empty stub).
- **Desktop/Sovereign_Report_Selection_1770469437528.txt** — a loose report file.

## Tech stack

Python (Streamlit, fpdf, ollama), React 18, TypeScript, Vite, Tailwind CSS, SQLite.

## Getting started

ReceiptGen: `pip install streamlit ollama fpdf pillow`, then `streamlit run ReceiptGen/app.py` (a local Ollama server is expected for AI features). The React app in `Desktop/app` is a standard Vite project (`Desktop/app/package.json`, `vite.config.ts`).

## Project structure

```
.
├── main.go            # empty
├── README.md          # title only ("llmswarm")
├── ReceiptGen/        # Streamlit receipt-PDF generator
└── Desktop/           # Vite+React property showcase site (app/), misc dirs
```

## Status

**Near-empty / scratch.** A grab-bag of unrelated experiments and exports; no unifying project, no top-level build, and the README is a one-line title.
