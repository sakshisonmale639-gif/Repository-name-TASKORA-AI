from agent import run_agent

print("Testing TASKORA...")

response = run_agent(
    "Hello TASKORA! Introduce yourself in one sentence."
)

print("\n========== TASKORA ==========")
print(response)
print("=============================")