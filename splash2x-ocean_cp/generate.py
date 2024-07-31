import os
import time

job_template = """
apiVersion: v1
kind: Pod
metadata:
  name: {program_name}-{app_name}{index}
  labels:
    app: {app_name}{index}
spec:
  restartPolicy: OnFailure
  containers:
  - name: {app_name}{index}
    image: docker.io/limitstory/parsec-modify:latest
    imagePullPolicy: IfNotPresent
    command: ["/home/parsec-3.0/run"]
    args: ["-a", "run", "-p", "{program_name}.{app_name}", "-i", "native"]
    resources:
      requests:
        memory: {memory_request}Mi
      limits:
        memory: {memory_limit}Mi
        cpu: 200m
"""

node_names = ["worker1", "worker2", "worker3"]
loop_times = 20

program_name = "splash2x"
app_name = "ocean_cp"
set_memory_limit = 3850


memory_percentages = range(10, 21, 1)  # 100%부터 200%까지 10% 단위로 증가

for percentage in memory_percentages:
    memory_request = set_memory_limit // percentage * 10
    memory_limit = set_memory_limit
    file_name = f'{program_name}-{app_name}-{percentage*10}%.py'
    
    with open(file_name, 'w') as script_file:
        script_file.write("import os\nimport time\n\n")
        script_file.write(f"job_template = '''{job_template}'''\n\n")
        script_file.write("node_names = [\"worker1\", \"worker2\", \"worker3\"]\n")
        script_file.write(f"loop_times = {loop_times}\n\n")
        script_file.write(f"program_name = \"{program_name}\"\n")
        script_file.write(f"app_name = \"{app_name}\"\n\n")
        
        script_file.write("for i in range(len(node_names)*loop_times):\n")
        script_file.write("  node_name = node_names[i % len(node_names)]\n")
        script_file.write(f"  job_manifest = job_template.format(index=i, memory_request={memory_request}, memory_limit={memory_limit}, program_name=program_name, app_name=app_name)\n")
        script_file.write("  with open(f'job-{i}.yaml', 'w') as f:\n")
        script_file.write("    f.write(job_manifest)\n")
        script_file.write("  os.system(f'kubectl apply -f job-{i}.yaml')\n")
        script_file.write("  if i%len(node_names) == len(node_names)-1:\n")
        script_file.write("    time.sleep(1)\n")
