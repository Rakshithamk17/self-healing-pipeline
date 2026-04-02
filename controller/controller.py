import time
import requests
import subprocess
import os
from datetime import datetime

PROMETHEUS_URL = "http://localhost:9090"
JENKINS_URL = "http://localhost:8080"
JENKINS_JOB = "self-healing-pipeline"
SIMULATED_JENKINS_URL = "http://localhost:3000"
FLASK_APP_PATH = r"C:\ProgramData\Jenkins\.jenkins\workspace\self-healing-pipeline"
PYTHON_PATH = r"C:\Users\yashr\AppData\Local\Programs\Python\Python312\python.exe"
CHECK_INTERVAL = 30

flask_process = None

def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def start_flask():
    global flask_process
    try:
        log("🔄 Starting Flask app...")
        flask_process = subprocess.Popen(
            [PYTHON_PATH, "app.py"],
            cwd=FLASK_APP_PATH
        )
        time.sleep(3)
        log("✅ Flask app started!")
    except Exception as e:
        log(f"⚠️ Could not start Flask: {e}")

def check_flask_app():
    global flask_process
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            log("✅ Flask app is healthy")
            return True
        else:
            log(f"⚠️ Flask app returned status {response.status_code}")
            return False
    except Exception:
        log("❌ Flask app is DOWN! Auto-restarting...")
        start_flask()
        return False

def check_jenkins_last_build():
    try:
        url = f"{JENKINS_URL}/job/{JENKINS_JOB}/lastBuild/api/json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            result = data.get("result")
            building = data.get("building")
            if building:
                log("🔄 Jenkins build is currently running...")
            elif result == "SUCCESS":
                log("✅ Last Jenkins build: SUCCESS")
            elif result == "FAILURE":
                log("❌ Last Jenkins build FAILED! Triggering retry...")
                retry_jenkins_build()
            else:
                log(f"ℹ️ Jenkins build result: {result}")
        else:
            log(f"⚠️ Could not reach Jenkins API: {response.status_code}")
    except Exception as e:
        log(f"⚠️ Jenkins check error: {e}")

def retry_jenkins_build():
    try:
        url = f"{JENKINS_URL}/job/{JENKINS_JOB}/build"
        response = requests.post(url, timeout=5)
        if response.status_code in [200, 201]:
            log("🔁 Successfully triggered Jenkins retry build!")
        else:
            log(f"⚠️ Could not trigger retry: {response.status_code}")
    except Exception as e:
        log(f"⚠️ Retry error: {e}")

def check_prometheus_metrics():
    try:
        query = "app_request_count_total"
        url = f"{PROMETHEUS_URL}/api/v1/query?query={query}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("data", {}).get("result", [])
            if results:
                log(f"📊 Prometheus metrics OK — {len(results)} series found")
            else:
                log("⚠️ No metrics data found in Prometheus")
        else:
            log("⚠️ Could not reach Prometheus")
    except Exception as e:
        log(f"⚠️ Prometheus check error: {e}")

def check_simulated_jenkins():
    try:
        response = requests.get(f"{SIMULATED_JENKINS_URL}/jobs", timeout=5)
        if response.status_code == 200:
            jobs = response.json()
            failed_jobs = [j for j in jobs if j['status'] == 'failed']
            queued_jobs = [j for j in jobs if j['status'] == 'queued']
            in_progress = [j for j in jobs if j['status'] == 'in_progress']
            completed = [j for j in jobs if j['status'] == 'completed']

            log(f"📋 Simulated Jenkins — Queued: {len(queued_jobs)} | In Progress: {len(in_progress)} | Completed: {len(completed)} | Failed: {len(failed_jobs)}")

            # Auto retry failed simulated jobs
            for job in failed_jobs[-2:]:  # retry last 2 failed jobs
                log(f"❌ Simulated job failed: {job['repo']} — triggering retry...")
                retry_simulated_job(job)
        else:
            log("⚠️ Could not reach Simulated Jenkins")
    except Exception as e:
        log(f"⚠️ Simulated Jenkins check error: {e}")

def retry_simulated_job(job):
    try:
        payload = {
            "repo": job['repo'],
            "branch": job['branch'],
            "commit_hash": job['commit_hash'] + "-retry",
            "language": job['language']
        }
        response = requests.post(
            f"{SIMULATED_JENKINS_URL}/webhook",
            json=payload,
            timeout=5
        )
        if response.status_code == 201:
            log(f"🔁 Retry job created for {job['repo']}")
        else:
            log(f"⚠️ Could not create retry job: {response.status_code}")
    except Exception as e:
        log(f"⚠️ Retry simulated job error: {e}")

def run():
    log("🚀 Self-Healing Controller started!")
    log("🔗 Watching: Flask + Real Jenkins + Simulated Jenkins + Prometheus")
    log(f"📡 Checking every {CHECK_INTERVAL} seconds...")
    log("=" * 60)

    # Auto start Flask on launch
    start_flask()

    while True:
        log("--- Running health checks ---")
        check_flask_app()
        check_jenkins_last_build()
        check_prometheus_metrics()
        check_simulated_jenkins()
        log(f"--- Done. Next check in {CHECK_INTERVAL} seconds ---")
        print()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run()