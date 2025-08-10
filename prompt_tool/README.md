# Prompt Generation & Model Comparison Tool

This prototype provides a simple interface for crafting AI prompts and
comparing responses across multiple models. It consists of a lightweight
Express backend and a React-based frontend loaded via CDN scripts.

## Features
- **Generate Tab** – Create prompts using mode and style helpers, with quick starter chips.
- **Compare Models Tab** – Submit a prompt to multiple models and view stubbed responses side by side.
- **Prompt Library** – Save optimized prompts for later use (stored in `backend/data/prompts.json`).
- **Responsive Design** – Uses a mobile-friendly flex layout with an orange/tan color palette.

## Running Locally
1. Install backend dependencies (Express and CORS):
   ```bash
   cd backend
   npm install
   npm start
   ```
2. Serve the frontend files (e.g. using `npx serve` or any static server) and open `index.html` in a browser.

The backend listens on `http://localhost:3001` by default.

## Notes
This project is a starting point. Real model integrations, authentication,
and advanced history/versioning would need to be implemented for a
production-ready tool.
