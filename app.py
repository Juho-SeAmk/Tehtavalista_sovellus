from flask import Flask, render_template, request
import ollama
import logging

app = Flask(__name__)

# Debugging helpers
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

@app.route("/health")
def health():
    return "OK"

@app.route("/raw")
def raw_index():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {"Content-Type": "text/html; charset=utf-8"}
    except Exception as e:
        app.logger.exception("Failed to read template")
        return f"Error reading template: {e}", 500

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    app.logger.debug("Index accessed, method=%s", request.method)
    if request.method == "POST":
        user_tasks = request.form["tasks"]

        if user_tasks.strip() == "":

            result = "Please enter some tasks first."
        else:
            prompt = (
                f"Respond in English. Write a clear and concise weekly plan for household chores and add short, practical tips. "
                f"Use English only and present the plan as a day-by-day list (Monday-Sunday). "
                f"If tasks are comma-separated, distribute them across the week.\n\nTasks: {user_tasks}"
            )
            app.logger.debug("LLM prompt: %s", prompt)
            
            try:
                response = ollama.chat(
                    model="llama3.2:latest",
                    messages=[{"role": "user", "content": prompt}]
                )
                app.logger.debug("LLM raw response: %s", response)
                result = response.get("message", {}).get("content", "") if isinstance(response, dict) else str(response)
                if not result or not str(result).strip():
                    result = "AI returned an empty response; try again or modify the tasks."
            except Exception as e:
                app.logger.exception("LLM call failed")
                result = f"LLM error: {e}"

    return render_template("index.html", result=result)


@app.route("/debug-info")
def debug_info():
    import os
    try:
        cwd = os.getcwd()
        root_list = os.listdir(cwd)
    except Exception as e:
        return f"Error getting cwd or listing: {e}", 500

    templates_exists = os.path.exists("templates")
    templates_list = []
    index_size = "n/a"
    if templates_exists:
        try:
            templates_list = os.listdir("templates")
            index_size = os.path.getsize("templates/index.html") if os.path.exists("templates/index.html") else "missing"
        except Exception as e:
            templates_list = [f"error: {e}"]

    info = [
        f"cwd: {cwd}",
        f"root: {root_list}",
        f"templates_exists: {templates_exists}",
        f"templates_list: {templates_list}",
        f"templates/index.html size: {index_size}",
    ]
    return "\n".join(info), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(debug=True)
