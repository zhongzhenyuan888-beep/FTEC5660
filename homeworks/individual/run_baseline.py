import time
from metagpt.software_company import generate_repo

start_time = time.time()
print("🚀 开始运行：基于 [gemini-2.5-flash] 的软件开发团队")

repo = generate_repo("Create a simple Python command-line password generator.")

end_time = time.time()
print(f"✅ 任务完成！耗时: {end_time - start_time:.2f} 秒")
