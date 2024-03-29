## ca_bot

### 💾 디렉토리 구조

```
├── ./.github
│   └── ./.github/workflows
│       └── ./.github/workflows/deploy.yml
├── ./README.md
└── ./ca_bot
    ├── ./ca_bot/app.yaml
    ├── ./ca_bot/main.py
    └── ./ca_bot/requirements.txt
```

### 📢 기능

- 메시지에 선임, 책임, 팀장, 담당, 상무, 전무 포함하는 글자 있을 때 reaction
- 메시지가 CA, ca, CA!, ca!와 일치할 때 reaction
- [240326] 보완사항 - '님들'이 뒤에 붙을 때는 trigger 되지 않도록 조정 (negative lookahead assertion (?!님들)을 사용)
- [240326] 보완사항 - 봄날같은 인사, ‘~~~님’과 함께 시작해보세요! 에서 발언한 사람의 이름이 들어가는 게 부자연스러움. 호칭 앞에 있는 이름을 잡도록 변경
    - re.sub(r'<@\w+>', '', text)를 사용하여 입력 텍스트에서 Slack 사용자 멘션을 제거


### 🤐 secrets 관리
1. 프로젝트의 Settings 탭으로 이동합니다.

2. 좌측 사이드바에서 Secrets 섹션을 찾고, Actions를 클릭합니다.

3. New repository secret 버튼을 클릭하여 새로운 시크릿을 추가합니다.

4. 다음 시크릿들을 추가하였습니다:

- GCP_PROJECT_ID: Google Cloud 프로젝트 ID.

- GCP_SA_KEY: Google Cloud 서비스 계정 키 (JSON 형태). Base64로 인코딩되어야 하기 때문에, `base64 <filename.json>` 명령어를 사용하여 인코딩하였습니다.

- SLACK_BOT_TOKEN: Slack Bot Token. ☠️

  - APP_YAML_CONTENT: GitHub Actions workflow에서 app.yaml 파일을 동적으로 생성. 이는 추후 구글 시크릿 매니저나 aws를 사용한다면 AWS 파라미터 스토어 사용해서 이렇게 파일을 굳이 동적으로 만들지 않고 가능함.

### 🤚 테스트 케이스
- 정재근 팀장님 안녕하세요
- @정재근 팀장님 안녕하세요
- 팀장님들 안녕하세요
- 
