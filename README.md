[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&random=false&width=435&lines=%EC%9E%91%EC%97%85%EC%83%9D%EC%84%B1%EC%9D%84+%EC%9C%84%ED%95%9C+DB+%EC%83%9D%EC%84%B1+%EC%98%88%EC%A0%9C)](https://git.io/typing-svg)

먼저, 새로운 데이터베이스를 생성합니다. 이 예제에서는 데이터베이스 이름을 airflow_tasks_db로 가정합니다.

```sql
CREATE DATABASE airflow_tasks_db;
```


task_info 테이블에는 Airflow에서 실행할 작업의 이름(task_name)과 파라미터(task_params)를 저장합니다. 
또한, 각 작업이 속한 워크플로우의 ID(workflow_id)를 포함할 수 있습니다.

```sql
USE airflow_tasks_db;

CREATE TABLE task_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    task_params TEXT NOT NULL
);
```

task_info 테이블에 예제 작업 정보를 삽입합니다. 
이 예제에서는 workflow_1 ID를 가진 세 개의 작업(stop_server, wait_30m, start_server)을 추가합니다.

```sql
INSERT INTO task_info (workflow_id, task_name, task_params) VALUES
('workflow_1', 'stop_server', '{"server_id": "server_123"}'),
('workflow_1', 'wait_30m', '{}'),
('workflow_1', 'start_server', '{"server_id": "server_123"}');
```
