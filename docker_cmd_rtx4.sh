img="nvcr.io/nvidia/pytorch:23.06-py3" 

docker run --gpus all  --privileged=true   --workdir /git --name "agent_lab"  -e DISPLAY --ipc=host -d --rm  -p 6233:8889\
 -v /home/ggzhang/AgentLab:/git/agent_lab \
 -v /home/ggzhang/datasets:/git/datasets \
 $img sleep infinity 

docker exec -it agent_lab /bin/bash

#docker images  |grep "agent_lab"  |grep "21."

#docker stop  agent_lab