import os
import time

job_template = '''
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
'''

node_names = ["worker1", "worker2", "worker3"]
loop_times = 84

program_name = "splash2x"
app_name = "water_spatial"

for i in range(len(node_names)*loop_times):
  node_name = node_names[i % len(node_names)]
  job_manifest = job_template.format(index=i, memory_request=850, memory_limit=850, program_name=program_name, app_name=app_name)
  with open(f'job-{i}.yaml', 'w') as f:
    f.write(job_manifest)
  os.system(f'kubectl apply -f job-{i}.yaml')
  if i%len(node_names) == len(node_names)-1:
    time.sleep(1)
