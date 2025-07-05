# Gemini CLI Directives

- When running `docker-compose up`, always use the `-d` flag to run in detached mode unless explicitly instructed otherwise.
- For other long-running processes, consider using `&` to run them in the background or confirm with the user if a new terminal window is preferred (though this is not directly supported by the current toolset).
