# Deploying the Telegram bot to Render

This branch (add-render-bot) contains a Render-ready Telegram bot implementation.

Files added:
- bot.py: Main application. Reads BOT_TOKEN from environment and supports polling (worker) or webhook (web) modes.
- requirements.txt: Python dependencies.
- Dockerfile: Optional container image build.
- render.yaml: Render service configuration (worker by default using polling).
- .dockerignore: Dockerignore file.

Quick deploy (recommended: Background Worker / polling)
1. In Render dashboard, click New -> Web Service or Background Worker. Recommended: Background Worker for polling mode.
2. Connect your GitHub repository and select branch `add-render-bot`.
3. Set build command (if not using render.yaml): `pip install -r requirements.txt`
4. Start command: `python bot.py`
5. Add Environment Variables (Render > Environment):
   - BOT_TOKEN = <your Telegram bot token> (mark as secret)
   - GITHUB_BASE_URL = https://yunes2009.github.io/Yee  (optional)
   - RENDER_EXTERNAL_URL = (leave empty to use polling, or set to your public service HTTPS URL to enable webhook mode)

Notes on webhook mode
- If you prefer webhook mode (Web Service), set RENDER_EXTERNAL_URL to your service public URL (e.g. https://my-app.onrender.com). The bot will register a webhook at `/webhook/{BOT_TOKEN}` automatically.
- For webhook mode it's recommended to use a Web Service (not a Background Worker) so Render exposes an HTTP endpoint.

Local testing
- To test locally with polling: set BOT_TOKEN in your environment and run `python bot.py`.
- To test webhook locally, use ngrok to expose your local port and set RENDER_EXTERNAL_URL accordingly.

Security
- Never commit BOT_TOKEN. If your token was ever committed, revoke it via BotFather and create a new one.

Support
If you want, I can:
- Open a Pull Request from this branch to your main branch.
- Configure webhook mode and add a health endpoint.
- Set up a Docker-based deployment configuration.
