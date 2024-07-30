import os
import time

job_template = """
apiVersion: v1
kind: Pod
metadata:
  name: parsec-raytrace{index}
  labels:
    app: raytrace{index}
spec:
  restartPolicy: OnFailure
  containers:
  - name: raytrace{index}
    image: docker.io/limitstory/parsec-modify:latest
    imagePullPolicy: IfNotPresent
    command: ["/home/parsec-3.0/run"]
    args: ["-a", "run", "-p", "parsec.raytrace", "-i", "native"]
    resources:
      requests:
        memory: 1200Mi
      limits:
        memory: 1300Mi
        cpu: 200m
  nodeName: {node_name}
"""

node_names = ["worker1", "worker2", "worker3"]
loop_times = 55

for i in range(len(node_names)*loop_times):
  node_name = node_names[i % len(node_names)]
  job_manifest = job_template.format(index=i, node_name=node_name)
  with open(f'job-{i}.yaml', 'w') as f:
    f.write(job_manifest)
  os.system(f'kubectl apply -f job-{i}.yaml')
  if i%len(node_names) == len(node_names)-1:
    time.sleep(1)  # 1초 간격으로 Job 생성
