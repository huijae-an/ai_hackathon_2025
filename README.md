# ai_hackathon_2025

Setup:

1. Activate python virtual environment
   ```
   python3 -m venv agent
   source agent/bin/activate
   ```
2. Create .env file, and paste your [OpenAI API](https://platform.openai.com/docs/overview)  key in.
   ```
   (editor of your choice) .env
   OPENAI_API_KEY = [your key]
   ```
3. Enable your [Gmail API](https://support.google.com/googleapi/answer/6158841?hl=en), create credential, download credential.json and token.json, and place in in the root directory.
4. Run
   ```
   python3 main.py
   ```
